"""
Numbering utilities.

This module contains utilities for managing numbering, chapters, and sections.
"""

from .numbering_utils import (
    remove_all_numbering,
    apply_numbering_to_text,
    process_paragraph_text,
    update_paragraph_numbering,
    apply_chapter_based_numbering
)
from .chapter_section_styles_utils import (
    enforce_chapter_page_breaks,
    adjust_chapter_section_numbering_format,
    adjust_section_numbering_order
)

__all__ = [
    'remove_all_numbering',
    'apply_numbering_to_text',
    'process_paragraph_text',
    'update_paragraph_numbering',
    'apply_chapter_based_numbering',
    'enforce_chapter_page_breaks',
    'adjust_chapter_section_numbering_format',
    'adjust_section_numbering_order',
]
