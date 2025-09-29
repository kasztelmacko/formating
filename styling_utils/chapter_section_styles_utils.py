from style_mapping import _arabic_to_roman, _roman_to_arabic, CHAPTER_SECTION_NUMBERING_REGEX

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
        number_group, _ = (1, 2) if numbering_side == "LEFT" else (2, 1)

        source_num = match.group(number_group)
        
        convert_number = _arabic_to_roman if numbering_format == "ROMAN" else _roman_to_arabic
        new_numbering = convert_number(source_num)

        return _apply_numbering_to_text(text, new_numbering, numbering_format, numbering_side, separator)

    except Exception:
        return text


def _apply_numbering_to_text(text, new_numbering, numbering_format, numbering_side, separator=" "):
    """
    Apply new numbering to text using the same logic as _process_paragraph_text.
    This function handles both LEFT and RIGHT side numbering and uses the proper regex patterns.
    
    Args:
        text: Original text
        new_numbering: The new numbering to apply
        numbering_format: "ROMAN" or "ARABIC"
        numbering_side: "LEFT" or "RIGHT"
        separator: Separator to use
    
    Returns:
        Updated text with new numbering applied
    """
    pattern_key = f"{numbering_format.lower()}_{numbering_side.lower()}"
    pattern = CHAPTER_SECTION_NUMBERING_REGEX.get(pattern_key)
    
    if not pattern:
        return f"{new_numbering}{separator}{text}"
    
    match = pattern.match(text) if numbering_side == "LEFT" else pattern.search(text)
    if not match:
        if numbering_side == "LEFT":
            return f"{new_numbering}{separator}{text}"
        else:
            return f"{text}{separator}{new_numbering}"
    
    try:
        number_group, separator_group = (1, 2) if numbering_side == "LEFT" else (2, 1)
        
        sep = (match.group(separator_group) if separator_group <= match.lastindex else "") or separator
        
        if numbering_side == "LEFT":
            text_before = text[:match.start(number_group)]
            text_after = text[match.end(separator_group) if separator_group <= match.lastindex else match.end(number_group):]
            return f"{text_before}{new_numbering}{sep}{text_after}"
        else:
            text_before = text[:match.start(separator_group) if separator_group <= match.lastindex else match.start(number_group)]
            text_after = text[match.end(number_group):]
            return f"{text_before}{sep}{new_numbering}{text_after}"
    
    except Exception:
        return f"{new_numbering}{separator}{text}"


def adjust_section_numbering_order(doc, style_names_mapping, style_definitions=None, style_attributes_names_mapping=None):
    """
    Adjust section numbering based on hierarchy:
    1. Find first paragraph with style chapter_titles and assign current_chapter = 1
    2. Find all subchapter_titles_level_2 until next chapter_titles and assign them 
       current_chapter = current_chapter and subchapter_titles_level_2 grows by one
    3. Find all subchapter_titles_level_3 until next subchapter_titles_level_2 and assign them
       current_chapter = current_chapter, subchapter_titles_level_2 = subchapter_titles_level_2,
       and subchapter_titles_level_3 grows by one
    """

    current_chapter = 0
    current_subchapter_level_2 = 0
    current_subchapter_level_3 = 0
    
    in_chapter = False
    chapter_numbering_applied = False
    
    for paragraph in doc.paragraphs:
        style_name = paragraph.style.name
        
        if style_name == style_names_mapping["chapter_titles"]:
            if not chapter_numbering_applied:
                current_chapter += 1
                current_subchapter_level_2 = 0
                current_subchapter_level_3 = 0
                in_chapter = True
                chapter_numbering_applied = True
                
                paragraph.text = _update_paragraph_numbering(
                    paragraph.text, current_chapter, None, None, 
                    style_definitions, style_attributes_names_mapping, style_name
                )
            
        elif style_name == style_names_mapping["subchapter_titles_level_2"]:
            if in_chapter:
                current_subchapter_level_2 += 1
                current_subchapter_level_3 = 0

                paragraph.text = _update_paragraph_numbering(
                    paragraph.text, current_chapter, current_subchapter_level_2, None,
                    style_definitions, style_attributes_names_mapping, style_name
                )
            
        elif style_name == style_names_mapping["subchapter_titles_level_3"]:
            if in_chapter and current_subchapter_level_2 > 0:
                current_subchapter_level_3 += 1

                paragraph.text = _update_paragraph_numbering(
                    paragraph.text, current_chapter, current_subchapter_level_2, current_subchapter_level_3,
                    style_definitions, style_attributes_names_mapping, style_name
                )
        else:
            chapter_numbering_applied = False


def _update_paragraph_numbering(text, chapter_num, subchapter_level_2_num, subchapter_level_3_num, 
                               style_definitions=None, style_attributes_names_mapping=None, style_name=None):
    """
    Update paragraph text with new numbering based on the hierarchy level.
    
    Args:
        text: Original paragraph text
        chapter_num: Chapter number (always provided)
        subchapter_level_2_num: Level 2 subchapter number (None if not applicable)
        subchapter_level_3_num: Level 3 subchapter number (None if not applicable)
        style_definitions: Dictionary containing style definitions
        style_attributes_names_mapping: Mapping for style attribute names
        style_name: Name of the current style
    
    Returns:
        Updated text with new numbering
    """
    if not text.strip():
        return text

    if style_definitions and style_attributes_names_mapping and style_name:
        style_def = style_definitions.get(style_name)
        if style_def:
            numbering_def = style_def.get(style_attributes_names_mapping.get("numbering_format", "numbering_format"), {})
            numbering_type = numbering_def.get("type", "ARABIC")
            numbering_side = numbering_def.get("side", "LEFT")
            separator = numbering_def.get("separator", " ")

    if subchapter_level_3_num is not None:
        base_numbering = f"{chapter_num}.{subchapter_level_2_num}.{subchapter_level_3_num}"
    elif subchapter_level_2_num is not None:
        base_numbering = f"{chapter_num}.{subchapter_level_2_num}"
    else:
        base_numbering = str(chapter_num)

    if numbering_type.upper() == "ROMAN":
        new_numbering = _arabic_to_roman(base_numbering)
    else:
        new_numbering = base_numbering

    return _apply_numbering_to_text(text, new_numbering, numbering_type, numbering_side, separator)

