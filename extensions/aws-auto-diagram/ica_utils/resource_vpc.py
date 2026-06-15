import re
import inkex
from inkex.elements import TextElement, Rectangle, Group, PathElement, Line, Symbol
from inkex import Use, Transform
from ica_utils.icalog import debug
from ica_utils.layout import Grid, Stack
from ica_utils.layers import get_or_create_layer
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils import resource_az
from ica_utils import resource_ec2
from ica_utils import resource_lb
from ica_utils import resource_db
from ica_utils import resource_eks
from ica_utils import resource_lambda
from ica_utils import resource_nat
from ica_utils import resource_asg
from ica_utils import resource_route53
from ica_utils.theme import get_text_color, get_border_color
from ica_utils.legend import register_legend

FONT_SIZE_PX = 17
ICON_SCALE = 1.0
ICON_SIZE = 40
ICON_PADDING = 2
LABEL_ICON_GAP = 4
LABEL_PADDING_RIGHT = 10

DEFAULT_SUBNET_MIN_WIDTH = 120
DEFAULT_SUBNET_HEIGHT = 50
DEFAULT_COL_GAP = 10
DEFAULT_ROW_GAP = 15
DEFAULT_VPC_PADDING_TOP = 50
DEFAULT_VPC_PADDING_SIDES = 15
DEFAULT_VPC_PADDING_BOTTOM = 15
DEFAULT_VPC_GAP = 25

register_legend("container", "VPC", "AWS-Group-light.svg:virtual-private-network-vpc.svg", "VPCs", border_key="border_vpc")
register_legend("container", "Public Subnet", "AWS-Group-light.svg:public-subnet.svg", "Subnets", border_key="border_subnet_public")
register_legend("container", "Private Subnet", "AWS-Group-light.svg:private-subnet.svg", "Subnets", border_key="border_subnet_private")


def _subnet_role_key(subnet):
    """Extract a role key from a subnet for cross-AZ alignment.

    Strips AZ-specific suffixes from the subnet name so that matching subnets
    across AZs produce the same key. Falls back to CIDR for unnamed subnets.
    """
    name = subnet.get("name", "")
    az = subnet.get("az", "")

    # No name tag — fall back to CIDR
    if not name or name.startswith("subnet-"):
        return subnet.get("cidr", name)

    # Strip the CIDR suffix that _get_name appends: " (10.0.0.0/24)"
    role = re.sub(r'\s*\([^)]*\)\s*$', '', name)

    # Try stripping full AZ name from end (e.g., "-us-west-2a", "_us-east-2b")
    if az and role.endswith(az):
        role = role[:-len(az)].rstrip('-_. ')
        if role:
            return role

    # Strip common AZ suffix patterns:
    # _az1, _az2, -az1, .az1
    stripped = re.sub(r'[._-]az[0-9]+$', '', role)
    if stripped != role and stripped:
        return stripped

    # .1a, .1b, .2c (dotted single-char AZ suffix)
    stripped = re.sub(r'[._-][0-9][a-z]$', '', role)
    if stripped != role and stripped:
        return stripped

    # Region suffix: -us-west-2a, -eu-west-1b, etc.
    stripped = re.sub(r'[._-][a-z]{2}-[a-z]+-[0-9]+[a-z]$', '', role)
    if stripped != role and stripped:
        return stripped

    return role


def _subnet_sort_key(subnet):
    """Sort key for subnets: public first, private middle, datastore/db last.

    Returns a tuple (tier, role) for stable sorting.
    """
    role = _subnet_role_key(subnet)
    role_lower = role.lower()

    if "public" in role_lower:
        tier = 0
    elif any(kw in role_lower for kw in ("datastore", "data", "db", "storage")):
        tier = 2
    else:
        tier = 1  # private, eks, backend, etc.

    return (tier, role)


def _label_width(name):
    """Compute required cell width for a label with icon."""
    text_w = estimate_text_width(name, FONT_SIZE_PX)
    return ICON_PADDING + ICON_SIZE + LABEL_ICON_GAP + text_w + LABEL_PADDING_RIGHT


