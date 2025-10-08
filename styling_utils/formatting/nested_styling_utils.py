import re
from typing import Callable, Optional

from docx.document import Document
from docx.text.paragraph import Paragraph

from styling_utils.core.style_appliers import map_config_to_docx_attributes
from styling_utils.numbering.numbering_utils import expand_common_pattern


def apply_nested_paragraph_styling(
    paragraph: Paragraph,
    text_parts: list[tuple[str, Optional[dict]]],
    font_mapping: dict[str, tuple[str, Callable | None]],
    default_font_format: Optional[dict],
) -> None:
    """Apply different font styles to different parts of a paragraph text."""
    paragraph.clear()
    
    for text, font_format in text_parts:
        if not text.strip():
            continue
            
        run = paragraph.add_run(text)

        if font_format:
            map_config_to_docx_attributes(
                target=run.font, 
                config_data=font_format, 
                mapping=font_mapping
            )
        elif default_font_format:
            map_config_to_docx_attributes(
                target=run.font, 
                config_data=default_font_format, 
                mapping=font_mapping
            )


def create_numbered_text_parts(
    text: str,
    new_numbering: str,
    numbering_format: str,
    numbering_side: str,
    separator: str,
    common_pattern: str,
    common_pattern_side: str,
    common_pattern_separator: str,
    common_pattern_font_format: Optional[dict],
    default_font_format: Optional[dict],
) -> list[tuple[str, Optional[dict]]]:
    """Create text parts for nested styling based on numbering and common pattern configuration."""
    cleaned_text = text
    text_parts = []

    if common_pattern:
        expanded_pattern = expand_common_pattern(common_pattern, numbering_format)
        
        if not any(char in expanded_pattern for char in ["\\", "(", ")", "[", "]"]):
            if common_pattern_side.upper() == "LEFT":
                text_parts.append((expanded_pattern, common_pattern_font_format))
                text_parts.append((common_pattern_separator, None))
                text_parts.append((new_numbering, default_font_format))
            else:
                text_parts.append((new_numbering, default_font_format))
                text_parts.append((common_pattern_separator, None))
                text_parts.append((expanded_pattern, common_pattern_font_format))
        else:
            text_parts.append((new_numbering, default_font_format))
    else:
        text_parts.append((new_numbering, default_font_format))

    if numbering_side.upper() == "LEFT":
        text_parts.append((separator, None))
        text_parts.append((cleaned_text, default_font_format))
    else:
        text_parts.append((separator, None))
        text_parts.append((cleaned_text, default_font_format))
    
    return text_parts


def apply_nested_numbering_to_paragraph(
    paragraph: Paragraph,
    new_numbering: str,
    numbering_format: str,
    numbering_side: str,
    font_mapping: dict[str, tuple[str, Callable | None]],
    separator: str,
    common_pattern: str,
    common_pattern_side: str,
    common_pattern_separator: str,
    common_pattern_font_format: Optional[dict],
    default_font_format: Optional[dict],
) -> None:
    """
    Apply nested numbering styling to a paragraph with different styles for different parts.
    
    This is a convenience function that combines text part creation and styling application.
    """
    
    text_parts = create_numbered_text_parts(
        text=paragraph.text,
        new_numbering=new_numbering,
        numbering_format=numbering_format,
        numbering_side=numbering_side,
        separator=separator,
        common_pattern=common_pattern,
        common_pattern_side=common_pattern_side,
        common_pattern_separator=common_pattern_separator,
        common_pattern_font_format=common_pattern_font_format,
        default_font_format=default_font_format,
    )
    
    apply_nested_paragraph_styling(
        paragraph=paragraph,
        text_parts=text_parts,
        font_mapping=font_mapping,
        default_font_format=default_font_format,
    )


def apply_pattern_styling_to_paragraph(
    paragraph: Paragraph,
    pattern: str,
    font_mapping: dict[str, tuple[str, Callable | None]],
    pattern_font_format: Optional[dict],
    default_font_format: Optional[dict],
) -> None:
    """
    Apply styling to a specific pattern within a paragraph text.
    
    This function looks for a specific pattern (like "Source") in the paragraph text
    and applies different font formatting to that pattern vs. the rest of the text.
    """
    text = paragraph.text
    if not text or not pattern:
        return

    pattern_match = re.search(re.escape(pattern), text, re.IGNORECASE)
    
    if not pattern_match:
        apply_nested_paragraph_styling(
            paragraph=paragraph,
            text_parts=[(text, default_font_format)],
            font_mapping=font_mapping,
            default_font_format=default_font_format,
        )
        return

    start_pos = pattern_match.start()
    end_pos = pattern_match.end()
    
    text_parts = []

    if start_pos > 0:
        before_text = text[:start_pos]
        text_parts.append((before_text, default_font_format))

    pattern_text = text[start_pos:end_pos]
    text_parts.append((pattern_text, pattern_font_format))

    if end_pos < len(text):
        after_text = text[end_pos:]
        text_parts.append((after_text, default_font_format))
    
    apply_nested_paragraph_styling(
        paragraph=paragraph,
        text_parts=text_parts,
        font_mapping=font_mapping,
        default_font_format=default_font_format,
    )


def apply_nested_styling_to_paragraphs(
    doc: Document,
    style_names_mapping: dict[str, str],
    font_mapping: dict[str, tuple[str, Callable | None]],
    style_definitions: dict[str, dict[str, str | dict[str, str]]] | None,
    style_attributes_names_mapping: dict[str, str] | None,
) -> None:
    """
    Apply nested styling to paragraphs that have common_pattern_format with font_format.
    
    This function processes paragraphs and applies different font styles to common patterns
    vs. the rest of the text when common_pattern_format includes font_format configuration.
    
    It automatically processes all styles that have the required properties.
    """

    eligible_styles = set()
    if style_definitions and style_attributes_names_mapping:
        for style_key, style_def in style_definitions.items():
            common_pattern_def = style_def.get(
                style_attributes_names_mapping.get("common_pattern_format", "common_pattern_format"),
                {},
            )
            if common_pattern_def.get("font_format"):
                eligible_styles.add(style_names_mapping.get(style_key, style_key))
    
    for paragraph in doc.paragraphs:
        style_name = paragraph.style.name

        if style_name not in eligible_styles:
            continue

        style_def = None
        if style_definitions and style_attributes_names_mapping:
            for style_key, mapped_name in style_names_mapping.items():
                if mapped_name == style_name:
                    style_def = style_definitions.get(style_key)
                    break
        
        if not style_def:
            continue

        common_pattern_def = style_def.get(
            style_attributes_names_mapping.get("common_pattern_format", "common_pattern_format"),
            {},
        )

        if not common_pattern_def.get("font_format"):
            continue

        common_pattern = common_pattern_def.get("pattern", "")
        common_pattern_font_format = common_pattern_def.get("font_format")

        default_font_format = style_def.get(
            style_attributes_names_mapping.get("font_format", "font_format"),
            {},
        )

        apply_pattern_styling_to_paragraph(
            paragraph=paragraph,
            pattern=common_pattern,
            font_mapping=font_mapping,
            pattern_font_format=common_pattern_font_format,
            default_font_format=default_font_format,
        )
