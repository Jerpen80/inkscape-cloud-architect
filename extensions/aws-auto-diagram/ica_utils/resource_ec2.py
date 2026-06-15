from inkex.elements import TextElement
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.theme import get_text_color, get_text_dimmed_opacity
from ica_utils.legend import register_legend

EC2_SYMBOL = "AWS-Resource-compute-light.svg:res-amazon-ec2-instance"

DEFAULT_ICON_SCALE = 0.5
DEFAULT_FONT_SIZE = 13
DEFAULT_CARD_GAP = 8
DEFAULT_CARD_TOP = 10

ICON_BASE_SIZE = 40  # symbol native size

register_legend("resource", "EC2", "AWS-Resource-compute-light.svg:res-amazon-ec2-instance", "EC2")


def card_height(config=None):
    """Height of a single EC2 instance card (icon + name + type)."""
    ec2_cfg = (config or {}).get("layout", {}).get("ec2", {})
    icon_scale = ec2_cfg["icon_scale"]
    font_size = ec2_cfg["font_size"]

    icon_h = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)
    return icon_h + font_h * 2 + 4  # icon + name + type + small spacing


def cards_height(instance_count, config=None):
    """Total height needed for N instance cards including gaps."""
    if instance_count == 0:
        return 0
    ec2_cfg = (config or {}).get("layout", {}).get("ec2", {})
    card_gap = ec2_cfg["card_gap"]
    card_top = ec2_cfg["card_top"]
    ch = card_height(config)
    return card_top + instance_count * ch + max(0, instance_count - 1) * card_gap


def render_instance(inkdoc, instance, x, y, cell_width, layer, config=None):
    """Render a single EC2 instance card at (x, y), centered within cell_width."""
    ec2_cfg = (config or {}).get("layout", {}).get("ec2", {})
    icon_scale = ec2_cfg["icon_scale"]
    font_size = ec2_cfg["font_size"]

    icon_h = ICON_BASE_SIZE * icon_scale
    icon_w = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)

    # Icon centered horizontally
    icon_x = x + (cell_width - icon_w) / 2
    icon_y = y
    icon_el = inkdoc.make_symbol_instance(EC2_SYMBOL, layer)
    tr = Transform(f'translate({icon_x}, {icon_y}) scale({icon_scale})')
    icon_el.transform = tr

    # Name centered below icon
    name = instance.get("name", "")
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

    # Instance type centered below name
    itype = instance.get("instance_type", "")
    type_w = estimate_text_width(itype, font_size)
    type_x = x + (cell_width - type_w) / 2
    type_y = name_y + font_h
    type_el = TextElement(x=str(type_x), y=str(type_y))
    type_el.text = itype
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

    return card_height(config)


def render_instances_in_subnet(inkdoc, instances, sx, sy, cell_width, subnet_label_height, layer, config=None):
    """Render all instances vertically stacked inside a subnet starting below the label."""
    ec2_cfg = (config or {}).get("layout", {}).get("ec2", {})
    card_gap = ec2_cfg["card_gap"]
    card_top = ec2_cfg["card_top"]

    cursor_y = sy + subnet_label_height + card_top
    for instance in instances:
        ch = render_instance(inkdoc, instance, sx, cursor_y, cell_width, layer, config)
        cursor_y += ch + card_gap
