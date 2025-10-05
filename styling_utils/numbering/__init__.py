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
    apply_chapter_page_breaks,
    apply_chapter_section_numbering_format,
    apply_section_numbering_order
)

__all__ = [
    'remove_all_numbering',
    'apply_numbering_to_text',
    'process_paragraph_text',
    'update_paragraph_numbering',
    'apply_chapter_based_numbering',
    'apply_chapter_page_breaks',
    'apply_chapter_section_numbering_format',
    'apply_section_numbering_order',
]
