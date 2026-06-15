from inkex.elements import TextElement
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.layers import get_or_create_layer
from ica_utils.theme import get_text_color, get_text_dimmed_opacity
from ica_utils.legend import register_legend

SYMBOL_FILE = "AWS-Resource-networking-content-delivery-light.svg"
CF_SYMBOL = f"{SYMBOL_FILE}:res-amazon-cloudfront-download-distribution"

ICON_BASE_SIZE = 40

DEFAULT_ICON_SCALE = 0.5
DEFAULT_FONT_SIZE = 13
DEFAULT_CARD_GAP = 6
DEFAULT_CARD_PADDING = 4

register_legend("resource", "CloudFront", "AWS-Resource-networking-content-delivery-light.svg:res-amazon-cloudfront-download-distribution", "Edge")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("cloudfront", {})


def _card_width(name, subtitle, config=None):
    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]
    card_padding = cfg["card_padding"]
    icon_w = ICON_BASE_SIZE * icon_scale
    name_w = estimate_text_width(name, font_size)
    sub_w = estimate_text_width(subtitle, font_size)
    text_w = max(name_w, sub_w)
    return icon_w + card_padding + text_w


def render_distributions(inkdoc, distributions, x, y, config=None):
    """Render CloudFront distributions stacked vertically.

    Returns (total_width, total_height).
    """
    if not distributions:
        return (0, 0)

    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]
    card_gap = cfg["card_gap"]
    card_padding = cfg["card_padding"]

    layer = get_or_create_layer(inkdoc, "Edge")

    icon_h = ICON_BASE_SIZE * icon_scale
    icon_w = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)

    cursor_y = y
    max_width = 0

    for dist in distributions:
        comment = dist.get("comment", "")
        aliases = dist.get("aliases", [])
        dist_id = dist.get("distribution_id", "")

        # Name: prefer comment, fallback to first alias, fallback to domain
        if comment:
            name = comment
        elif aliases:
            name = aliases[0]
        else:
            name = dist.get("domain_name", dist_id)

        # Icon
        icon_el = inkdoc.make_symbol_instance(CF_SYMBOL, layer)
        tr = Transform(f'translate({x}, {cursor_y}) scale({icon_scale})')
        icon_el.transform = tr

        # Name to the right of icon
        text_x = x + icon_w + card_padding
        text_y = cursor_y + font_h
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

        # Distribution ID below name (dimmed)
        sub_y = text_y + font_h
        sub_el = TextElement(x=str(text_x), y=str(sub_y))
        sub_el.text = dist_id
        sub_el.style = {
            'font-family': "'DejaVu Sans', sans-serif",
            'font-size': f'{font_size}px',
            'fill': get_text_color(config),
            'fill-opacity': str(get_text_dimmed_opacity(config)),
            'stroke': 'none',
            'font-weight': 'normal',
            'font-style': 'normal',
        }
        layer.append(sub_el)

        w = _card_width(name, dist_id, config)
        if w > max_width:
            max_width = w

        cursor_y += icon_h + card_gap

    total_height = cursor_y - y - card_gap
    return (max_width, total_height)
