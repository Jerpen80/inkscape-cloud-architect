from inkex.elements import TextElement
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.layers import get_or_create_layer
from ica_utils.theme import get_text_color
from ica_utils.legend import register_legend

DDB_SYMBOL = "AWS-Resource-database-light.svg:res-amazon-dynamodb-table"

DEFAULT_ICON_SCALE = 0.5
DEFAULT_FONT_SIZE = 13
DEFAULT_CARD_GAP = 6
DEFAULT_CARD_PADDING = 4

ICON_BASE_SIZE = 40

register_legend("resource", "DynamoDB", "AWS-Resource-database-light.svg:res-amazon-dynamodb-table", "DynamoDB")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("dynamodb", {})


def _card_height(config=None):
    """Height of a single DynamoDB table card."""
    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    return ICON_BASE_SIZE * icon_scale


def _card_width(name, config=None):
    """Width of a single DynamoDB table card (icon + gap + name text)."""
    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]
    card_padding = cfg["card_padding"]

    icon_w = ICON_BASE_SIZE * icon_scale
    text_w = estimate_text_width(name, font_size)
    return icon_w + card_padding + text_w


def render_tables(inkdoc, tables, x, y, config=None):
    """Render DynamoDB table cards stacked vertically at (x, y).

    Returns (total_width, total_height) of the rendered block.
    """
    if not tables:
        return (0, 0)

    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]
    card_gap = cfg["card_gap"]
    card_padding = cfg["card_padding"]

    ddb_layer = get_or_create_layer(inkdoc, "DynamoDB")

    icon_h = ICON_BASE_SIZE * icon_scale
    icon_w = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)

    cursor_y = y
    max_width = 0

    for table in tables:
        name = table.get("name", "")

        # Icon
        icon_el = inkdoc.make_symbol_instance(DDB_SYMBOL, ddb_layer)
        tr = Transform(f'translate({x}, {cursor_y}) scale({icon_scale})')
        icon_el.transform = tr

        # Name to the right of icon, vertically centered
        text_x = x + icon_w + card_padding
        text_y = cursor_y + (icon_h + font_h) / 2
        text_el = TextElement(x=str(text_x), y=str(text_y))
        text_el.text = name
        text_el.style = {
            'font-family': "'DejaVu Sans', sans-serif",
            'font-size': f'{font_size}px',
            'fill': get_text_color(config),
            'fill-opacity': '1.0',
            'stroke': 'none',
            'font-weight': 'normal',
            'font-style': 'normal',
        }
        ddb_layer.append(text_el)

        w = _card_width(name, config)
        if w > max_width:
            max_width = w

        cursor_y += icon_h + card_gap

    total_height = cursor_y - y - card_gap
    return (max_width, total_height)
