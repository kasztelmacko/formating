"""
Configuration package for document formatting.

This package provides all configuration constants, mappings, patterns, and utilities
used throughout the document formatting system.

For backward compatibility, this module exports all the same names as the original
style_mapping_config.py file.
"""

# Import all constants
from .constants import (
    STYLE_NAMES_MAPPING,
    STYLE_ATTRIBUTES_NAMES_MAPPING,
    BULLET_CHARACTER_OPTIONS,
    HEADER_FOOTER_FIELD_MAPPINGS,
    HEADER_FOOTER_LAYOUT_CONFIG,
)

# Import all mappings
from .mappings import (
    FONT_MAPPING,
    PARAGRAPH_FORMAT_MAPPING,
)

# Import all patterns
from .patterns import (
    BASE_PATTERNS,
    CHAPTER_SECTION_NUMBERING_REGEX,
    RENUMBERING_REGEX,
    OPENXML_FORMATS,
    W_TAGS,
)

# Import all utility functions
from .utils import (
    _hex_to_rgbcolor,
    _arabic_to_roman,
    _roman_to_arabic,
    _resolve_enum,
    expand_common_pattern,
)

# Export everything for backward compatibility
__all__ = [
    # Constants
    'STYLE_NAMES_MAPPING',
    'STYLE_ATTRIBUTES_NAMES_MAPPING',
    'BULLET_CHARACTER_OPTIONS',
    'HEADER_FOOTER_FIELD_MAPPINGS',
    'HEADER_FOOTER_LAYOUT_CONFIG',
    
    # Mappings
    'FONT_MAPPING',
    'PARAGRAPH_FORMAT_MAPPING',
    
    # Patterns
    'BASE_PATTERNS',
    'CHAPTER_SECTION_NUMBERING_REGEX',
    'RENUMBERING_REGEX',
    'OPENXML_FORMATS',
    'W_TAGS',
    
    # Utility functions
    '_hex_to_rgbcolor',
    '_arabic_to_roman',
    '_roman_to_arabic',
    '_resolve_enum',
    'expand_common_pattern',
]
