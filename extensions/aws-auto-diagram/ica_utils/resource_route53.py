from inkex.elements import TextElement
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.layers import get_or_create_layer
from ica_utils.theme import get_text_color, get_text_dimmed_opacity
from ica_utils.legend import register_legend

SYMBOL_FILE = "AWS-Resource-networking-content-delivery-light.svg"
R53_SYMBOL = f"{SYMBOL_FILE}:res-amazon-route-53-hosted-zone"

ICON_BASE_SIZE = 40

DEFAULT_ICON_SCALE = 0.5
DEFAULT_FONT_SIZE = 13
DEFAULT_CARD_GAP = 6
DEFAULT_CARD_PADDING = 4
DEFAULT_CARD_HEIGHT = 30

register_legend("resource", "Route 53", "AWS-Resource-networking-content-delivery-light.svg:res-amazon-route-53-hosted-zone", "Edge")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("route53", {})


def _card_width(label, config=None):
    cfg = _get_cfg(config)
    icon_scale = cfg.get("icon_scale", DEFAULT_ICON_SCALE)
    font_size = cfg.get("font_size", DEFAULT_FONT_SIZE)
    card_padding = cfg.get("card_padding", DEFAULT_CARD_PADDING)
    icon_w = ICON_BASE_SIZE * icon_scale
    text_w = estimate_text_width(label, font_size)
    return icon_w + card_padding + text_w


def render_public_zones(inkdoc, zones, x, y, config=None):
    """Render public Route 53 hosted zones stacked vertically.

    Returns (total_width, total_height).
    """
    if not zones:
        return (0, 0)

    cfg = _get_cfg(config)
    icon_scale = cfg.get("icon_scale", DEFAULT_ICON_SCALE)
    font_size = cfg.get("font_size", DEFAULT_FONT_SIZE)
    card_gap = cfg.get("card_gap", DEFAULT_CARD_GAP)
    card_padding = cfg.get("card_padding", DEFAULT_CARD_PADDING)

    layer = get_or_create_layer(inkdoc, "Edge")

    icon_h = ICON_BASE_SIZE * icon_scale
    icon_w = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)

    cursor_y = y
    max_width = 0

    for zone in zones:
        name = zone.get("name", "")
        record_count = zone.get("record_count", 0)
        label = f"{name} ({record_count} records)"

        # Icon
        icon_el = inkdoc.make_symbol_instance(R53_SYMBOL, layer)
        tr = Transform(f'translate({x}, {cursor_y}) scale({icon_scale})')
        icon_el.transform = tr

        # Label to the right of icon
        text_x = x + icon_w + card_padding
        text_y = cursor_y + (icon_h + font_h) / 2
        text_el = TextElement(x=str(text_x), y=str(text_y))
        text_el.text = label
        text_el.style = {
            'font-family': "'DejaVu Sans', sans-serif",
            'font-size': f'{font_size}px',
            'fill': get_text_color(config),
            'fill-opacity': '1.0',
            'stroke': 'none',
            'font-weight': 'normal',
            'font-style': 'normal',
        }
        layer.append(text_el)

        w = _card_width(label, config)
        if w > max_width:
            max_width = w

        cursor_y += icon_h + card_gap

    total_height = cursor_y - y - card_gap
    return (max_width, total_height)


def private_zone_height(zone_count, config=None):
    """Total height needed for the private R53 zone in the VPC pre-grid area."""
    if zone_count == 0:
        return 0
    cfg = _get_cfg(config)
    card_h = cfg.get("card_height", DEFAULT_CARD_HEIGHT)
    card_gap = cfg.get("card_gap", DEFAULT_CARD_GAP)
    return zone_count * card_h + max(0, zone_count - 1) * card_gap + card_gap


def render_private_zone(inkdoc, zone, y, grid, layer, config=None):
    """Render a single private R53 zone as a spanning element across all columns.

    Returns card height used.
    """
    cfg = _get_cfg(config)
    icon_scale = cfg.get("icon_scale", DEFAULT_ICON_SCALE)
    font_size = cfg.get("font_size", DEFAULT_FONT_SIZE)
    card_h = cfg.get("card_height", DEFAULT_CARD_HEIGHT)

    font_h = get_font_height(font_size)

    # Span across all columns
    first_x, _ = grid.cell_position(0, 0)

    # Icon
    icon_el = inkdoc.make_symbol_instance(R53_SYMBOL, layer)
    tr = Transform(f'translate({first_x}, {y}) scale({icon_scale})')
    icon_el.transform = tr

    # Name right of icon
    name = zone.get("name", "")
    record_count = zone.get("record_count", 0)
    label = f"{name} ({record_count} records)"

    text_x = first_x + ICON_BASE_SIZE * icon_scale + 4
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

    # "Private" label below name (dimmed)
    priv_y = text_y + font_h
    priv_el = TextElement(x=str(text_x), y=str(priv_y))
    priv_el.text = "private zone"
    priv_el.style = {
        'font-family': "'DejaVu Sans', sans-serif",
        'font-size': f'{font_size}px',
        'fill': get_text_color(config),
        'fill-opacity': str(get_text_dimmed_opacity(config)),
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal',
    }
    layer.append(priv_el)

    return card_h


def render_private_zones(inkdoc, zones, zone_y, grid, layer, config=None):
    """Render all private R53 zones in the VPC pre-grid zone."""
    cfg = _get_cfg(config)
    card_gap = cfg.get("card_gap", DEFAULT_CARD_GAP)

    cursor_y = zone_y
    for zone in zones:
        h = render_private_zone(inkdoc, zone, cursor_y, grid, layer, config)
        if h > 0:
            cursor_y += h + card_gap
