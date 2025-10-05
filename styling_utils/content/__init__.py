"""
Content-specific utilities.

This module contains utilities for formatting specific content types
like headers, footers, and other document elements.
"""

from .header_footer_styling_utils import (
    apply_header_footer_styles,
    apply_header_footer_to_all_sections
)

__all__ = [
    'apply_header_footer_styles',
    'apply_header_footer_to_all_sections',
]
