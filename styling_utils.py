from xml.etree.ElementTree import Element
from style_mapping import OPENXML_FORMATS, BULLET_CHARACTER_OPTIONS

def _apply_properties(target, data, mapping):
    """
    Apply values from data to target attributes using mapping rules.

    mapping: {
        "json_key": ("attr_name", converter_function)
    }
    """
    for key, (attr, converter) in mapping.items():
        if key not in data or data[key] is None:
            continue
        if converter:
            try:
                value = converter(target, data[key])
            except TypeError:
                value = converter(data[key])
        else:
            value = data[key]

        if "." in attr:
            obj, subattr = attr.split(".", 1)
            setattr(getattr(target, obj), subattr, value)
        else:
            setattr(target, attr, value)


def _clean_paragraph(paragraph, trim_spaces=True):
    """Remove unnecessary blank lines/spaces from a paragraph."""
    if trim_spaces:
        paragraph.text = paragraph.text.lstrip("\n\r ").rstrip("\n\r ")

def _remove_empty_paragraph(paragraph):
    """Remove empty paragraph from the document."""
    if not paragraph.text.strip():
        p_element = paragraph._element
        p_element.getparent().remove(p_element)

def _adjust_bullet_character(doc, bullet_char):
    numbering_xml = doc.part.numbering_part._element
    abstract_nums = numbering_xml.findall(f'.//{{{OPENXML_FORMATS["W"]}}}abstractNum')

    for _, abstract_num in enumerate(abstract_nums):

        levels = abstract_num.findall(f'.//{{{OPENXML_FORMATS["W"]}}}lvl')
        for level in levels:
            lvl_text = level.find(f'{{{OPENXML_FORMATS["W"]}}}lvlText')
            if lvl_text is None:
                lvl_text = Element(f'{{{OPENXML_FORMATS["W"]}}}lvlText')
                level.append(lvl_text)

            lvl_text.set(f'{{{OPENXML_FORMATS["W"]}}}val', BULLET_CHARACTER_OPTIONS[bullet_char])

            rPr = level.find(f'{{{OPENXML_FORMATS["W"]}}}rPr')
            if rPr is not None:
                rFonts = rPr.find(f'{{{OPENXML_FORMATS["W"]}}}rFonts')
                if rFonts is not None:
                    rPr.remove(rFonts)