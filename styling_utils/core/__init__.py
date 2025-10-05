"""
Core styling utilities.

This module contains the fundamental style application functionality
used throughout the document formatting system.
"""

from .style_appliers import apply_docx_style_definitions, apply_docx_style_attributes, map_config_to_docx_attributes

__all__ = [
    'apply_docx_style_definitions',
    'apply_docx_style_attributes',
    'map_config_to_docx_attributes',
]
