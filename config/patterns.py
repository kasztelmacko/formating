"""
Regex patterns and XML namespace definitions.

This module contains all regex patterns and XML namespace definitions
used for document processing and formatting.
"""

import re

# Base patterns for building more complex regexes
BASE_PATTERNS = {
    "arabic_number": r"\d+",
    "roman_number": r"[IVXLCDMivxlcdm\d]+",
    "decimal_number": r"\d+(?:\.\d+)*",
    "mixed_number": r"[IVXLCDMivxlcdm\d]+(?:\.[IVXLCDMivxlcdm\d]+)*",
    "word_boundary": r"\b",
    "space_optional": r"\s*",
    "space_required": r"\s+",
    "punctuation": r"[.:-]?",
    "extra_spaces": r"\s+",
}

# Compiled regex patterns for chapter/section numbering
CHAPTER_SECTION_NUMBERING_REGEX = {
    "arabic_base": BASE_PATTERNS["decimal_number"],
    "roman_base": f"({BASE_PATTERNS['mixed_number']})",

    # TARGET: ROMAN (Source: Arabic-only)
    "roman_left": re.compile(f"^{BASE_PATTERNS['space_optional']}({BASE_PATTERNS['decimal_number']}){BASE_PATTERNS['space_optional']}({BASE_PATTERNS['punctuation']}{BASE_PATTERNS['space_optional']})"),
    "roman_right": re.compile(f"({BASE_PATTERNS['space_optional']}{BASE_PATTERNS['punctuation']}{BASE_PATTERNS['space_optional']})({BASE_PATTERNS['decimal_number']}){BASE_PATTERNS['space_optional']}$"),

    # TARGET: ARABIC (Source: Roman/Mixed)
    "arabic_left": re.compile(f"^{BASE_PATTERNS['space_optional']}({BASE_PATTERNS['mixed_number']}){BASE_PATTERNS['space_optional']}({BASE_PATTERNS['punctuation']}{BASE_PATTERNS['space_optional']})", re.IGNORECASE),
    "arabic_right": re.compile(f"({BASE_PATTERNS['space_optional']}{BASE_PATTERNS['punctuation']}{BASE_PATTERNS['space_optional']}|^{BASE_PATTERNS['space_optional']})({BASE_PATTERNS['mixed_number']}){BASE_PATTERNS['space_optional']}$", re.IGNORECASE),
}

# Regex patterns for renumbering and cleanup
RENUMBERING_REGEX = {
    # Common word + numbering patterns
    "common_word_pattern": f"{BASE_PATTERNS['word_boundary']}{{common_word}}{BASE_PATTERNS['space_required']}{BASE_PATTERNS['mixed_number']}",
    
    # Roman numeral patterns (standalone)
    "roman_uppercase": f"{BASE_PATTERNS['word_boundary']}[IVXLCDM]+{BASE_PATTERNS['word_boundary']}",
    "roman_lowercase": f"{BASE_PATTERNS['word_boundary']}[ivxlcdm]+{BASE_PATTERNS['word_boundary']}",
    
    # Arabic number patterns (including decimal numbers like 1.1, 2.3, etc.)
    "arabic_numbers": f"{BASE_PATTERNS['word_boundary']}{BASE_PATTERNS['decimal_number']}{BASE_PATTERNS['word_boundary']}",
    
    # Space cleanup pattern
    "extra_spaces": BASE_PATTERNS["extra_spaces"],
    
    # Chapter patterns (for fallback removal)
    "chapter_uppercase": f"{BASE_PATTERNS['word_boundary']}CHAPTER{BASE_PATTERNS['space_required']}{BASE_PATTERNS['mixed_number']}{BASE_PATTERNS['word_boundary']}",
    "chapter_titlecase": f"{BASE_PATTERNS['word_boundary']}Chapter{BASE_PATTERNS['space_required']}{BASE_PATTERNS['mixed_number']}{BASE_PATTERNS['word_boundary']}",
    "chapter_lowercase": f"{BASE_PATTERNS['word_boundary']}chapter{BASE_PATTERNS['space_required']}{BASE_PATTERNS['mixed_number']}{BASE_PATTERNS['word_boundary']}",
    
    # Pattern boundaries for precise matching
    "pattern_start": r"(?:^|\s)",
    "pattern_end": r"(?:\s|$)",
    "word_boundary": BASE_PATTERNS["word_boundary"],
    
    # Cleanup patterns
    "leading_punctuation": r"^\s*[.:-]\s*",
    "trailing_punctuation": r"\s*[.:-]\s*$",
}

# OpenXML namespace definitions
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
