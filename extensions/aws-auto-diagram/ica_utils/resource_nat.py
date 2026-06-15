from inkex.elements import TextElement
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.theme import get_text_color, get_text_dimmed_opacity
from ica_utils.legend import register_legend

NAT_SYMBOL = "AWS-Resource-networking-content-delivery-light.svg:res-amazon-vpc-nat-gateway"

DEFAULT_ICON_SCALE = 0.5
DEFAULT_FONT_SIZE = 13
DEFAULT_CARD_GAP = 8
DEFAULT_CARD_TOP = 10

ICON_BASE_SIZE = 40

register_legend("resource", "NAT Gateway", "AWS-Resource-networking-content-delivery-light.svg:res-amazon-vpc-nat-gateway", "NAT Gateways")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("nat_gateway", {})


def card_height(config=None):
    """Height of a single NAT gateway card (icon + name)."""
    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]
    icon_h = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)
    return icon_h + font_h + 4


def cards_height(count, config=None):
    """Total height needed for N NAT gateway cards including gaps."""
    if count == 0:
        return 0
    cfg = _get_cfg(config)
    card_gap = cfg["card_gap"]
    card_top = cfg["card_top"]
    ch = card_height(config)
    return card_top + count * ch + max(0, count - 1) * card_gap


def render_instance(inkdoc, nat_gw, x, y, cell_width, layer, config=None):
    """Render a single NAT gateway card at (x, y), centered within cell_width."""
    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]

    icon_h = ICON_BASE_SIZE * icon_scale
    icon_w = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)

    # Icon centered horizontally
    icon_x = x + (cell_width - icon_w) / 2
    icon_y = y
    icon_el = inkdoc.make_symbol_instance(NAT_SYMBOL, layer)
    tr = Transform(f'translate({icon_x}, {icon_y}) scale({icon_scale})')
    icon_el.transform = tr

    # Name centered below icon
    name = nat_gw.get("name", "")
    name_w = estimate_text_width(name, font_size)
    name_x = x + (cell_width - name_w) / 2
    name_y = icon_y + icon_h + font_h
    name_el = TextElement(x=str(name_x), y=str(name_y))
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

    return card_height(config)


def render_in_subnet(inkdoc, nat_gateways, sx, sy, cell_width, offset_y, layer, config=None):
    """Render all NAT gateways stacked inside a subnet starting at offset_y below subnet top."""
    cfg = _get_cfg(config)
    card_gap = cfg["card_gap"]

    cursor_y = sy + offset_y
    for nat_gw in nat_gateways:
        ch = render_instance(inkdoc, nat_gw, sx, cursor_y, cell_width, layer, config)
        cursor_y += ch + card_gap
