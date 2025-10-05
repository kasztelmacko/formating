"""
Styling utilities package for document formatting.

This package provides utilities for formatting Word documents including:
- Core style application functionality
- Paragraph and text formatting
- Numbering and chapter/section management
- Content-specific formatting (tables, figures, headers, footers)
"""

from .core.style_appliers import apply_docx_style_definitions, apply_docx_style_attributes, map_config_to_docx_attributes
from .formatting.paragraph_cleaning_utils import apply_paragraph_cleaning, apply_empty_paragraph_removal, is_paragraph_empty
from .formatting.bullet_list_styling_utils import (
    apply_bullet_character_updates, 
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
from .formatting.chapter_section_styles_utils import (
    apply_chapter_page_breaks,
    apply_chapter_section_numbering_format,
    apply_section_numbering_order
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
    'apply_paragraph_cleaning',
    'apply_empty_paragraph_removal',
    'is_paragraph_empty',
    'apply_bullet_character_updates',
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
    'apply_chapter_page_breaks',
    'apply_chapter_section_numbering_format',
    'apply_section_numbering_order',
    
    # Content utilities
    'apply_header_footer_styles',
    'apply_header_footer_to_all_sections',
]
