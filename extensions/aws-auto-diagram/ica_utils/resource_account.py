import inkex
from ica_utils.resource_vpc import aws_rect
from ica_utils.layers import get_or_create_layer
from ica_utils.theme import get_border_color
from ica_utils.legend import register_legend

DEFAULT_PADDING_TOP = 50
DEFAULT_PADDING_RIGHT = 20
DEFAULT_PADDING_BOTTOM = 20
DEFAULT_PADDING_LEFT = 20

register_legend("container", "Account", "AWS-Group-light.svg:cloud.svg", "Accounts", border_key="border_account")


def render_account_rect(inkdoc, account_name, config=None):
    """Render an account rectangle around all rendered content.

    Uses bounding box of existing elements to determine size,
    then draws the account rect with padding around everything.
    """
    layout = (config or {}).get("layout", {})
    acct_cfg = layout.get("account", {})
    acct_pad = acct_cfg.get("padding", {})

    pad_top = acct_pad.get("top", DEFAULT_PADDING_TOP)
    pad_right = acct_pad.get("right", DEFAULT_PADDING_RIGHT)
    pad_bottom = acct_pad.get("bottom", DEFAULT_PADDING_BOTTOM)
    pad_left = acct_pad.get("left", DEFAULT_PADDING_LEFT)

    # Compute bounding box of all rendered content
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

    account_layer = get_or_create_layer(inkdoc, "Accounts")

    # Account rect encloses all content with padding
    rect_x = bbox.left - pad_left
    rect_y = bbox.top - pad_top
    rect_w = (bbox.right - bbox.left) + pad_left + pad_right
    rect_h = (bbox.bottom - bbox.top) + pad_top + pad_bottom

    aws_rect(inkdoc, [rect_x, rect_y], [rect_w, rect_h],
             get_border_color(config, "account"),
             account_name, "AWS-Group-light.svg:cloud.svg", account_layer, config)
