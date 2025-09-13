from docx.shared import RGBColor, Pt
from docx.oxml.ns import qn

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


def _hex_to_rgbcolor(hex_str):
    """Convert '#RRGGBB' string into docx RGBColor."""
    hex_str = hex_str.lstrip("#")
    r, g, b = (int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return RGBColor(r, g, b)

def _resolve_enum(enum_class, name):
    """Get enum value from its name (string)."""
    return getattr(enum_class, name)

def _clean_paragraph(paragraph, trim_spaces=True):
    """Remove unnecessary blank lines/spaces from a paragraph."""
    if trim_spaces:
        paragraph.text = paragraph.text.lstrip("\n\r ").rstrip("\n\r ")


def _remove_empty_paragraph(paragraph):
    """Remove empty paragraph from the document."""
    if not paragraph.text.strip():
        p_element = paragraph._element
        p_element.getparent().remove(p_element)
