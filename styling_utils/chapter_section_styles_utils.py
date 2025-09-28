from style_mapping import _arabic_to_roman, _roman_to_arabic
import re

def enforce_chapter_page_breaks(doc, style_names_mapping):
    """
    Ensure only the first paragraph of each 'chapter_titles' block starts on a new page.
    """
    page_break_applied = False

    for paragraph in doc.paragraphs:
        if paragraph.style.name == style_names_mapping["chapter_titles"]:
            if not page_break_applied:
                paragraph.paragraph_format.page_break_before = True
                page_break_applied = True
        else:
            page_break_applied = False

def adjust_chapter_section_numbering_format(
    doc,
    style_definitions: dict,
    style_attributes_names_mapping: dict,
    chapter_section_numbering_regex: dict
):
    """
    Adjust numbering in chapter/section titles based on YAML config.
    - numbering_format: { type: ROMAN|ARABIC, side: LEFT|RIGHT, separator: " " }
    """

    for paragraph in doc.paragraphs:
        style_name = paragraph.style.name
        style_def = style_definitions.get(style_name)

        if not style_def:
            continue

        numbering_def = style_def.get(style_attributes_names_mapping["numbering_format"], {})
        numbering_type = numbering_def.get("type")
        numbering_side = numbering_def.get("side")
        separator = numbering_def.get("separator", " ")

        if not numbering_type or not numbering_side:
            continue

        processed_text = _process_paragraph_text(
            paragraph.text.strip(),
            numbering_type.upper(),
            numbering_side.upper(),
            chapter_section_numbering_regex,
            separator
        )
        
        if processed_text != paragraph.text:
            paragraph.text = " ".join(processed_text.split())

def _process_paragraph_text(text, numbering_format, numbering_side, regex_patterns, separator=" "):
    """Process a single paragraph's text to convert numbering."""
    
    pattern_key = f"{numbering_format.lower()}_{numbering_side.lower()}"
    pattern = regex_patterns.get(pattern_key)
    
    if not pattern:
        return text

    match = pattern.match(text) if numbering_side == "LEFT" else pattern.search(text)
    if not match:
        return text

    try:
        number_group, separator_group = (1, 2) if numbering_side == "LEFT" else (2, 1)

        source_num = match.group(number_group)
        sep = (match.group(separator_group) if separator_group <= match.lastindex else "") or separator
        
        convert_number = _arabic_to_roman if numbering_format == "ROMAN" else _roman_to_arabic
        new_numbering = convert_number(source_num)

        if numbering_side == "LEFT":
            text_before = text[:match.start(number_group)]
            text_after = text[match.end(separator_group) if separator_group <= match.lastindex else match.end(number_group):]
            return f"{text_before}{new_numbering}{sep}{text_after}"
        else:
            text_before = text[:match.start(separator_group) if separator_group <= match.lastindex else match.start(number_group)]
            text_after = text[match.end(number_group):]
            return f"{text_before}{sep}{new_numbering}{text_after}"

    except Exception:
        return text

