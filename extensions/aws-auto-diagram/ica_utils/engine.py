"""Headless render engine for ICA.

This module holds the rendering orchestration that previously lived on the
`inkex.EffectExtension` subclass in ``aws-auto-diagram.py``. It is pure Python
and uses ``inkex`` only as an SVG-tree library — no Inkscape process is launched
(verified: ``Use.bounding_box()`` works headless).

Two front-ends share this one implementation:

* The Inkscape extension (``aws-auto-diagram.py``) — its ``effect()`` builds a
  ``RenderDoc`` bound to its own live ``self.svg`` and runs the orchestration.
* The headless ``render()`` entry point — builds a blank inkex SVG, runs the same
  orchestration, and returns the serialized SVG string.

The resource modules already take an ``inkdoc`` parameter; ``RenderDoc`` provides
exactly the surface they use: ``.svg`` and ``make_symbol_instance()``.
"""

import os
from pathlib import Path

import inkex
from inkex import Use, Transform

from ica_utils import cloudia_parser
from ica_utils import resource_vpc
from ica_utils import resource_account
from ica_utils import resource_region
from ica_utils import resource_s3
from ica_utils import resource_lambda
from ica_utils import resource_edge
from ica_utils import resource_dynamodb
from ica_utils.layout import Stack, Row
from ica_utils.layers import get_or_create_layer
from ica_utils.config import load_config, resolve_layout_mode
from ica_utils.theme import resolve_theme, get_background
from ica_utils.legend import render_legend
from ica_utils.icalog import debug


# Symbol files imported into every document (unchanged from the extension).
SYMBOL_FILES = [
    "AWS-Group-light.svg",
    "AWS-Resource-compute-light.svg",
    "AWS-Resource-networking-content-delivery-light.svg",
    "AWS-Resource-database-light.svg",
    "AWS-Resource-storage-light.svg",
    "AWS-Service-containers.svg",
]


def default_symbol_dir():
    """The Inkscape symbol location — the historical default."""
    return str(Path.home()) + "/.config/inkscape/symbols/aws-architect"


def resolve_symbol_dir(config=None, symbol_dir=None):
    """Resolve where AWS symbol SVGs live.

    Resolution order (first present wins):
      1. explicit ``symbol_dir`` argument (CLI/engine option)
      2. ``config["symbols"]["dir"]`` (user/default config)
      3. the Inkscape install location (current behavior)

    Inkscape installs hit case 3 and are therefore unchanged.
    """
    if symbol_dir:
        return symbol_dir
    if config:
        cfg_dir = config.get("symbols", {}).get("dir")
        if cfg_dir:
            return cfg_dir
    return default_symbol_dir()


