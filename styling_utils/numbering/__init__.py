"""
Numbering utilities.

This module contains utilities for managing numbering, chapters, and sections.
"""

from .numbering_utils import (
    apply_chapter_based_numbering,
    apply_numbering_to_text,
    process_paragraph_text,
    remove_all_numbering,
    update_paragraph_numbering,
)

__all__ = [
    "apply_chapter_based_numbering",
    "apply_numbering_to_text",
    "process_paragraph_text",
    "remove_all_numbering",
    "update_paragraph_numbering",
]
