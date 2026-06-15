from inkex.elements import TextElement
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.theme import get_text_color, get_text_dimmed_opacity
from ica_utils.legend import register_legend

SYMBOL_FILE = "AWS-Resource-database-light.svg"
RDS_SYMBOL = f"{SYMBOL_FILE}:res-amazon-aurora-amazon-rds-instance"
ELASTICACHE_REDIS_SYMBOL = f"{SYMBOL_FILE}:res-amazon-elasticache-elasticache-for-redis"
ELASTICACHE_MEMCACHED_SYMBOL = f"{SYMBOL_FILE}:res-amazon-elasticache-elasticache-for-memcached"

DEFAULT_ICON_SCALE = 0.5
DEFAULT_FONT_SIZE = 13
DEFAULT_CARD_GAP = 8
DEFAULT_CARD_TOP = 10

ICON_BASE_SIZE = 40

register_legend("resource", "RDS", "AWS-Resource-database-light.svg:res-amazon-aurora-amazon-rds-instance", "Database")
register_legend("resource", "ElastiCache", "AWS-Resource-database-light.svg:res-amazon-elasticache-elasticache-for-redis", "Database")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("database", {})


def _symbol_for(db_instance):
    db_type = db_instance.get("db_type", "")
    if db_type == "elasticache":
        engine = db_instance.get("engine", "")
        if engine == "memcached":
            return ELASTICACHE_MEMCACHED_SYMBOL
        return ELASTICACHE_REDIS_SYMBOL
    return RDS_SYMBOL


def card_height(config=None):
    """Height of a single database card (icon + name + detail)."""
    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]
    icon_h = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)
    return icon_h + font_h * 2 + 4


def cards_height(count, config=None):
    """Total height needed for N database cards including gaps."""
    if count == 0:
        return 0
    cfg = _get_cfg(config)
    card_gap = cfg["card_gap"]
    card_top = cfg["card_top"]
    ch = card_height(config)
    return card_top + count * ch + max(0, count - 1) * card_gap


def render_instance(inkdoc, db_instance, x, y, cell_width, layer, config=None):
    """Render a single database card at (x, y), centered within cell_width."""
    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]

    icon_h = ICON_BASE_SIZE * icon_scale
    icon_w = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)

    # Icon centered
    icon_x = x + (cell_width - icon_w) / 2
    icon_y = y
    icon_el = inkdoc.make_symbol_instance(_symbol_for(db_instance), layer)
    tr = Transform(f'translate({icon_x}, {icon_y}) scale({icon_scale})')
    icon_el.transform = tr

    # Name centered below icon
    name = db_instance.get("name", "")
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

    # Engine/class detail centered below name
    engine = db_instance.get("engine", "")
    inst_class = db_instance.get("instance_class", "")
    detail = f"{engine} / {inst_class}" if inst_class else engine
    detail_w = estimate_text_width(detail, font_size)
    detail_x = x + (cell_width - detail_w) / 2
    detail_y = name_y + font_h
    detail_el = TextElement(x=str(detail_x), y=str(detail_y))
    detail_el.text = detail
    detail_el.style = {
        'font-family': "'DejaVu Sans', sans-serif",
        'font-size': f'{font_size}px',
        'fill': get_text_color(config),
        'fill-opacity': str(get_text_dimmed_opacity(config)),
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal',
    }
    layer.append(detail_el)

    return card_height(config)


def render_instances_in_subnet(inkdoc, db_instances, sx, sy, cell_width, offset_y, layer, config=None):
    """Render all database instances stacked inside a subnet starting at offset_y below subnet top."""
    cfg = _get_cfg(config)
    card_gap = cfg["card_gap"]

    cursor_y = sy + offset_y
    for db_inst in db_instances:
        ch = render_instance(inkdoc, db_inst, sx, cursor_y, cell_width, layer, config)
        cursor_y += ch + card_gap
