from inkex.elements import TextElement, PathElement
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.layers import get_or_create_layer
from ica_utils.theme import get_text_color, get_text_dimmed_opacity
from ica_utils.legend import register_legend

LAMBDA_SYMBOL = "AWS-Resource-compute-light.svg:res-aws-lambda-lambda-function"

ICON_BASE_SIZE = 40

DEFAULT_ICON_SCALE = 0.5
DEFAULT_FONT_SIZE = 13
DEFAULT_CARD_HEIGHT = 30
DEFAULT_CARD_GAP = 8
DEFAULT_CARD_PADDING = 4

register_legend("resource", "Lambda", "AWS-Resource-compute-light.svg:res-aws-lambda-lambda-function", "Lambda")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("lambda_function", {})


def zone_height(lambda_count, config=None):
    """Total height needed for the Lambda zone above the subnet grid."""
    if lambda_count == 0:
        return 0
    cfg = _get_cfg(config)
    card_h = cfg["card_height"]
    card_gap = cfg["card_gap"]
    return lambda_count * card_h + max(0, lambda_count - 1) * card_gap + card_gap


def render_lambda_spanning(inkdoc, fn, y, grid, subnet_to_col, layer, config=None):
    """Render a single VPC Lambda as a spanning card.

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
    cols = [subnet_to_col[sid] for sid in fn.get("subnet_ids", []) if sid in subnet_to_col]

    if cols:
        min_col = min(cols)
        max_col = max(cols)
        span_x_left, _ = grid.cell_position(0, min_col)
        span_x_right, _ = grid.cell_position(0, max_col)
        span_x_right += grid.col_width(max_col)
    else:
        span_x_left, _ = grid.cell_position(0, 0)
        span_x_right = None

    # Icon left-aligned
    icon_x = span_x_left
    icon_y = y
    icon_el = inkdoc.make_symbol_instance(LAMBDA_SYMBOL, layer)
    tr = Transform(f'translate({icon_x}, {icon_y}) scale({icon_scale})')
    icon_el.transform = tr

    # Name right of icon
    name = fn.get("name", "")
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

    # Runtime below name (dimmed)
    runtime = fn.get("runtime", "")
    if runtime:
        runtime_y = text_y + font_h
        runtime_el = TextElement(x=str(text_x), y=str(runtime_y))
        runtime_el.text = runtime
        runtime_el.style = {
            'font-family': "'DejaVu Sans', sans-serif",
            'font-size': f'{font_size}px',
            'fill': get_text_color(config),
            'fill-opacity': str(get_text_dimmed_opacity(config)),
            'stroke': 'none',
            'font-weight': 'normal',
            'font-style': 'normal',
        }
        layer.append(runtime_el)

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


def render_lambda_zone(inkdoc, vpc_lambdas, zone_y, grid, subnet_to_col, layer, config=None):
    """Render all VPC Lambdas in the pre-grid zone."""
    cfg = _get_cfg(config)
    card_gap = cfg["card_gap"]

    cursor_y = zone_y
    for fn in vpc_lambdas:
        h = render_lambda_spanning(inkdoc, fn, cursor_y, grid, subnet_to_col, layer, config)
        if h > 0:
            cursor_y += h + card_gap


# --- Non-VPC Lambda rendering (for Global region) ---

def render_non_vpc_lambdas(inkdoc, lambdas, x, y, config=None):
    """Render non-VPC Lambda functions as a simple list (icon + name).

    Returns (total_width, total_height) of the rendered block.
    """
    if not lambdas:
        return (0, 0)

    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]
    card_gap = cfg["card_gap"]
    card_padding = cfg["card_padding"]

    lambda_layer = get_or_create_layer(inkdoc, "Lambda")

    icon_h = ICON_BASE_SIZE * icon_scale
    icon_w = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)

    cursor_y = y
    max_width = 0

    for fn in lambdas:
        name = fn.get("name", "")

        # Icon
        icon_el = inkdoc.make_symbol_instance(LAMBDA_SYMBOL, lambda_layer)
        tr = Transform(f'translate({x}, {cursor_y}) scale({icon_scale})')
        icon_el.transform = tr

        # Name to the right of icon
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
        lambda_layer.append(text_el)

        w = icon_w + card_padding + estimate_text_width(name, font_size)
        if w > max_width:
            max_width = w

        cursor_y += icon_h + card_gap

    total_height = cursor_y - y - card_gap
    return (max_width, total_height)
