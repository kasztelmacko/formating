from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import RGBColor
import roman
import re

def _hex_to_rgbcolor(hex_str):
    """Convert '#RRGGBB' string into docx RGBColor."""
    hex_str = hex_str.lstrip("#")
    r, g, b = (int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return RGBColor(r, g, b)

def _arabic_to_roman(num_str: str) -> str:
    return ".".join(roman.toRoman(int(p)) if p.isdigit() else p for p in num_str.split("."))

def _roman_to_arabic(roman_str: str) -> str:
    return ".".join(str(roman.fromRoman(p)) if p.isalpha() else p for p in roman_str.split("."))

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
    'header_style': 'header_style',
    'footer_style': 'footer_style',
}

STYLE_ATTRIBUTES_NAMES_MAPPING = {
    'font_format': 'font_format',
    'paragraph_format': 'paragraph_format',
    'based_on': 'based_on',
    'numbering_format': 'numbering_format',
    'numbering_side': 'numbering_side',
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

CHAPTER_SECTION_NUMBERING_REGEX = {
    "arabic_base": r"\d+(?:\.\d+)*",
    "roman_base": r"([IVXLCDMivxlcdm\d]+(?:\.[IVXLCDMivxlcdm\d]+)*)",

    # TARGET: ROMAN (Source: Arabic-only)
    "roman_left": re.compile(r"^\s*(" + r"\d+(?:\.\d+)*" + r")\s*([.:-]?\s*)"),
    "roman_right": re.compile(r"(\s*[.:-]?\s*)(" + r"\d+(?:\.\d+)*" + r")\s*$"),

    # TARGET: ARABIC (Source: Roman/Mixed)
    "arabic_left": re.compile(r"^\s*" + r"([IVXLCDMivxlcdm\d]+(?:\.[IVXLCDMivxlcdm\d]+)*)" + r"\s*([.:-]?\s*)", re.IGNORECASE),
    "arabic_right": re.compile(r"(\s*[.:-]?\s*|^\s*)" + r"([IVXLCDMivxlcdm\d]+(?:\.[IVXLCDMivxlcdm\d]+)*)" + r"\s*$", re.IGNORECASE),
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

# Pre-computed XML namespace tags for WordprocessingML elements
W_TAGS = {
    'abstractNum': f'{{{OPENXML_FORMATS["W"]}}}abstractNum',
    'lvl': f'{{{OPENXML_FORMATS["W"]}}}lvl',
    'pPr': f'{{{OPENXML_FORMATS["W"]}}}pPr',
    'ind': f'{{{OPENXML_FORMATS["W"]}}}ind',
    'left': f'{{{OPENXML_FORMATS["W"]}}}left',
    'hanging': f'{{{OPENXML_FORMATS["W"]}}}hanging',
    'lvlText': f'{{{OPENXML_FORMATS["W"]}}}lvlText',
    'val': f'{{{OPENXML_FORMATS["W"]}}}val',
    'rPr': f'{{{OPENXML_FORMATS["W"]}}}rPr',
    'rFonts': f'{{{OPENXML_FORMATS["W"]}}}rFonts',
    'numPr': f'{{{OPENXML_FORMATS["W"]}}}numPr',
    'numId': f'{{{OPENXML_FORMATS["W"]}}}numId',
    'ilvl': f'{{{OPENXML_FORMATS["W"]}}}ilvl'
}

HEADER_FOOTER_FIELD_MAPPINGS = [
    (r'\{page_number\}', 'PAGE'),
    (r'\{total_pages\}', 'NUMPAGES'),
    (r'\{datetime\}', 'DATE \\@ "dd/MM/yyyy HH:mm"'),
    (r'\{numpages\}', 'NUMPAGES'),
    (r'\{page\}', 'PAGE'),
    (r'\{date\}', 'DATE \\@ "dd/MM/yyyy"'),
    (r'\{time\}', 'TIME \\@ "HH:mm"')
]

HEADER_FOOTER_LAYOUT_CONFIG = {
    'use_table_for_multiple_positions': True,
    'table_style': 'Table Grid',
    'table_borders': False,
    'column_widths': [33.33, 33.33, 33.34],
    'alignments': ['left', 'center', 'right']
}