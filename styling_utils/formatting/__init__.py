"""
Formatting utilities.

This module contains utilities for formatting paragraphs, lists, tables, and figures.
"""

from .paragraph_cleaning_utils import apply_paragraph_cleaning, apply_empty_paragraph_removal, is_paragraph_empty
from .bullet_list_styling_utils import (
    apply_bullet_character_updates, 
    apply_list_termination_characters,
    find_all_list_paragraphs
)
from .table_figure_titles_utils import apply_table_figure_styles, apply_source_styles

__all__ = [
    'apply_paragraph_cleaning',
    'apply_empty_paragraph_removal', 
    'is_paragraph_empty',
    'apply_bullet_character_updates',
    'apply_list_termination_characters',
    'find_all_list_paragraphs',
    'apply_table_figure_styles',
    'apply_source_styles',
]