class RenderDoc:
    """A document object the resource renderers draw into.

    Holds an inkex ``SvgDocumentElement`` as ``.svg`` plus the small surface the
    renderers require. Constructed by the headless engine; the Inkscape extension
    provides the equivalent surface from its own ``self``.
    """

    def __init__(self, svg, config=None, options=None, symbol_dir=None):
        self.svg = svg
        self.config = config
        self.options = options
        self.symbol_dir = symbol_dir

    # --- symbol import (moved verbatim from the extension) ------------------ #

    def import_defs_from_external_file_in_document(self):
        sym_dir = resolve_symbol_dir(self.config, self.symbol_dir)
        for symbol_group in SYMBOL_FILES:
            svg_file_path = f"{sym_dir}/{symbol_group}"
            self._import_symbol_file(symbol_group, svg_file_path)

    def _import_symbol_file(self, symbol_group, svg_file_path):
        try:
            external_svg = inkex.load_svg(svg_file_path)

            if external_svg:
                debug(f"Successfully loaded SVG from {svg_file_path}")

                external_defs = external_svg.getroot().find('{http://www.w3.org/2000/svg}defs')

                if external_defs is not None:
                    external_symbols = external_defs.findall('{http://www.w3.org/2000/svg}symbol')

                    if external_symbols:
                        debug(f"Found {len(external_symbols)} symbols in {symbol_group}")

                        if self.svg.defs is None:
                            self.svg.defs = self.svg.getroot().add(inkex.elements._defs.Defs())

                        for symbol in external_symbols:
                            symbol_copy = symbol.copy()
                            symbol_id = symbol.get('id')
                            symbol_dest_id = f"{symbol_group}:{symbol_id}"
                            symbol_copy.set('id', symbol_dest_id)
                            existing_symbols = self.svg.defs.findall(f".//*[@id='{symbol_dest_id}']")

                            if not existing_symbols:
                                self.svg.defs.append(symbol_copy)
                                debug(f"Imported symbol: {symbol_id} > {symbol_dest_id}")
                            else:
                                debug(f"Symbol {symbol_id} already exists in document, skipping")
                    else:
                        debug(f"No symbols found in {symbol_group}")
                else:
                    debug(f"No defs section found in {symbol_group}")
            else:
                debug(f"Failed to load SVG from {svg_file_path}")
        except Exception as e:
            debug(f"Error importing symbols from {symbol_group}: {str(e)}")

    # --- symbol instance (moved verbatim from the extension) --------------- #

    def make_symbol_instance(self, symbol_id, parent):
        use_element = Use()
        use_element.set('xlink:href', f'#{symbol_id}')
        parent.append(use_element)

        bbox = use_element.bounding_box()
        origin_translate = -Transform().add_translate(bbox.left, bbox.top)
        use_element.transform = use_element.transform @ origin_translate

        return use_element

    # --- orchestration (moved verbatim from the extension) ----------------- #

    def render(self):
        """Run the full render against this doc. Requires self.config/options set."""
        self.import_defs_from_external_file_in_document()

        layout_mode = self.options.layout_mode or "spaced"
        resolve_layout_mode(self.config, layout_mode)

        theme_name = self.options.theme or "light"
        self.config["_theme"] = resolve_theme(theme_name, self.config)

        data_dir = self.options.data_dir
        region = self.options.region

        if not data_dir:
            debug("No account data directory specified")
            return

        account_name = self.options.account_name.strip() if self.options.account_name else ""
        account_id = Path(data_dir).name
        if account_name:
            account_label = f"{account_name} ({account_id})"
        else:
            account_label = account_id
        multi_region = (region == "all")

        if multi_region:
            self._render_multi_region(data_dir, account_label)
        else:
            self._render_single_region(data_dir, region, account_label)

        render_legend(self, config=self.config)
        self.resize_to_fit()

    def _create_layers(self, multi_region):
        """Pre-create layers in z-order (bottom to top)."""
        az_cfg = self.config.get("layout", {}).get("availability_zone", {})
        get_or_create_layer(self, "Edge")
        get_or_create_layer(self, "Accounts")
        if multi_region:
            get_or_create_layer(self, "Regions")
        get_or_create_layer(self, "VPCs")
        if az_cfg.get("enabled", True):
            get_or_create_layer(self, "Availability Zones")
        get_or_create_layer(self, "Subnets")
        get_or_create_layer(self, "EC2")
        get_or_create_layer(self, "Load Balancers")
        get_or_create_layer(self, "EKS")
        get_or_create_layer(self, "Lambda")
        get_or_create_layer(self, "Database")
        get_or_create_layer(self, "Auto Scaling Groups")
        get_or_create_layer(self, "NAT Gateways")
        get_or_create_layer(self, "Route 53 Private")
        get_or_create_layer(self, "S3")
        get_or_create_layer(self, "DynamoDB")
        get_or_create_layer(self, "Legend")

    def _render_vpcs(self, vpcs, subnets, instances, load_balancers, db_instances, eks_clusters, vpc_lambdas, nat_gateways, auto_scaling_groups, stack, private_r53_zones=None):
        """Render VPCs into a Stack."""
        private_r53_zones = private_r53_zones or []
        auto_scaling_groups = auto_scaling_groups or []
        for vpc in vpcs:
            vpc_subnets = [s for s in subnets if s["vpc_id"] == vpc["vpc_id"]]
            vpc_instances = [i for i in instances if i["vpc_id"] == vpc["vpc_id"]]
            vpc_lbs = [lb for lb in load_balancers if lb["vpc_id"] == vpc["vpc_id"]]
            vpc_dbs = [db for db in db_instances if db["vpc_id"] == vpc["vpc_id"]]
            vpc_eks = [c for c in eks_clusters if c["vpc_id"] == vpc["vpc_id"]]
            vpc_lam = [fn for fn in vpc_lambdas if fn["vpc_id"] == vpc["vpc_id"]]
            vpc_nats = [n for n in nat_gateways if n["vpc_id"] == vpc["vpc_id"]]
            vpc_asgs = [a for a in auto_scaling_groups if a["vpc_id"] == vpc["vpc_id"]]
            resource_vpc.render_vpc_with_subnets(
                self, vpc, vpc_subnets, stack, config=self.config,
                instances=vpc_instances, load_balancers=vpc_lbs, db_instances=vpc_dbs,
                eks_clusters=vpc_eks, vpc_lambdas=vpc_lam, nat_gateways=vpc_nats,
                private_r53_zones=private_r53_zones, auto_scaling_groups=vpc_asgs)

    def _render_single_region(self, data_dir, region, account_label):
        """Render a single region (no region rect, original behavior)."""
        vpcs, subnets, instances, load_balancers, db_instances, eks_clusters, vpc_lambdas, _non_vpc_lambdas, nat_gateways, auto_scaling_groups, dynamodb_tables = cloudia_parser.parse_region(data_dir, region)

        # Parse global services for Edge zone
        global_data = cloudia_parser.parse_global_services(data_dir)

        self._create_layers(multi_region=False)

        layout = self.config.get("layout", {})
        vpc_gap = layout.get("vpc", {}).get("gap", resource_vpc.DEFAULT_VPC_GAP)
        acct_pad = layout.get("account", {}).get("padding", {})
        stack_x = 10 + acct_pad.get("left", 20)
        stack_y = 10 + acct_pad.get("top", 50)

        # Render Edge zone
        r53_public = global_data.get("route53_public_zones", [])
        cf_dists = global_data.get("cloudfront_distributions", [])
        r53_private = global_data.get("route53_private_zones", [])

        if r53_public or cf_dists:
            edge_w, edge_h = resource_edge.render_edge_zone(
                self, r53_public, cf_dists, stack_x, stack_y, config=self.config)
            stack_y += edge_h + resource_edge.get_bottom_spacing(self.config)

        # Determine private zone placement
        private_zones_for_vpcs = self._assign_private_zones(r53_private, vpcs)

        stack = Stack(x=stack_x, y=stack_y, gap=vpc_gap)
        self._render_vpcs(vpcs, subnets, instances, load_balancers, db_instances, eks_clusters, vpc_lambdas, nat_gateways, auto_scaling_groups, stack, private_r53_zones=private_zones_for_vpcs)

        # Render DynamoDB tables below VPCs
        if dynamodb_tables:
            ddb_y = stack.cursor_y
            resource_dynamodb.render_tables(self, dynamodb_tables, stack_x, ddb_y, config=self.config)

        resource_account.render_account_rect(self, account_label, config=self.config)

    def _assign_private_zones(self, private_zones, vpcs):
        """Assign private R53 zones to VPCs using fallback logic."""
        if not private_zones:
            return []
        non_default_vpcs = [v for v in vpcs if not v.get("is_default", False)]
        if len(non_default_vpcs) == 1:
            return private_zones
        return []

    def _render_multi_region(self, data_dir, account_label):
        """Render all non-empty regions side by side."""
        regions = cloudia_parser.parse_all_regions(data_dir)
        if not regions:
            debug("No non-default regions found")
            return

        self._create_layers(multi_region=True)

        layout = self.config.get("layout", {})
        vpc_gap = layout.get("vpc", {}).get("gap", resource_vpc.DEFAULT_VPC_GAP)
        region_pad = resource_region.get_region_padding(self.config)
        region_gap = resource_region.get_region_gap(self.config)

        acct_pad = layout.get("account", {}).get("padding", {})
        row_x = 10 + acct_pad.get("left", 20)
        row_y = 10 + acct_pad.get("top", 50)

        r53_public = []
        cf_dists = []
        r53_private = []
        if regions and isinstance(regions[0][1], dict):
            global_data = regions[0][1]
            r53_public = global_data.get("route53_public_zones", [])
            cf_dists = global_data.get("cloudfront_distributions", [])
            r53_private = global_data.get("route53_private_zones", [])

        if r53_public or cf_dists:
            edge_w, edge_h = resource_edge.render_edge_zone(
                self, r53_public, cf_dists, row_x, row_y, config=self.config)
            row_y += edge_h + resource_edge.get_bottom_spacing(self.config)

        row = Row(x=row_x, y=row_y, gap=region_gap)

        for entry in regions:
            region_name = entry[0]
            reg_x, reg_y = row.next_position()

            if isinstance(entry[1], dict):
                global_data = entry[1]
                content_x = reg_x + region_pad["left"]
                content_y = reg_y + region_pad["top"]

                content_w, content_h = 0, 0
                cursor_y = content_y

                s3_buckets = global_data.get("s3_buckets", [])
                if s3_buckets:
                    s3_w, s3_h = resource_s3.render_buckets(
                        self, s3_buckets, content_x, cursor_y, config=self.config)
                    content_w = max(content_w, s3_w)
                    cursor_y += s3_h + 10  # gap between sections
                    content_h = cursor_y - content_y

                global_lambdas = global_data.get("lambdas", [])
                if global_lambdas:
                    lam_w, lam_h = resource_lambda.render_non_vpc_lambdas(
                        self, global_lambdas, content_x, cursor_y, config=self.config)
                    content_w = max(content_w, lam_w)
                    cursor_y += lam_h
                    content_h = cursor_y - content_y
            else:
                _, vpcs, subnets, instances, load_balancers, db_instances, eks_clusters, vpc_lambdas, nat_gateways, auto_scaling_groups, dynamodb_tables = entry
                stack_x = reg_x + region_pad["left"]
                stack_y = reg_y + region_pad["top"]
                stack = Stack(x=stack_x, y=stack_y, gap=vpc_gap)

                private_zones_for_vpcs = self._assign_private_zones(r53_private, vpcs)
                self._render_vpcs(vpcs, subnets, instances, load_balancers, db_instances, eks_clusters, vpc_lambdas, nat_gateways, auto_scaling_groups, stack, private_r53_zones=private_zones_for_vpcs)

                content_h = stack.cursor_y - stack_y - stack.gap
                if content_h < 0:
                    content_h = 0
                content_w = stack.max_width

                if dynamodb_tables:
                    ddb_y = stack.cursor_y
                    ddb_w, ddb_h = resource_dynamodb.render_tables(
                        self, dynamodb_tables, stack_x, ddb_y, config=self.config)
                    content_h = (ddb_y - stack_y) + ddb_h
                    content_w = max(content_w, ddb_w)

            region_w = region_pad["left"] + content_w + region_pad["right"]
            region_h = region_pad["top"] + content_h + region_pad["bottom"]

            resource_region.render_region_rect(
                self, region_name, [reg_x, reg_y], [region_w, region_h], config=self.config)

            row.advance(region_w, region_h)

        resource_account.render_account_rect(self, account_label, config=self.config)

    def resize_to_fit(self):
        """Resize document to fit all rendered content plus configured margin."""
        bbox = None
        for elem in self.svg.descendants():
            if isinstance(elem, inkex.ShapeElement):
                try:
                    eb = elem.bounding_box()
                    if eb is not None:
                        bbox = eb if bbox is None else (bbox + eb)
                except Exception:
                    continue

        if bbox is None:
            return

        margin = self.config.get("document", {}).get("margin", 20)

        shift_x = margin - bbox.left
        shift_y = margin - bbox.top
        if abs(shift_x) > 0.01 or abs(shift_y) > 0.01:
            for layer in self.svg.findall('{http://www.w3.org/2000/svg}g'):
                layer.transform = Transform(f'translate({shift_x}, {shift_y})') @ layer.transform

        width = (bbox.width) + 2 * margin
        height = (bbox.height) + 2 * margin
        self.svg.set('width', str(width))
        self.svg.set('height', str(height))
        self.svg.set('viewBox', f'0 0 {width} {height}')

        bg_color = get_background(self.config)
        if bg_color and bg_color != "none":
            from inkex.elements import Rectangle
            bg_rect = Rectangle.new(0, 0, width, height)
            bg_rect.style = {"fill": bg_color, "stroke": "none"}
            self.svg.insert(0, bg_rect)


