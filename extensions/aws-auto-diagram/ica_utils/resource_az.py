from inkex.elements import TextElement, Rectangle
from ica_utils.layers import get_or_create_layer
from ica_utils.text_utils import get_font_height
from ica_utils.theme import get_text_color, get_text_dimmed_opacity

FONT_SIZE_PX = 17


def render_az_columns(inkdoc, vpc_x, vpc_y, grid, azs, num_rows, config):
    """Render dashed AZ column rects and labels on the Availability Zones layer."""
    layout = config.get("layout", {})
    az_cfg = layout.get("availability_zone", {})

    if not az_cfg["enabled"]:
        return

    az_pad = az_cfg.get("padding", {})
    pad_top = az_pad["top"]
    pad_bottom = az_pad["bottom"]
    pad_sides = az_pad["sides"]
    stroke_color = az_cfg["stroke_color"]
    stroke_width = az_cfg["stroke_width"]
    stroke_dasharray = az_cfg["stroke_dasharray"]
    label_prefix = az_cfg["label_prefix"]

    row_gap = grid.row_gap

    az_layer = get_or_create_layer(inkdoc, "Availability Zones")

    # Content height = sum of actual row heights (which may vary with instance count)
    content_height = sum(grid.row_height(r) for r in range(num_rows))
    content_height += max(0, num_rows - 1) * row_gap

    # AZ rects start just above the first subnet row
    # The grid's first cell y = vpc_y + grid.padding_top
    first_cell_y = grid.cell_position(0, 0)[1]

    for col, az in enumerate(azs):
        cell_x, _ = grid.cell_position(0, col)
        col_w = grid.col_width(col)

        # AZ rect wraps the column with padding
        az_x = cell_x - pad_sides
        az_y = first_cell_y - pad_top
        az_w = col_w + pad_sides * 2
        az_h = pad_top + content_height + pad_bottom

        rect = Rectangle.new(az_x, az_y, az_w, az_h)
        rect.style = {
            "fill": "none",
            "stroke": stroke_color,
            "stroke-width": stroke_width,
            "stroke-dasharray": stroke_dasharray,
        }
        az_layer.append(rect)

        # AZ label at top of column
        label = f"{label_prefix}{az}" if label_prefix else az
        font_height = get_font_height(FONT_SIZE_PX)
        text_x = az_x + pad_sides
        text_y = az_y + font_height + 3
        elem = TextElement(x=str(text_x), y=str(text_y))
        elem.text = label
        elem.style = {
            'font-family': "'DejaVu Sans', sans-serif",
            'font-size': f'{FONT_SIZE_PX}px',
            'fill': get_text_color(config),
            'fill-opacity': '1.0',
            'stroke': 'none',
            'font-weight': 'normal',
            'font-style': 'normal',
        }
        az_layer.append(elem)
