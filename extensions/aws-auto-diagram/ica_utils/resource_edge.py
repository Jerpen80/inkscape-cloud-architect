from inkex.elements import Rectangle, TextElement
from inkex import Transform
from ica_utils.layers import get_or_create_layer
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils import resource_route53
from ica_utils import resource_cloudfront
from ica_utils.theme import get_text_color, get_border_color
from ica_utils.legend import register_legend

ICON_SIZE = 40
ICON_PADDING = 2
LABEL_ICON_GAP = 4
FONT_SIZE_PX = 17

DEFAULT_PADDING_TOP = 50
DEFAULT_PADDING_RIGHT = 20
DEFAULT_PADDING_BOTTOM = 15
DEFAULT_PADDING_LEFT = 15
DEFAULT_COLUMN_GAP = 40
DEFAULT_BOTTOM_SPACING = 20

register_legend("container", "Edge", None, "Edge", border_key="border_edge")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("edge", {})


def render_edge_zone(inkdoc, route53_public_zones, cloudfront_distributions, x, y, config=None):
    """Render the Edge zone with R53 zones on the left and CF distributions on the right.

    Returns (total_width, total_height) of the Edge zone including padding.
    """
    if not route53_public_zones and not cloudfront_distributions:
        return (0, 0)

    cfg = _get_cfg(config)
    pad_top = cfg.get("padding", {}).get("top", DEFAULT_PADDING_TOP)
    pad_right = cfg.get("padding", {}).get("right", DEFAULT_PADDING_RIGHT)
    pad_bottom = cfg.get("padding", {}).get("bottom", DEFAULT_PADDING_BOTTOM)
    pad_left = cfg.get("padding", {}).get("left", DEFAULT_PADDING_LEFT)
    column_gap = cfg.get("column_gap", DEFAULT_COLUMN_GAP)

    edge_layer = get_or_create_layer(inkdoc, "Edge")

    content_x = x + pad_left
    content_y = y + pad_top

    r53_w, r53_h = 0, 0
    cf_w, cf_h = 0, 0

    # Render R53 zones on the left
    if route53_public_zones:
        r53_w, r53_h = resource_route53.render_public_zones(
            inkdoc, route53_public_zones, content_x, content_y, config)

    # Render CF distributions on the right
    if cloudfront_distributions:
        cf_x = content_x + (r53_w + column_gap if r53_w > 0 else 0)
        cf_w, cf_h = resource_cloudfront.render_distributions(
            inkdoc, cloudfront_distributions, cf_x, content_y, config)

    # Compute total dimensions
    content_w = r53_w + (column_gap if r53_w > 0 and cf_w > 0 else 0) + cf_w
    content_h = max(r53_h, cf_h)

    zone_w = pad_left + content_w + pad_right
    zone_h = pad_top + content_h + pad_bottom

    # Draw Edge zone rect
    rect = Rectangle.new(x, y, zone_w, zone_h)
    rect.style = {"fill": "none", "stroke-width": 0.5, "stroke": get_border_color(config, "edge")}
    edge_layer.append(rect)

    # Edge label
    text_color = get_text_color(config)
    font_h = get_font_height(FONT_SIZE_PX)
    label_x = x + ICON_PADDING + ICON_SIZE + LABEL_ICON_GAP
    label_y = y + ICON_PADDING + (ICON_SIZE + font_h) / 2
    label_el = TextElement(x=str(label_x), y=str(label_y))
    label_el.text = "Edge"
    label_el.style = {
        'font-family': "'DejaVu Sans', sans-serif",
        'font-size': f'{FONT_SIZE_PX}px',
        'fill': text_color,
        'fill-opacity': '1.0',
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal',
    }
    edge_layer.append(label_el)

    return (zone_w, zone_h)


def get_bottom_spacing(config=None):
    """Get the spacing below the Edge zone before regions."""
    cfg = _get_cfg(config)
    return cfg.get("bottom_spacing", DEFAULT_BOTTOM_SPACING)
