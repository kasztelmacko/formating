from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_COLOR_INDEX
from styling_utils import _hex_to_rgbcolor, _resolve_enum, _set_font_name

FONT_MAPPING = {
    "name": ("name", _set_font_name),
    "size": ("size", Pt),
    "bold": ("bold", None),
    "italic": ("italic", None),
    "underline": ("underline", None),
    "highlight": ("highlight_color", lambda v: _resolve_enum(WD_COLOR_INDEX, v)),
    "color_rgb": ("color.rgb", _hex_to_rgbcolor),
}

PARAGRAPH_FORMAT_MAPPING = {
    "alignment": ("alignment", lambda v: _resolve_enum(WD_ALIGN_PARAGRAPH, v)),
    "left_indent": ("left_indent", Cm),
    "right_indent": ("right_indent", Cm),
    "first_line_indent": ("first_line_indent", Cm),
    "space_before": ("space_before", Pt),
    "space_after": ("space_after", Pt),
    "line_spacing": ("line_spacing", None),
    "keep_with_next": ("keep_with_next", None),
    "keep_together": ("keep_together", None),
    "widow_control": ("widow_control", None),
}