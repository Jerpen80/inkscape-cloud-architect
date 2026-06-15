from inkex.elements import TextElement, Rectangle
from inkex import Transform
from ica_utils.text_utils import estimate_text_width, get_font_height
from ica_utils import resource_ec2
from ica_utils.theme import get_text_color, get_text_dimmed_opacity
from ica_utils.legend import register_legend

ASG_SYMBOL = "AWS-Group-light.svg:auto-scaling-group.svg"
ICON_BASE_SIZE = 40
DEFAULT_ICON_SCALE = 0.35

DEFAULT_STROKE_COLOR = "#ED7100"
DEFAULT_STROKE_WIDTH = 0.5
DEFAULT_STROKE_DASHARRAY = "4,4"
DEFAULT_LABEL_HEIGHT = 28
DEFAULT_PADDING = 6
DEFAULT_TOP_MARGIN = 10
DEFAULT_FONT_SIZE = 11

register_legend("resource", "Auto Scaling", "AWS-Group-light.svg:auto-scaling-group.svg", "Auto Scaling Groups")


def _get_cfg(config):
    return (config or {}).get("layout", {}).get("asg", {})


def label_width(asg_name, config=None):
    """Compute the minimum cell width needed to fit an ASG label (icon + name + padding)."""
    cfg = _get_cfg(config)
    padding = cfg["padding"]
    font_size = cfg["font_size"]
    icon_scale = cfg["icon_scale"]
    icon_w = ICON_BASE_SIZE * icon_scale
    # outer padding + container padding + icon + gap + text + container padding + outer padding
    text_w = estimate_text_width(asg_name, font_size)
    return padding * 2 + padding + icon_w + 4 + text_w + padding * 2


def container_overhead(config=None):
    """Extra height added per ASG container (top_margin + label + padding)."""
    cfg = _get_cfg(config)
    label_h = cfg["label_height"]
    top_margin = cfg["top_margin"]
    return top_margin + label_h


def subnet_asg_extra_height(subnet_instances, instance_to_asg, config=None):
    """Compute extra height needed for ASG containers in a subnet.

    For each ASG that has instances in this subnet, adds container_overhead.
    """
    asgs_in_subnet = set()
    for inst in subnet_instances:
        iid = inst.get("instance_id", "")
        asg_name = instance_to_asg.get(iid)
        if asg_name:
            asgs_in_subnet.add(asg_name)
    return len(asgs_in_subnet) * container_overhead(config)


def sort_instances_for_asg(subnet_instances, instance_to_asg):
    """Sort instances: non-ASG first, then grouped by ASG name."""
    non_asg = []
    asg_groups = {}
    for inst in subnet_instances:
        iid = inst.get("instance_id", "")
        asg_name = instance_to_asg.get(iid)
        if asg_name:
            asg_groups.setdefault(asg_name, []).append(inst)
        else:
            non_asg.append(inst)
    # Return non-ASG instances first, then ASG groups in sorted order
    sorted_instances = list(non_asg)
    asg_order = []
    for asg_name in sorted(asg_groups.keys()):
        asg_order.append((asg_name, len(sorted_instances), len(asg_groups[asg_name])))
        sorted_instances.extend(asg_groups[asg_name])
    return sorted_instances, asg_order


