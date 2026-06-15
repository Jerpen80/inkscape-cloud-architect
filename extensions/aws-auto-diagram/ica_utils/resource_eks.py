from inkex.elements import TextElement, PathElement
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.theme import get_text_color, get_text_dimmed_opacity
from ica_utils.legend import register_legend

SYMBOL_FILE = "AWS-Service-containers.svg"
EKS_SYMBOL = f"{SYMBOL_FILE}:arch-amazon-eks-cloud"

ICON_BASE_SIZE = 40

DEFAULT_ICON_SCALE = 0.5
DEFAULT_FONT_SIZE = 13
DEFAULT_CARD_HEIGHT = 30
DEFAULT_CARD_GAP = 8

register_legend("resource", "EKS", "AWS-Service-containers.svg:arch-amazon-eks-cloud", "EKS")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("eks", {})


def zone_height(cluster_count, config=None):
    """Total height needed for the EKS zone above the subnet grid."""
    if cluster_count == 0:
        return 0
    cfg = _get_cfg(config)
    card_h = cfg["card_height"]
    card_gap = cfg["card_gap"]
    return cluster_count * card_h + max(0, cluster_count - 1) * card_gap + card_gap


def render_eks(inkdoc, cluster, y, grid, subnet_to_col, layer, config=None):
    """Render a single EKS cluster spanning its columns.

    Returns:
        Card height used
    """
    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]
    card_h = cfg["card_height"]
    span_color = cfg["span_line_color"]
    span_width = cfg["span_line_width"]
    span_dash = cfg["span_line_dasharray"]

    font_h = get_font_height(font_size)

    # Determine column span
    cols = [subnet_to_col[sid] for sid in cluster.get("subnet_ids", []) if sid in subnet_to_col]

    # Find leftmost position from grid for icon placement
    if cols:
        min_col = min(cols)
        max_col = max(cols)
        span_x_left, _ = grid.cell_position(0, min_col)
        span_x_right, _ = grid.cell_position(0, max_col)
        span_x_right += grid.col_width(max_col)
    else:
        # No matching subnets in grid — render at first column with no span line
        span_x_left, _ = grid.cell_position(0, 0)
        span_x_right = None

    # Icon left-aligned within span
    icon_x = span_x_left
    icon_y = y
    icon_el = inkdoc.make_symbol_instance(EKS_SYMBOL, layer)
    tr = Transform(f'translate({icon_x}, {icon_y}) scale({icon_scale})')
    icon_el.transform = tr

    # Name right of icon
    name = cluster.get("name", "")
    text_x = icon_x + ICON_BASE_SIZE * icon_scale + 4
    text_y = y + font_h
    name_el = TextElement(x=str(text_x), y=str(text_y))
    name_el.text = name
    name_el.style = {
        'font-family': "'DejaVu Sans', sans-serif",
        'font-size': f'{font_size}px',
        'fill': get_text_color(config),
        'fill-opacity': '1.0',
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal',
    }
    layer.append(name_el)

    # Version below name (dimmed)
    version = cluster.get("version", "")
    if version:
        version_label = f"v{version}"
        version_y = text_y + font_h
        version_el = TextElement(x=str(text_x), y=str(version_y))
        version_el.text = version_label
        version_el.style = {
            'font-family': "'DejaVu Sans', sans-serif",
            'font-size': f'{font_size}px',
            'fill': get_text_color(config),
            'fill-opacity': str(get_text_dimmed_opacity(config)),
            'stroke': 'none',
            'font-weight': 'normal',
            'font-style': 'normal',
        }
        layer.append(version_el)

    # Span line below the card
    if span_x_right is not None:
        line_y = y + card_h - 2
        line = PathElement()
        line.set('d', f'M {span_x_left},{line_y} L {span_x_right},{line_y}')
        line.style = {
            'stroke': span_color,
            'stroke-width': span_width,
            'stroke-dasharray': span_dash,
            'fill': 'none',
        }
        layer.append(line)

    return card_h


def render_eks_zone(inkdoc, eks_clusters, zone_y, grid, subnet_to_col, layer, config=None):
    """Render all EKS clusters in the pre-grid zone."""
    cfg = _get_cfg(config)
    card_gap = cfg["card_gap"]

    cursor_y = zone_y
    for cluster in eks_clusters:
        h = render_eks(inkdoc, cluster, cursor_y, grid, subnet_to_col, layer, config)
        if h > 0:
            cursor_y += h + card_gap
