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

__all__ = [
    'remove_all_numbering',
    'apply_numbering_to_text',
    'process_paragraph_text',
    'update_paragraph_numbering',
    'apply_chapter_based_numbering',
]
