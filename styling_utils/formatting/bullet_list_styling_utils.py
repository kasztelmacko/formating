from xml.etree.ElementTree import Element

def ensure_child(parent: Element, tag: str) -> Element:
    """Create or find a child element with the given tag."""
    child = parent.find(tag)
    if child is None:
        child = Element(tag)
        parent.append(child)
    return child

def apply_list_indentation(level: Element, left: int, hanging: int, w_tags: dict):
    """
    Apply indentation on a numbering level (<w:lvl>).
    """ 
    pPr = ensure_child(level, w_tags['pPr'])
    ind = ensure_child(pPr, w_tags['ind'])
    ind.set(w_tags['left'], str(left))
    ind.set(w_tags['hanging'], str(hanging))

def apply_bullet_character_updates(doc, list_config: dict, bullet_character_options: dict, w_tags: dict):
    """
    Update bullet characters and indentation in the document based on list_config.
    Termination characters are applied later to paragraph text.
    """
    if not list_config:
        return
        
    bullet_char = list_config.get("bullet_char")
    indent_cfg = list_config.get("indent", {})
    
    left = indent_cfg.get("left")
    hanging = indent_cfg.get("hanging")
 
    if not bullet_char and left is None and hanging is None:
        return

    numbering_xml = doc.part.numbering_part._element
    abstract_nums = numbering_xml.findall(f'.//{w_tags["abstractNum"]}')

    for abstract_num in abstract_nums:
        levels = abstract_num.findall(f'.//{w_tags["lvl"]}')
        for level in levels:
            if left is not None and hanging is not None:
                apply_list_indentation(level, left, hanging, w_tags)

            if bullet_char and bullet_char in bullet_character_options:
                lvl_text = ensure_child(level, w_tags['lvlText'])
                lvl_text.set(w_tags['val'], bullet_character_options[bullet_char])

            _remove_bullet_font_formatting(level, w_tags)

def apply_list_termination_characters(doc, list_config: dict, w_tags: dict):
    """
    Apply termination characters to list items based on the configuration.
    """
    if not list_config:
        return
        
    termination_cfg = list_config.get("list_item_termination", {})
    intermediate_char = termination_cfg.get("intermediate", "")
    last_item_char = termination_cfg.get("last_item", "")
 
    if not intermediate_char and not last_item_char:
        return
    
    list_paragraphs_info = find_all_list_paragraphs(doc, w_tags)
    if not list_paragraphs_info:
        return
        
    _apply_termination_to_list_groups(list_paragraphs_info, intermediate_char, last_item_char)


def _apply_termination_to_list_groups(list_paragraphs_info, intermediate_char, last_item_char):
    """
    Apply termination characters to grouped list paragraphs.
    """
    if not list_paragraphs_info:
        return
        
    current_group = []
    current_num_id = None
    
    for para_info in list_paragraphs_info:
        _, num_id, level = para_info

        if (num_id != current_num_id or 
            (current_group and level == 0 and current_group[-1][2] > 0)):
            
            if current_group:
                _apply_termination_to_single_group(current_group, intermediate_char, last_item_char)
            
            current_group = [para_info]
            current_num_id = num_id
        else:
            current_group.append(para_info)

    if current_group:
        _apply_termination_to_single_group(current_group, intermediate_char, last_item_char)


def _apply_termination_to_single_group(group_paragraphs, intermediate_char, last_item_char):
    """
    Apply termination characters to a single list group.
    """
    if not group_paragraphs:
        return

    if intermediate_char:
        for paragraph, _, _ in group_paragraphs[:-1]:
            _apply_termination_character(paragraph, intermediate_char)

    if last_item_char and group_paragraphs:
        last_paragraph, _, _ = group_paragraphs[-1]
        _apply_termination_character(last_paragraph, last_item_char)


def _apply_termination_character(paragraph, termination_char):
    """
    Apply a termination character to a single paragraph if needed.
    """
    if not termination_char or not paragraph.text:
        return
    
    text = paragraph.text.strip()
    if not text:
        return

    cleaned_text = text.rstrip('.;,:').strip()
    
    if cleaned_text:
        paragraph.text = f"{cleaned_text}{termination_char}"


def _get_numbering_info(paragraph, w_tags: dict):
    """
    Get the numbering ID and level for a paragraph in one operation.
    Returns a tuple (num_id, level) or (None, 0) if not found.
    """
    num_pr = paragraph._p.find(f'.//{w_tags["numPr"]}')
    if num_pr is None:
        return None, 0
    
    num_id, level = None, 0
 
    num_id_elem = num_pr.find(f'.//{w_tags["numId"]}')
    if num_id_elem is not None:
        num_id = num_id_elem.get(w_tags["val"])
 
    ilvl_elem = num_pr.find(f'.//{w_tags["ilvl"]}')
    if ilvl_elem is not None:
        try:
            level = int(ilvl_elem.get(w_tags["val"]))
        except (ValueError, TypeError):
            level = 0
    
    return num_id, level

def find_all_list_paragraphs(doc, w_tags: dict):
    """
    Find all paragraphs that are part of lists (bulleted or numbered) in the document.
    Returns a list of tuples (paragraph, num_id, level).
    """
    list_paragraphs = []
    
    for paragraph in doc.paragraphs:
        num_id, level = _get_numbering_info(paragraph, w_tags)
        if num_id is not None:
            list_paragraphs.append((paragraph, num_id, level))
    
    return list_paragraphs


def _remove_bullet_font_formatting(level: Element, w_tags: dict):
    """
    Remove font formatting from bullet level to ensure consistent appearance.
    """
    rPr = level.find(w_tags['rPr'])
    if rPr is not None:
        rFonts = rPr.find(w_tags['rFonts'])
        if rFonts is not None:
            rPr.remove(rFonts)
