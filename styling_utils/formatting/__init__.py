"""
Formatting utilities.

This module contains utilities for formatting paragraphs, lists, tables, and figures.
"""

from .paragraph_cleaning_utils import clean_paragraph, remove_empty_paragraph, is_paragraph_empty
from .bullet_list_styling_utils import (
    update_bullet_characters, 
    apply_list_termination_characters,
    find_all_list_paragraphs
)
from .table_figure_titles_utils import apply_table_figure_styles, apply_source_styles

__all__ = [
    'clean_paragraph',
    'remove_empty_paragraph', 
    'is_paragraph_empty',
    'update_bullet_characters',
    'apply_list_termination_characters',
    'find_all_list_paragraphs',
    'apply_table_figure_styles',
    'apply_source_styles',
]
