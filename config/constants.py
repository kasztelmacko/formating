"""
Configuration constants for document formatting.

This module contains pure constants used throughout the document formatting system.
"""

# Style name mappings
STYLE_NAMES_MAPPING = {
    'main_text': 'main_text',
    'chapter_titles': 'chapter_titles',
    'subchapter_titles_level_2': 'subchapter_titles_level_2',
    'subchapter_titles_level_3': 'subchapter_titles_level_3',
    'table_titles': 'table_titles',
    'figure_titles': 'figure_titles',
    'source_text': 'source_text',
    'header_row_style': 'header_row_style',
    'header_style': 'header_style',
    'footer_style': 'footer_style',
}

# Style attribute name mappings
STYLE_ATTRIBUTES_NAMES_MAPPING = {
    'font_format': 'font_format',
    'paragraph_format': 'paragraph_format',
    'based_on': 'based_on',
    'numbering_format': 'numbering_format',
    'numbering_side': 'numbering_side',
    'common_pattern_format': 'common_pattern_format',
}

# Bullet character options
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

# Header/Footer field mappings
HEADER_FOOTER_FIELD_MAPPINGS = [
    (r'\{page_number\}', 'PAGE'),
    (r'\{total_pages\}', 'NUMPAGES'),
    (r'\{datetime\}', 'DATE \\@ "dd/MM/yyyy HH:mm"'),
    (r'\{numpages\}', 'NUMPAGES'),
    (r'\{page\}', 'PAGE'),
    (r'\{date\}', 'DATE \\@ "dd/MM/yyyy"'),
    (r'\{time\}', 'TIME \\@ "HH:mm"')
]

# Header/Footer layout configuration
HEADER_FOOTER_LAYOUT_CONFIG = {
    'use_table_for_multiple_positions': True,
    'table_style': 'Table Grid',
    'table_borders': False,
    'column_widths': [33.33, 33.33, 33.34],
    'alignments': ['left', 'center', 'right']
}
