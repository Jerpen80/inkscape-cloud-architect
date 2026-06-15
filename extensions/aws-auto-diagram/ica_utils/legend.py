import inkex
from inkex.elements import TextElement, Rectangle
from inkex import Transform
from ica_utils.layers import get_or_create_layer
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils.theme import get_text_color, get_border_color

ICON_BASE_SIZE = 40
LABEL_FONT_SIZE = 17
LABEL_ICON_GAP = 4
ICON_PADDING = 2
RECT_PADDING = 20

LEGEND_REGISTRY = []


def register_legend(category, name, symbol, layer, border_key=None):
    """Register a legend entry. Called at module level by resource modules."""
    LEGEND_REGISTRY.append({
        "category": category,
        "name": name,
        "symbol": symbol,
        "layer": layer,
        "border_key": border_key,
    })


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("legend", {})


def _has_layer_content(inkdoc, layer_name):
    """Check if a layer has any child elements."""
    ns = {'svg': 'http://www.w3.org/2000/svg',
          'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}
    for g in inkdoc.svg.findall(f".//svg:g[@inkscape:label='{layer_name}']", ns):
        if len(g) > 0:
            return True
    return False


def render_legend(inkdoc, config=None):
    """Render the legend below all content on the Legend layer."""
    cfg = _get_cfg(config)
    icon_scale = cfg["icon_scale"]
    font_size = cfg["font_size"]
    item_gap = cfg["item_gap"]
    row_gap = cfg["row_gap"]
    section_gap = cfg["section_gap"]
    top_spacing = cfg["top_spacing"]
    swatch_w = cfg["swatch_width"]
    swatch_h = cfg["swatch_height"]

    text_color = get_text_color(config)
    icon_w = ICON_BASE_SIZE * icon_scale
    icon_h = ICON_BASE_SIZE * icon_scale
    font_h = get_font_height(font_size)
    label_font_h = get_font_height(LABEL_FONT_SIZE)

    active_entries = [e for e in LEGEND_REGISTRY if _has_layer_content(inkdoc, e["layer"])]
    if not active_entries:
        return

    containers = [e for e in active_entries if e["category"] == "container"]
    resources = [e for e in active_entries if e["category"] == "resource"]

    legend_layer = get_or_create_layer(inkdoc, "Legend")

    # Find bottom of all content
    bbox = None
    for elem in inkdoc.svg.descendants():
        if isinstance(elem, inkex.ShapeElement):
            try:
                eb = elem.bounding_box()
                if eb is not None:
                    bbox = eb if bbox is None else (bbox + eb)
            except Exception:
                continue

    if bbox is None:
        return

    # Legend rect origin — leave space for the title icon+label at top-left
    rect_x = bbox.left
    rect_y = bbox.bottom + top_spacing
    content_x = rect_x + RECT_PADDING
    # Title takes up ICON_SIZE height at the top
    content_y = rect_y + ICON_PADDING + ICON_BASE_SIZE + RECT_PADDING

    cursor_y = content_y
    max_x = content_x

    # Render containers section
    if containers:
        label_el = TextElement(x=str(content_x), y=str(cursor_y + font_h))
        label_el.text = "Containers"
        label_el.style = {
            'font-family': "'DejaVu Sans', sans-serif",
            'font-size': f'{font_size}px',
            'fill': text_color,
            'fill-opacity': '0.6',
            'stroke': 'none',
            'font-weight': 'bold',
            'font-style': 'normal',
        }
        legend_layer.append(label_el)
        cursor_y += font_h + row_gap

        cursor_x = content_x
        for entry in containers:
            border_color = get_border_color(config, entry["border_key"].replace("border_", "")) if entry.get("border_key") else "#666"

            swatch = Rectangle.new(cursor_x, cursor_y, swatch_w, swatch_h)
            swatch.style = {"fill": "none", "stroke": border_color, "stroke-width": 1.5}
            legend_layer.append(swatch)

            if entry["symbol"]:
                ix = cursor_x + swatch_w + 4
                iy = cursor_y + (swatch_h - icon_h) / 2
                icon_el = inkdoc.make_symbol_instance(entry["symbol"], legend_layer)
                tr = Transform(f'translate({ix}, {iy}) scale({icon_scale})')
                icon_el.transform = tr
                text_start = ix + icon_w + 4
            else:
                text_start = cursor_x + swatch_w + 8

            text_y = cursor_y + (swatch_h + font_h) / 2
            text_el = TextElement(x=str(text_start), y=str(text_y))
            text_el.text = entry["name"]
            text_el.style = {
                'font-family': "'DejaVu Sans', sans-serif",
                'font-size': f'{font_size}px',
                'fill': text_color,
                'fill-opacity': '1.0',
                'stroke': 'none',
                'font-weight': 'normal',
                'font-style': 'normal',
            }
            legend_layer.append(text_el)

            name_w = estimate_text_width(entry["name"], font_size)
            cursor_x = text_start + name_w + item_gap
            max_x = max(max_x, cursor_x)

        cursor_y += max(swatch_h, icon_h) + section_gap

    # Render resources section
    if resources:
        label_el = TextElement(x=str(content_x), y=str(cursor_y + font_h))
        label_el.text = "Resources"
        label_el.style = {
            'font-family': "'DejaVu Sans', sans-serif",
            'font-size': f'{font_size}px',
            'fill': text_color,
            'fill-opacity': '0.6',
            'stroke': 'none',
            'font-weight': 'bold',
            'font-style': 'normal',
        }
        legend_layer.append(label_el)
        cursor_y += font_h + row_gap

        cursor_x = content_x
        for entry in resources:
            ix = cursor_x
            iy = cursor_y
            icon_el = inkdoc.make_symbol_instance(entry["symbol"], legend_layer)
            tr = Transform(f'translate({ix}, {iy}) scale({icon_scale})')
            icon_el.transform = tr

            text_x = ix + icon_w + 4
            text_y = cursor_y + (icon_h + font_h) / 2
            text_el = TextElement(x=str(text_x), y=str(text_y))
            text_el.text = entry["name"]
            text_el.style = {
                'font-family': "'DejaVu Sans', sans-serif",
                'font-size': f'{font_size}px',
                'fill': text_color,
                'fill-opacity': '1.0',
                'stroke': 'none',
                'font-weight': 'normal',
                'font-style': 'normal',
            }
            legend_layer.append(text_el)

            name_w = estimate_text_width(entry["name"], font_size)
            cursor_x = text_x + name_w + item_gap
            max_x = max(max_x, cursor_x)

        cursor_y += icon_h

    # Draw legend border rect
    rect_w = (max_x - rect_x) + RECT_PADDING
    rect_h = (cursor_y - rect_y) + RECT_PADDING
    legend_rect = Rectangle.new(rect_x, rect_y, rect_w, rect_h)
    legend_rect.style = {"fill": "none", "stroke": text_color, "stroke-width": 0.5}
    legend_layer.append(legend_rect)

    # "Legend" title label at top-left of rect
    title_x = rect_x + ICON_PADDING + ICON_BASE_SIZE + LABEL_ICON_GAP
    title_y = rect_y + ICON_PADDING + (ICON_BASE_SIZE + label_font_h) / 2
    title_el = TextElement(x=str(title_x), y=str(title_y))
    title_el.text = "Legend"
    title_el.style = {
        'font-family': "'DejaVu Sans', sans-serif",
        'font-size': f'{LABEL_FONT_SIZE}px',
        'fill': text_color,
        'fill-opacity': '1.0',
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal',
    }
    legend_layer.append(title_el)
