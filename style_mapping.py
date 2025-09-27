from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import RGBColor

def _hex_to_rgbcolor(hex_str):
    """Convert '#RRGGBB' string into docx RGBColor."""
    hex_str = hex_str.lstrip("#")
    r, g, b = (int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return RGBColor(r, g, b)

def _resolve_enum(enum_class, name):
    """Get enum value from its name (string)."""
    return getattr(enum_class, name)

STYLE_NAMES_MAPPING = {
    'main_text': 'main_text',
    'chapter_titles': 'chapter_titles',
    'subchapter_titles_level_2': 'subchapter_titles_level_2',
    'subchapter_titles_level_3': 'subchapter_titles_level_3',
    'caption_style': 'caption_style',
    'header_row_style': 'header_row_style',
    'source_style': 'source_style',
}

STYLE_ATTRIBUTES_NAMES_MAPPING = {
    'font': 'font',
    'paragraph_format': 'paragraph_format',
    'based_on': 'based_on',
    'apply_to_regex': 'apply_to_regex',
}

FONT_MAPPING = {
    "name": ("name", None),
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

BULLET_CHARACTER_OPTIONS = {
        "bullet": "•",
        "arrow": "→",
        "diamond": "♦",
        "square": "▪",
        "circle": "○",
        "dash": "–",
        "star": "★",
        "check": "✓"
}

OPENXML_FORMATS = {
    "W": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",  # WordprocessingML
    "MC": "http://schemas.openxmlformats.org/markup-compatibility/2006",  # Markup compatibility
    "WP": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",  # Wordprocessing drawings
    "A": "http://schemas.openxmlformats.org/drawingml/2006/main",  # DrawingML main
    "PIC": "http://schemas.openxmlformats.org/drawingml/2006/picture",  # Pictures
    "M": "http://schemas.openxmlformats.org/officeDocument/2006/math",  # Office Math (equations)
    "R": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",  # Relationships
    "V": "urn:schemas-microsoft-com:vml",  # Legacy VML shapes
}