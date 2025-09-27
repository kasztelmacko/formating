from xml.etree.ElementTree import Element
from style_mapping import OPENXML_FORMATS, BULLET_CHARACTER_OPTIONS

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
    Update bullet characters in the document based on list_config.
    """
    bullet_char = list_config.get("bullet_char")
    if not bullet_char or bullet_char not in BULLET_CHARACTER_OPTIONS:
        return

    indent_cfg = list_config.get("indent", {})
    left = indent_cfg.get("left")
    hanging = indent_cfg.get("hanging")

    numbering_xml = doc.part.numbering_part._element
    abstract_nums = numbering_xml.findall(f'.//{w_tag("abstractNum")}')

    for abstract_num in abstract_nums:
        levels = abstract_num.findall(f'.//{w_tag("lvl")}')
        for level in levels:
            apply_list_indentation(level, left, hanging)

            lvl_text = ensure_child(level, w_tag("lvlText"))
            lvl_text.set(w_tag("val"), BULLET_CHARACTER_OPTIONS[bullet_char])

            rPr = level.find(w_tag("rPr"))
            if rPr is not None:
                rFonts = rPr.find(w_tag("rFonts"))
                if rFonts is not None:
                    rPr.remove(rFonts)
