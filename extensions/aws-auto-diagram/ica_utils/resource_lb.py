from inkex.elements import TextElement, PathElement
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.theme import get_text_color, get_text_dimmed_opacity
from ica_utils.legend import register_legend

SYMBOL_FILE = "AWS-Resource-networking-content-delivery-light.svg"
ALB_SYMBOL = f"{SYMBOL_FILE}:res-elastic-load-balancing-application-load-balancer"
NLB_SYMBOL = f"{SYMBOL_FILE}:res-elastic-load-balancing-network-load-balancer"

ICON_BASE_SIZE = 40

DEFAULT_ICON_SCALE = 0.5
DEFAULT_FONT_SIZE = 13
DEFAULT_CARD_HEIGHT = 30
DEFAULT_CARD_GAP = 8

register_legend("resource", "Load Balancer", "AWS-Resource-networking-content-delivery-light.svg:res-elastic-load-balancing-application-load-balancer", "Load Balancers")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("load_balancer", {})


def _symbol_for_type(lb_type):
    if lb_type == "network":
        return NLB_SYMBOL
    return ALB_SYMBOL


def zone_height(lb_count, config=None):
    """Total height needed for the LB zone above the subnet grid."""
    if lb_count == 0:
        return 0
    cfg = _get_cfg(config)
    card_h = cfg.get("card_height", DEFAULT_CARD_HEIGHT)
    card_gap = cfg.get("card_gap", DEFAULT_CARD_GAP)
    return lb_count * card_h + max(0, lb_count - 1) * card_gap + card_gap  # trailing gap before subnets


def render_lb(inkdoc, lb, y, grid, subnet_to_col, layer, config=None):
    """Render a single load balancer spanning its columns.

    Args:
        inkdoc: Extension instance
        lb: Load balancer dict
        y: Y position for this LB card
        grid: The Grid used for subnet layout
        subnet_to_col: Dict mapping subnet_id → column index
        layer: SVG layer to render into
        config: Config dict

    Returns:
        Card height used
    """
    cfg = _get_cfg(config)
    icon_scale = cfg.get("icon_scale", DEFAULT_ICON_SCALE)
    font_size = cfg.get("font_size", DEFAULT_FONT_SIZE)
    card_h = cfg.get("card_height", DEFAULT_CARD_HEIGHT)
    span_color = cfg.get("span_line_color", "#ED7100")
    span_width = cfg.get("span_line_width", 1.0)
    span_dash = cfg.get("span_line_dasharray", "4,4")

    icon_h = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)

    # Determine column span
    cols = [subnet_to_col[sid] for sid in lb.get("subnet_ids", []) if sid in subnet_to_col]
    if not cols:
        return 0

    min_col = min(cols)
    max_col = max(cols)

    # X coordinates: left edge of min_col to right edge of max_col
    span_x_left, _ = grid.cell_position(0, min_col)
    span_x_right, _ = grid.cell_position(0, max_col)
    span_x_right += grid.col_width(max_col)

    # Icon left-aligned within span
    icon_x = span_x_left
    icon_y = y
    icon_el = inkdoc.make_symbol_instance(_symbol_for_type(lb.get("lb_type", "")), layer)
    tr = Transform(f'translate({icon_x}, {icon_y}) scale({icon_scale})')
    icon_el.transform = tr

    # Name right of icon
    name = lb.get("name", "")
    scheme = lb.get("scheme", "")
    lb_type = lb.get("lb_type", "")
    label = f"{name}"
    type_label = f"{lb_type} / {scheme}" if scheme else lb_type

    text_x = icon_x + ICON_BASE_SIZE * icon_scale + 4
    text_y = y + font_h
    name_el = TextElement(x=str(text_x), y=str(text_y))
    name_el.text = label
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

    # Type/scheme label below name
    type_y = text_y + font_h
    type_el = TextElement(x=str(text_x), y=str(type_y))
    type_el.text = type_label
    type_el.style = {
        'font-family': "'DejaVu Sans', sans-serif",
        'font-size': f'{font_size}px',
        'fill': get_text_color(config),
        'fill-opacity': str(get_text_dimmed_opacity(config)),
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal',
    }
    layer.append(type_el)

    # Span line below the card
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


def render_lb_zone(inkdoc, load_balancers, zone_y, grid, subnet_to_col, layer, config=None):
    """Render all load balancers in the pre-grid zone.

    Args:
        inkdoc: Extension instance
        load_balancers: List of LB dicts for this VPC
        zone_y: Y start of the LB zone
        grid: Grid for column positions
        subnet_to_col: Dict mapping subnet_id → column index
        layer: SVG layer
        config: Config dict
    """
    cfg = _get_cfg(config)
    card_gap = cfg.get("card_gap", DEFAULT_CARD_GAP)

    cursor_y = zone_y
    for lb in load_balancers:
        h = render_lb(inkdoc, lb, cursor_y, grid, subnet_to_col, layer, config)
        if h > 0:
            cursor_y += h + card_gap