def render_asg_spanning(inkdoc, auto_scaling_groups, instance_to_asg, asg_lookup,
                        instance_map, placement, grid, subnet_to_col,
                        subnet_label_height, layer, config=None):
    """Render ASG spanning rectangles across columns.

    For each ASG, draws a dashed rect spanning from its leftmost to rightmost
    subnet column, positioned at the y-offset of its instances within the row.
    """
    cfg = _get_cfg(config)
    stroke_color = cfg["stroke_color"]
    stroke_width = cfg["stroke_width"]
    stroke_dash = cfg["stroke_dasharray"]
    label_h = cfg["label_height"]
    padding = cfg["padding"]
    top_margin = cfg["top_margin"]
    font_size = cfg["font_size"]
    icon_scale = cfg["icon_scale"]

    ec2_card_top = (config or {}).get("layout", {}).get("ec2", {})["card_top"]
    ec2_card_gap = (config or {}).get("layout", {}).get("ec2", {})["card_gap"]
    ch = resource_ec2.card_height(config)

    # Build per-ASG: which (row, col) cells contain its instances, and the start_idx per cell
    # We need to know the card index of the first ASG instance in each subnet
    asg_cells = {}  # asg_name → set of (row, col)
    for (row, col), subnet in placement.items():
        sid = subnet.get("subnet_id", "")
        subnet_insts = instance_map.get(sid, [])
        if not subnet_insts:
            continue
        _, asg_order = sort_instances_for_asg(subnet_insts, instance_to_asg)
        for asg_name, start_idx, count in asg_order:
            asg_cells.setdefault(asg_name, []).append({
                "row": row, "col": col,
                "start_idx": start_idx, "count": count,
            })

    # Track cumulative ASG overhead per row for correct y positioning
    row_asg_count = {}  # row → number of ASGs already rendered in this row

    # Process ASGs sorted by name to match sort_instances_for_asg ordering
    for asg in sorted(auto_scaling_groups, key=lambda a: a.get("name", "")):
        asg_name = asg.get("name", "")
        cells = asg_cells.get(asg_name, [])
        if not cells:
            continue

        asg_data = asg_lookup.get(asg_name, {})
        min_s = asg_data.get("min_size", 0)
        max_s = asg_data.get("max_size", 0)
        desired = asg_data.get("desired_capacity", 0)

        # Full column span from ASG's subnet_ids (used for overall span reference)
        all_asg_cols = set()
        for sid in asg.get("subnet_ids", []):
            if sid in subnet_to_col:
                all_asg_cols.add(subnet_to_col[sid])
        for cell in cells:
            all_asg_cols.add(cell["col"])

        if not all_asg_cols:
            continue

        # Group cells by row
        rows_with_cells = {}
        for cell in cells:
            rows_with_cells.setdefault(cell["row"], []).append(cell)

        # X span: from left edge of leftmost to right edge of rightmost ASG column
        min_col = min(all_asg_cols)
        max_col = max(all_asg_cols)
        span_x_left, _ = grid.cell_position(0, min_col)
        span_x_right, _ = grid.cell_position(0, max_col)
        span_x_right += grid.col_width(max_col)

        # Draw one spanning rect per row
        for row, row_cells in sorted(rows_with_cells.items()):
            max_count = max(c["count"] for c in row_cells)

            _, sy = grid.cell_position(row, row_cells[0]["col"])

            # Position based on ASG order in this row, not card indices.
            # Non-ASG instances come first, then ASGs stack sequentially.
            # Find how many non-ASG instances are in this row (from any subnet).
            non_asg_count = 0
            for (r, c), subnet in placement.items():
                if r != row:
                    continue
                sid = subnet.get("subnet_id", "")
                for inst in instance_map.get(sid, []):
                    if inst.get("instance_id", "") not in instance_to_asg:
                        non_asg_count = max(non_asg_count, 1)  # at least some exist
                        break

            # Compute non-ASG cards height (max non-ASG count across columns in this row)
            max_non_asg = 0
            for (r, c), subnet in placement.items():
                if r != row:
                    continue
                sid = subnet.get("subnet_id", "")
                n = sum(1 for inst in instance_map.get(sid, []) if inst.get("instance_id", "") not in instance_to_asg)
                max_non_asg = max(max_non_asg, n)

            non_asg_h = resource_ec2.cards_height(max_non_asg, config) if max_non_asg > 0 else 0

            # ASG rect index in this row
            asg_idx = row_asg_count.get(row, 0)

            # Compute cumulative height of all previous ASGs in this row
            prev_asg_h = 0
            for prev_asg in sorted(auto_scaling_groups, key=lambda a: a.get("name", ""))[:asg_idx + len(auto_scaling_groups)]:
                prev_name = prev_asg.get("name", "")
                if prev_name == asg_name:
                    break
                prev_cells = asg_cells.get(prev_name, [])
                prev_in_row = [c for c in prev_cells if c["row"] == row]
                if prev_in_row:
                    prev_max_count = max(c["count"] for c in prev_in_row)
                    prev_cards_h = prev_max_count * ch + max(0, prev_max_count - 1) * ec2_card_gap
                    prev_asg_h += label_h + prev_cards_h + padding + top_margin

            cards_start_y = sy + subnet_label_height + ec2_card_top + non_asg_h
            container_y = cards_start_y + prev_asg_h

            row_asg_count[row] = asg_idx + 1
            container_x = span_x_left + padding
            container_w = (span_x_right - span_x_left) - padding * 2

            # Height: label + cards of the column with most instances in this row
            max_count = max(c["count"] for c in row_cells)
            cards_block_h = max_count * ch + max(0, max_count - 1) * ec2_card_gap
            container_h = label_h + cards_block_h + padding

            # Dashed rectangle
            rect = Rectangle.new(container_x, container_y, container_w, container_h)
            rect.style = {
                "fill": "none",
                "stroke": stroke_color,
                "stroke-width": stroke_width,
                "stroke-dasharray": stroke_dash,
            }
            layer.append(rect)

            # Icon + label at top of container
            font_h = get_font_height(font_size)
            icon_w = ICON_BASE_SIZE * icon_scale

            icon_x = container_x + 2
            icon_y = container_y + 2
            icon_el = inkdoc.make_symbol_instance(ASG_SYMBOL, layer)
            tr = Transform(f'translate({icon_x}, {icon_y}) scale({icon_scale})')
            icon_el.transform = tr

            label_x = icon_x + icon_w + 4
            label_y = container_y + font_h + 2

            name_el = TextElement(x=str(label_x), y=str(label_y))
            name_el.text = asg_name
            name_el.style = {
                'font-family': "'DejaVu Sans', sans-serif",
                'font-size': f'{font_size}px',
                'fill': get_text_color(config),
                'fill-opacity': '0.7',
                'stroke': 'none',
                'font-weight': 'normal',
                'font-style': 'normal',
            }
            layer.append(name_el)

            capacity_y = label_y + font_h
            capacity_el = TextElement(x=str(label_x), y=str(capacity_y))
            capacity_el.text = f"min:{min_s} desired:{desired} max:{max_s}"
            capacity_el.style = {
                'font-family': "'DejaVu Sans', sans-serif",
                'font-size': f'{font_size}px',
                'fill': get_text_color(config),
                'fill-opacity': str(get_text_dimmed_opacity(config)),
                'stroke': 'none',
                'font-weight': 'normal',
                'font-style': 'normal',
            }
            layer.append(capacity_el)
