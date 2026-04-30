from ica_utils.resource_vpc import aws_rect
from ica_utils.layers import get_or_create_layer
from ica_utils.theme import get_border_color
from ica_utils.legend import register_legend

DEFAULT_PADDING_TOP = 50
DEFAULT_PADDING_RIGHT = 15
DEFAULT_PADDING_BOTTOM = 15
DEFAULT_PADDING_LEFT = 15

register_legend("container", "Region", "AWS-Group-light.svg:region.svg", "Regions", border_key="border_region")


def render_region_rect(inkdoc, region_name, xy, wh, config=None):
    """Render a region boundary rectangle at the given position and size."""
    region_layer = get_or_create_layer(inkdoc, "Regions")

    aws_rect(inkdoc, xy, wh, get_border_color(config, "region"), region_name,
             "AWS-Group-light.svg:region.svg", region_layer, config)


def get_region_padding(config):
    """Get region padding values from config."""
    layout = (config or {}).get("layout", {})
    region_cfg = layout.get("region", {})
    pad = region_cfg.get("padding", {})
    return {
        "top": pad.get("top", DEFAULT_PADDING_TOP),
        "right": pad.get("right", DEFAULT_PADDING_RIGHT),
        "bottom": pad.get("bottom", DEFAULT_PADDING_BOTTOM),
        "left": pad.get("left", DEFAULT_PADDING_LEFT),
    }


def get_region_gap(config):
    """Get horizontal gap between regions from config."""
    layout = (config or {}).get("layout", {})
    return layout.get("region", {}).get("gap", 20)