def aws_rect(inkdoc, xy, wh, color, name, symid, layer, config=None):
    rect = Rectangle.new(xy[0], xy[1], wh[0], wh[1])
    rect.style = {"fill": "none", "stroke-width": 0.5, "stroke": color}
    layer.append(rect)

    # Icon top-left of rect
    icon_el = inkdoc.make_symbol_instance(symid, layer)
    icon_x = xy[0] + ICON_PADDING
    icon_y = xy[1] + ICON_PADDING
    tr = Transform(f'translate({icon_x}, {icon_y}) scale({ICON_SCALE})')
    icon_el.transform = tr

    # Label right of icon, baseline vertically centered on icon
    text_x = icon_x + ICON_SIZE + LABEL_ICON_GAP
    font_height = get_font_height(FONT_SIZE_PX)
    text_y = icon_y + (ICON_SIZE + font_height) / 2
    text_color = get_text_color(config)
    elem = TextElement(x=str(text_x), y=str(text_y))
    elem.text = str(name)
    elem.style = {
        'font-family': "'DejaVu Sans', sans-serif",
        'font-size': f'{FONT_SIZE_PX}px',
        'fill': text_color,
        'fill-opacity': '1.0',
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal'}

    layer.append(elem)


def render_vpc_with_subnets(inkdoc, vpc, vpc_subnets, stack, config=None, instances=None, load_balancers=None, db_instances=None, eks_clusters=None, vpc_lambdas=None, nat_gateways=None, private_r53_zones=None, auto_scaling_groups=None):
    """Render a VPC with its subnets in canonical AWS layout."""
    instances = instances or []
    load_balancers = load_balancers or []
    db_instances = db_instances or []
    eks_clusters = eks_clusters or []
    vpc_lambdas = vpc_lambdas or []
    nat_gateways = nat_gateways or []
    private_r53_zones = private_r53_zones or []
    auto_scaling_groups = auto_scaling_groups or []
    layout = (config or {}).get("layout", {})
    vpc_cfg = layout.get("vpc", {})
    vpc_pad = vpc_cfg.get("padding", {})
    subnet_cfg = layout.get("subnet", {})

    az_cfg = layout.get("availability_zone", {})
    az_enabled = az_cfg["enabled"]
    az_pad_sides = az_cfg.get("padding", {})["sides"]
    az_pad_top = az_cfg.get("padding", {})["top"]

    pad_top = vpc_pad["top"]
    pad_right = vpc_pad["right"]
    pad_bottom = vpc_pad["bottom"]
    pad_left = vpc_pad["left"]
    base_col_gap = subnet_cfg["col_gap"]
    row_gap = subnet_cfg["row_gap"]
    subnet_min_width = subnet_cfg["min_width"]
    subnet_min_height = subnet_cfg["height"]

    # Widen col_gap, pad_top and pad_bottom to accommodate AZ rects when enabled
    if az_enabled:
        az_pad_bottom = az_cfg.get("padding", {})["bottom"]
        col_gap = az_pad_sides * 2 + base_col_gap
        pad_top = pad_top + az_pad_top
        pad_bottom = az_pad_bottom + pad_bottom
    else:
        col_gap = base_col_gap

    # Add LB zone height to pad_top when load balancers are present
    lb_zone_h = resource_lb.zone_height(len(load_balancers), config)
    pad_top += lb_zone_h

    # Add EKS zone height to pad_top when EKS clusters are present
    eks_zone_h = resource_eks.zone_height(len(eks_clusters), config)
    pad_top += eks_zone_h

    # Add Lambda zone height to pad_top when VPC Lambdas are present
    lambda_zone_h = resource_lambda.zone_height(len(vpc_lambdas), config)
    pad_top += lambda_zone_h

    # Add private R53 zone height to pad_top
    r53_zone_h = resource_route53.private_zone_height(len(private_r53_zones), config)
    pad_top += r53_zone_h

    vpc_layer = get_or_create_layer(inkdoc, "VPCs")
    subnet_layer = get_or_create_layer(inkdoc, "Subnets")
    ec2_layer = get_or_create_layer(inkdoc, "EC2")
    lb_layer = get_or_create_layer(inkdoc, "Load Balancers")
    eks_layer = get_or_create_layer(inkdoc, "EKS")
    lambda_layer = get_or_create_layer(inkdoc, "Lambda")
    db_layer = get_or_create_layer(inkdoc, "Database")
    asg_layer = get_or_create_layer(inkdoc, "Auto Scaling Groups")
    nat_layer = get_or_create_layer(inkdoc, "NAT Gateways")

    azs = sorted(set(s["az"] for s in vpc_subnets))
    num_cols = max(len(azs), 1)

    # Build grid: columns = AZs, one row per subnet per AZ
    az_groups = {az: [] for az in azs}
    for subnet in vpc_subnets:
        az_groups[subnet["az"]].append(subnet)

    # Sort subnets within each AZ: public first, private middle, datastore last
    for az in azs:
        az_groups[az].sort(key=_subnet_sort_key)

    num_rows = max(len(subs) for subs in az_groups.values()) if az_groups else 1

    # Build a placement map: (row, col) → subnet
    placement = {}
    for col, az in enumerate(azs):
        for row, subnet in enumerate(az_groups[az]):
            placement[(row, col)] = subnet

    # Build instance map: subnet_id → [instances]
    instance_map = {}
    for inst in instances:
        sid = inst.get("subnet_id", "")
        if sid:
            instance_map.setdefault(sid, []).append(inst)

    # Build db instance map: subnet_id → [db_instances]
    db_map = {}
    for db_inst in db_instances:
        sid = db_inst.get("subnet_id", "")
        if sid:
            db_map.setdefault(sid, []).append(db_inst)

    # Build NAT gateway map: subnet_id → [nat_gateways]
    nat_map = {}
    for nat_gw in nat_gateways:
        sid = nat_gw.get("subnet_id", "")
        if sid:
            nat_map.setdefault(sid, []).append(nat_gw)

    # Build instance_id → asg_name mapping and asg_name → asg data lookup
    instance_to_asg = {}
    asg_lookup = {}
    for asg in auto_scaling_groups:
        asg_name = asg.get("name", "")
        asg_lookup[asg_name] = asg
        for iid in asg.get("instance_ids", []):
            instance_to_asg[iid] = asg_name

    # Subnet label height (icon + padding)
    subnet_label_height = ICON_SIZE + ICON_PADDING * 2

    # Compute per-row heights based on max resource count in each row
    # ASG bands are consistent across all columns in a row, so compute
    # the cross-column ASG band total per row first.
    ec2_card_gap_cfg = layout.get("ec2", {})["card_gap"]
    ch_cfg = resource_ec2.card_height(config)
    asg_oh_cfg = resource_asg.container_overhead(config)
    asg_pad_cfg = resource_asg._get_cfg(config)["padding"]

    row_heights = []
    for row in range(num_rows):
        # Compute cross-column ASG band height for this row
        # (non-ASG cards height + all ASG bands that have instances in any column)
        max_non_asg_in_row = 0
        for col in range(num_cols):
            subnet = placement.get((row, col))
            if subnet:
                sid = subnet.get("subnet_id", "")
                n = sum(1 for i in instance_map.get(sid, []) if i.get("instance_id", "") not in instance_to_asg)
                max_non_asg_in_row = max(max_non_asg_in_row, n)

        non_asg_band_h = resource_ec2.cards_height(max_non_asg_in_row, config) if max_non_asg_in_row > 0 else 0

        row_asg_band_h = 0
        for asg_name in sorted(set(instance_to_asg.values())):
            max_asg_count = 0
            for col in range(num_cols):
                subnet = placement.get((row, col))
                if subnet:
                    sid = subnet.get("subnet_id", "")
                    n = sum(1 for i in instance_map.get(sid, []) if instance_to_asg.get(i.get("instance_id", "")) == asg_name)
                    max_asg_count = max(max_asg_count, n)
            if max_asg_count > 0:
                asg_cards_h = max_asg_count * ch_cfg + max(0, max_asg_count - 1) * ec2_card_gap_cfg
                row_asg_band_h += asg_oh_cfg + asg_cards_h + asg_pad_cfg

        # The EC2+ASG zone height for this row (consistent across all columns)
        # Add bottom margin after the last ASG band so it doesn't touch the subnet edge
        if row_asg_band_h > 0:
            row_asg_band_h += asg_pad_cfg
        ec2_zone_h = non_asg_band_h + row_asg_band_h

        max_h = subnet_min_height
        for col in range(num_cols):
            subnet = placement.get((row, col))
            if subnet:
                sid = subnet.get("subnet_id", "")
                n_db = len(db_map.get(sid, []))
                n_nat = len(nat_map.get(sid, []))
                has_ec2 = len(instance_map.get(sid, [])) > 0
                has_content = has_ec2 or n_db > 0 or n_nat > 0
                if has_content:
                    needed = subnet_label_height + ec2_zone_h
                    if n_db > 0:
                        needed += resource_db.cards_height(n_db, config)
                    if n_nat > 0:
                        needed += resource_nat.cards_height(n_nat, config)
                    max_h = max(max_h, needed)
                # Even if this subnet has no content, the row needs to be tall enough
                # for the EC2+ASG zone if other columns have EC2 content
                elif ec2_zone_h > 0:
                    max_h = max(max_h, subnet_label_height + ec2_zone_h)
        row_heights.append(max_h)

    # Compute per-column widths based on widest content in each AZ
    col_widths = []
    for az in azs:
        az_subs = az_groups[az]
        if az_subs:
            widest = max(_label_width(s.get("name", "")) for s in az_subs)
            # Check ASG labels for instances in this AZ's subnets
            seen_asgs = set()
            for s in az_subs:
                sid = s.get("subnet_id", "")
                for inst in instance_map.get(sid, []):
                    asg_name = instance_to_asg.get(inst.get("instance_id", ""))
                    if asg_name and asg_name not in seen_asgs:
                        seen_asgs.add(asg_name)
                        widest = max(widest, resource_asg.label_width(asg_name, config))
                # Also consider EC2 instance card widths
                ec2_layout = layout.get("ec2", {})
                ec2_font = ec2_layout["font_size"]
                ec2_icon_w = 40 * ec2_layout["icon_scale"]
                for inst in instance_map.get(sid, []):
                    name_w = estimate_text_width(inst.get("name", ""), ec2_font)
                    type_w = estimate_text_width(inst.get("instance_type", ""), ec2_font)
                    card_w = ec2_icon_w + max(name_w, type_w) + 10
                    widest = max(widest, card_w)
                # Also consider DB instance card widths
                db_layout = layout.get("database", {})
                db_font = db_layout["font_size"]
                db_icon_w = 40 * db_layout["icon_scale"]
                for db in db_map.get(sid, []):
                    db_name_w = estimate_text_width(db.get("name", ""), db_font)
                    db_card_w = db_icon_w + db_name_w + 10
                    widest = max(widest, db_card_w)
            col_widths.append(max(subnet_min_width, widest))
        else:
            col_widths.append(subnet_min_width)

    # Also consider VPC label width for minimum total
    vpc_name = vpc.get("name", "vpc")
    vpc_label_w = _label_width(vpc_name)

    # Create grid
    vpc_x, vpc_y = stack.next_position()
    grid = Grid(
        origin_x=vpc_x, origin_y=vpc_y,
        col_widths=col_widths, row_heights=row_heights,
        col_gap=col_gap, row_gap=row_gap,
        padding_top=pad_top, padding_right=pad_right,
        padding_bottom=pad_bottom, padding_left=pad_left,
    )

    vpc_width, vpc_height = grid.bounds(num_rows, num_cols)

    # Ensure VPC is at least wide enough for its own label
    vpc_width = max(vpc_width, vpc_label_w + pad_left + pad_right)

    # Draw VPC rectangle to VPC layer
    aws_rect(inkdoc, [vpc_x, vpc_y], [vpc_width, vpc_height],
             get_border_color(config, "vpc"), vpc_name,
             "AWS-Group-light.svg:virtual-private-network-vpc.svg", vpc_layer, config)

    # Build subnet_id → column mapping for LB rendering
    subnet_to_col = {}
    for (row, col), subnet in placement.items():
        sid = subnet.get("subnet_id", "")
        if sid and sid not in subnet_to_col:
            subnet_to_col[sid] = col

    # Draw load balancers and EKS clusters in the pre-grid zone
    first_cell_y = grid.cell_position(0, 0)[1]
    az_overhead = az_pad_top if az_enabled else 0
    pre_grid_y = first_cell_y - az_overhead

    if load_balancers and subnet_to_col:
        lb_zone_y = pre_grid_y - r53_zone_h - lambda_zone_h - eks_zone_h - lb_zone_h
        resource_lb.render_lb_zone(inkdoc, load_balancers, lb_zone_y, grid, subnet_to_col, lb_layer, config)

    if eks_clusters and subnet_to_col:
        eks_zone_y = pre_grid_y - r53_zone_h - lambda_zone_h - eks_zone_h
        resource_eks.render_eks_zone(inkdoc, eks_clusters, eks_zone_y, grid, subnet_to_col, eks_layer, config)

    if vpc_lambdas and subnet_to_col:
        lambda_zone_y = pre_grid_y - r53_zone_h - lambda_zone_h
        resource_lambda.render_lambda_zone(inkdoc, vpc_lambdas, lambda_zone_y, grid, subnet_to_col, lambda_layer, config)

    if private_r53_zones:
        r53_layer = get_or_create_layer(inkdoc, "Route 53 Private")
        r53_zone_y = pre_grid_y - r53_zone_h
        resource_route53.render_private_zones(inkdoc, private_r53_zones, r53_zone_y, grid, r53_layer, config)

    # Draw AZ columns if enabled
    if az_enabled:
        resource_az.render_az_columns(inkdoc, vpc_x, vpc_y, grid, azs, num_rows, config)

    # Draw subnets and EC2 instances
    for (row, col), subnet in placement.items():
        sx, sy = grid.cell_position(row, col)
        subnet_name = subnet.get("name", "subnet")
        cell_w = grid.col_width(col)
        cell_h = grid.row_height(row)

        if subnet["is_public"]:
            aws_rect(inkdoc, [sx, sy], [cell_w, cell_h],
                     get_border_color(config, "subnet_public"),
                     subnet_name, "AWS-Group-light.svg:public-subnet.svg", subnet_layer, config)
        else:
            aws_rect(inkdoc, [sx, sy], [cell_w, cell_h],
                     get_border_color(config, "subnet_private"),
                     subnet_name, "AWS-Group-light.svg:private-subnet.svg", subnet_layer, config)

        # Render EC2 instances inside this subnet using ASG band positioning
        # Non-ASG instances render first, then each ASG's instances at the global band offset
        sid = subnet.get("subnet_id", "")
        subnet_instances = instance_map.get(sid, [])
        ec2_offset = subnet_label_height
        if subnet_instances:
            ec2_card_top = layout.get("ec2", {})["card_top"]
            ec2_card_gap = layout.get("ec2", {})["card_gap"]
            ch = resource_ec2.card_height(config)
            asg_oh = resource_asg.container_overhead(config)

            # Separate non-ASG and ASG instances
            non_asg_insts = [i for i in subnet_instances if i.get("instance_id", "") not in instance_to_asg]

            # Render non-ASG instances at the top
            cursor_y = sy + subnet_label_height + ec2_card_top
            for inst in non_asg_insts:
                resource_ec2.render_instance(inkdoc, inst, sx, cursor_y, cell_w, ec2_layer, config)
                cursor_y += ch + ec2_card_gap

            # Compute base y for ASG bands (after non-ASG instances)
            max_non_asg = 0
            for (r2, c2), s2 in placement.items():
                if r2 != row:
                    continue
                s2id = s2.get("subnet_id", "")
                n = sum(1 for i in instance_map.get(s2id, []) if i.get("instance_id", "") not in instance_to_asg)
                max_non_asg = max(max_non_asg, n)

            non_asg_band_h = resource_ec2.cards_height(max_non_asg, config) if max_non_asg > 0 else 0
            asg_bands_y = sy + subnet_label_height + non_asg_band_h

            # Render each ASG's instances at the global band offset
            band_cursor = asg_bands_y
            for asg_name in sorted(set(instance_to_asg.values())):
                asg_insts_here = [i for i in subnet_instances if instance_to_asg.get(i.get("instance_id", "")) == asg_name]
                # Find max instance count for this ASG across all columns in this row
                max_asg_count = 0
                for (r2, c2), s2 in placement.items():
                    if r2 != row:
                        continue
                    s2id = s2.get("subnet_id", "")
                    n = sum(1 for i in instance_map.get(s2id, []) if instance_to_asg.get(i.get("instance_id", "")) == asg_name)
                    max_asg_count = max(max_asg_count, n)

                if max_asg_count == 0:
                    continue

                # Render this ASG's instances at band_cursor + asg_oh (after label space)
                card_y = band_cursor + asg_oh
                for inst in asg_insts_here:
                    resource_ec2.render_instance(inkdoc, inst, sx, card_y, cell_w, ec2_layer, config)
                    card_y += ch + ec2_card_gap

                # Advance band cursor by overhead + max cards for this ASG
                asg_cards_h = max_asg_count * ch + max(0, max_asg_count - 1) * ec2_card_gap
                band_cursor += asg_oh + asg_cards_h + resource_asg._get_cfg(config)["padding"]

            # ec2_offset for DB placement: use the band cursor position (accounts for
            # cross-column ASG bands) so DB cards start below all ASG bands in this row
            ec2_offset = band_cursor - sy

        # Render database instances below EC2 cards
        subnet_dbs = db_map.get(sid, [])
        db_offset = ec2_offset
        if subnet_dbs:
            resource_db.render_instances_in_subnet(
                inkdoc, subnet_dbs, sx, sy, cell_w,
                ec2_offset, db_layer, config)
            db_offset = ec2_offset + resource_db.cards_height(len(subnet_dbs), config)

        # Render NAT gateways below database cards
        subnet_nats = nat_map.get(sid, [])
        if subnet_nats:
            resource_nat.render_in_subnet(
                inkdoc, subnet_nats, sx, sy, cell_w,
                db_offset, nat_layer, config)

    # Render ASG spanning rectangles across columns
    if auto_scaling_groups and subnet_to_col:
        resource_asg.render_asg_spanning(
            inkdoc, auto_scaling_groups, instance_to_asg, asg_lookup,
            instance_map, placement, grid, subnet_to_col,
            subnet_label_height, asg_layer, config)

    stack.track_width(vpc_width)
    stack.advance(vpc_height)
