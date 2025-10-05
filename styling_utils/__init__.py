"""
Styling utilities package for document formatting.

This package provides utilities for formatting Word documents including:
- Core style application functionality
- Paragraph and text formatting
- Numbering and chapter/section management
- Content-specific formatting (tables, figures, headers, footers)
"""

from .core.style_appliers import apply_docx_style_definitions, apply_docx_style_attributes, map_config_to_docx_attributes
from .formatting.paragraph_cleaning_utils import clean_paragraph, remove_empty_paragraph, is_paragraph_empty
from .formatting.bullet_list_styling_utils import (
    update_bullet_characters, 
    apply_list_termination_characters,
    find_all_list_paragraphs
)
from .formatting.table_figure_titles_utils import apply_table_figure_styles, apply_source_styles
from .numbering.numbering_utils import (
    remove_all_numbering,
    apply_numbering_to_text,
    process_paragraph_text,
    update_paragraph_numbering,
    apply_chapter_based_numbering
)
from .numbering.chapter_section_styles_utils import (
    enforce_chapter_page_breaks,
    adjust_chapter_section_numbering_format,
    adjust_section_numbering_order
)
from .content.header_footer_styling_utils import (
    apply_header_footer_styles,
    apply_header_footer_to_all_sections
)

__all__ = [
    # Core functionality
    'apply_docx_style_definitions',
    'apply_docx_style_attributes', 
    'map_config_to_docx_attributes',
    
    # Formatting utilities
    'clean_paragraph',
    'remove_empty_paragraph',
    'is_paragraph_empty',
    'update_bullet_characters',
    'apply_list_termination_characters',
    'find_all_list_paragraphs',
    'apply_table_figure_styles',
    'apply_source_styles',
    
    # Numbering utilities
    'remove_all_numbering',
    'apply_numbering_to_text',
    'process_paragraph_text',
    'update_paragraph_numbering',
    'apply_chapter_based_numbering',
    'enforce_chapter_page_breaks',
    'adjust_chapter_section_numbering_format',
    'adjust_section_numbering_order',
    
    # Content utilities
    'apply_header_footer_styles',
    'apply_header_footer_to_all_sections',
]
