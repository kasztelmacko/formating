"""
Configuration package for document formatting.

This package provides all configuration constants, mappings, and patterns
used throughout the document formatting system.

For backward compatibility, this module exports all the same names as the original
style_mapping_config.py file.
"""

# Import all constants
from .constants import (
    BULLET_CHARACTER_OPTIONS,
    DEFAULT_BULLET_LIST_INDENTATION,
    DEFAULT_NESTED_LEVEL_CONFIG,
    HEADER_FOOTER_FIELD_MAPPINGS,
    HEADER_FOOTER_LAYOUT_CONFIG,
    STYLE_ATTRIBUTES_NAMES_MAPPING,
    STYLE_NAMES_MAPPING,
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
    OPENXML_FORMATS,
    RENUMBERING_REGEX,
    W_TAGS,
)

# Export everything for backward compatibility
__all__ = [
    # Constants
    "STYLE_NAMES_MAPPING",
    "STYLE_ATTRIBUTES_NAMES_MAPPING",
    "BULLET_CHARACTER_OPTIONS",
    "HEADER_FOOTER_FIELD_MAPPINGS",
    "HEADER_FOOTER_LAYOUT_CONFIG",
    "DEFAULT_NESTED_LEVEL_CONFIG",
    "DEFAULT_BULLET_LIST_INDENTATION",
    # Mappings
    "FONT_MAPPING",
    "PARAGRAPH_FORMAT_MAPPING",
    # Patterns
    "BASE_PATTERNS",
    "CHAPTER_SECTION_NUMBERING_REGEX",
    "RENUMBERING_REGEX",
    "OPENXML_FORMATS",
    "W_TAGS",
]
