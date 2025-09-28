from xml.etree.ElementTree import Element
from style_mapping import OPENXML_FORMATS, BULLET_CHARACTER_OPTIONS
from docx.oxml.ns import qn

def w_tag(tag: str) -> str:
    return f'{{{OPENXML_FORMATS["W"]}}}{tag}'

def ensure_child(parent: Element, tag: str) -> Element:
    child = parent.find(tag)
    if child is None:
        child = Element(tag)
        parent.append(child)
    return child

def apply_list_indentation(level: Element, left: int, hanging: int):
    """
    Apply indentation on a numbering level (<w:lvl>).
    """
    pPr = ensure_child(level, w_tag("pPr"))
    ind = ensure_child(pPr, w_tag("ind"))
    ind.set(w_tag("left"), str(left))
    ind.set(w_tag("hanging"), str(hanging))

def update_bullet_characters(doc, list_config: dict):
    """
    Update bullet characters and indentation in the document based on list_config.
    Termination characters are applied later to paragraph text.
    """
    bullet_char = list_config.get("bullet_char")
    indent_cfg = list_config.get("indent", {})
    
    left = indent_cfg.get("left")
    hanging = indent_cfg.get("hanging")

    numbering_xml = doc.part.numbering_part._element
    abstract_nums = numbering_xml.findall(f'.//{w_tag("abstractNum")}')

    for abstract_num in abstract_nums:
        levels = abstract_num.findall(f'.//{w_tag("lvl")}')
        for level in levels:
            apply_list_indentation(level, left, hanging)

            if bullet_char and bullet_char in BULLET_CHARACTER_OPTIONS:
                lvl_text = ensure_child(level, w_tag("lvlText"))
                lvl_text.set(w_tag("val"), BULLET_CHARACTER_OPTIONS[bullet_char])

            rPr = level.find(w_tag("rPr"))
            if rPr is not None:
                rFonts = rPr.find(w_tag("rFonts"))
                if rFonts is not None:
                    rPr.remove(rFonts)

def apply_list_termination_characters(doc, list_config: dict):
    """
    Apply termination characters to list items based on the configuration.
    """
    termination_cfg = list_config.get("list_item_termination", {})
    intermediate_char = termination_cfg.get("intermediate", "")
    last_item_char = termination_cfg.get("last_item", "")
    
    if not intermediate_char and not last_item_char:
        return
    
    list_paragraphs_info = find_all_list_paragraphs(doc)
    if not list_paragraphs_info:
        return
    _apply_termination_to_list_groups(list_paragraphs_info, intermediate_char, last_item_char)


def _apply_termination_to_list_groups(list_paragraphs_info, intermediate_char, last_item_char):
    """
    Apply termination characters to grouped list paragraphs.
    """
    current_group = []
    current_num_id = None
    
    for para_info in list_paragraphs_info:
        _, num_id, level = para_info
        
        if num_id != current_num_id or (current_group and level == 0 and current_group[-1][2] > 0):
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
    
    for _, (paragraph, _, _) in enumerate(group_paragraphs[:-1]):
        _apply_termination_character(paragraph, intermediate_char)
    
    last_paragraph, _, _ = group_paragraphs[-1]
    _apply_termination_character(last_paragraph, last_item_char)


def _apply_termination_character(paragraph, termination_char):
    """
    Apply a termination character to a single paragraph if needed.
    """
    if not termination_char:
        return
    
    text = paragraph.text.strip()
    if not text:
        return
    
    cleaned_text = text.rstrip('.;,:')
    cleaned_text = cleaned_text.strip()
    
    if cleaned_text:
        paragraph.text = f"{cleaned_text}{termination_char}"


def _get_numbering_info(paragraph):
    """
    Get the numbering ID and level for a paragraph in one operation.
    Returns a tuple (num_id, level) or (None, 0) if not found.
    """
    num_pr = paragraph._p.find(f'.//{w_tag("numPr")}')
    if num_pr is None:
        return None, 0
    
    num_id, level = None, 0
    num_id_elem = num_pr.find(f'.//{w_tag("numId")}')
    if num_id_elem is not None:
        num_id = num_id_elem.get(w_tag("val"))
    
    ilvl_elem = num_pr.find(f'.//{w_tag("ilvl")}')
    if ilvl_elem is not None:
        level = int(ilvl_elem.get(w_tag("val")))
    
    return num_id, level

def find_all_list_paragraphs(doc):
    """
    Find all paragraphs that are part of lists (bulleted or numbered) in the document.
    Returns a list of tuples (paragraph, num_id, level).
    """
    list_paragraphs = []
    for paragraph in doc.paragraphs:
        num_id, level = _get_numbering_info(paragraph)
        if num_id is not None:
            list_paragraphs.append((paragraph, num_id, level))
    return list_paragraphs
