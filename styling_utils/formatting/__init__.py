"""
Formatting utilities.

This module contains utilities for formatting paragraphs, lists, tables, and figures.
"""

from .bullet_list_styling_utils import (
    apply_bullet_character_updates,
    apply_list_termination_characters,
    find_all_list_paragraphs,
)
from .chapter_section_styles_utils import (
    apply_chapter_page_breaks,
    apply_chapter_section_numbering_format,
    apply_section_numbering_order,
)
from .paragraph_cleaning_utils import (
    apply_empty_paragraph_removal,
    apply_paragraph_cleaning,
    is_paragraph_empty,
)
from .table_figure_titles_utils import apply_source_styles, apply_table_figure_styles

__all__ = [
    "apply_bullet_character_updates",
    "apply_chapter_page_breaks",
    "apply_chapter_section_numbering_format",
    "apply_empty_paragraph_removal",
    "apply_list_termination_characters",
    "apply_paragraph_cleaning",
    "apply_section_numbering_order",
    "apply_source_styles",
    "apply_table_figure_styles",
    "find_all_list_paragraphs",
    "is_paragraph_empty",
]
