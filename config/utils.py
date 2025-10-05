"""
Utility functions for configuration processing.

This module contains utility functions used for processing configuration data
and converting between different formats.
"""

from docx.shared import RGBColor
import roman
from .patterns import BASE_PATTERNS

def _hex_to_rgbcolor(hex_str):
    """Convert '#RRGGBB' string into docx RGBColor."""
    hex_str = hex_str.lstrip("#")
    r, g, b = (int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return RGBColor(r, g, b)

def _arabic_to_roman(num_str: str) -> str:
    """Convert Arabic numerals to Roman numerals."""
    return ".".join(roman.toRoman(int(p)) if p.isdigit() else p for p in num_str.split("."))

def _roman_to_arabic(roman_str: str) -> str:
    """Convert Roman numerals to Arabic numerals."""
    return ".".join(str(roman.fromRoman(p)) if p.isalpha() else p for p in roman_str.split("."))

def _resolve_enum(enum_class, name):
    """Get enum value from its name (string)."""
    return getattr(enum_class, name)

def expand_common_pattern(common_pattern, numbering_format="ARABIC"):
    """Expand a common pattern string into a regex pattern."""
    if not common_pattern:
        return ""

    if "number" not in common_pattern and "." not in common_pattern:
        return common_pattern

    number_type = numbering_format.upper()
    number_pattern = BASE_PATTERNS["roman_number" if number_type == "ROMAN" else "arabic_number"]

    return common_pattern.replace("number", number_pattern)
