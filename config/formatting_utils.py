"""
Formatting utility functions for document styling.

This module contains utility functions for formatting operations like color conversion,
enum resolution, and other formatting-related utilities.
"""

from docx.shared import RGBColor


def hex_to_rgbcolor(hex_str):
    """Convert '#RRGGBB' string into docx RGBColor."""
    hex_str = hex_str.lstrip("#")
    r, g, b = (int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return RGBColor(r, g, b)


def resolve_enum(enum_class, name):
    """Get enum value from its name (string)."""
    return getattr(enum_class, name)