# --------------------------------------------------------------------------- #
# Options container + headless entry point
# --------------------------------------------------------------------------- #


class _Options:
    """Minimal stand-in for the inkex parsed options namespace."""

    def __init__(self, data_dir, region, account_name="", theme="light", layout_mode="spaced"):
        self.data_dir = data_dir
        self.region = region
        self.account_name = account_name
        self.theme = theme
        self.layout_mode = layout_mode


# Byte-for-byte the same blank canvas the file-based runner used to create
# (newline + 2-space indent before <defs>), minus the XML declaration which
# lxml rejects on a *str*. The whitespace is preserved by lxml as tail text, so
# headless output matches the previous subprocess output exactly.
_BLANK_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"\n'
    '     width="800" height="600" viewBox="0 0 800 600">\n'
    '  <defs/>\n'
    '</svg>'
)


def render(data_dir, region, account_name="", theme="light", layout_mode="spaced",
           symbol_dir=None, extension_dir=None):
    """Render a diagram headlessly and return the SVG as a string.

    No ``inkex.EffectExtension`` is instantiated and no Inkscape process is
    spawned. Writing the result to a file (and where) is the caller's concern.
    """
    if extension_dir is None:
        extension_dir = str(Path(__file__).resolve().parent.parent)

    config = load_config(extension_dir)
    options = _Options(data_dir, region, account_name, theme, layout_mode)

    svg = inkex.load_svg(_BLANK_SVG).getroot()
    doc = RenderDoc(svg, config=config, options=options, symbol_dir=symbol_dir)
    doc.render()

    return svg.tostring().decode("utf-8") if isinstance(svg.tostring(), bytes) else svg.tostring()
