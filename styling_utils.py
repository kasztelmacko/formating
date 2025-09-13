from docx.shared import RGBColor
from docx.oxml.ns import qn

def _apply_properties(target, data, mapping):
    """
    Apply values from data to target attributes using mapping rules.

    mapping: {
        "json_key": ("attr_name", converter_function)
    }

    If a key is missing or its value is None, the property is not modified.
    """
    for key, (attr, converter) in mapping.items():
        if key not in data or data[key] is None:
            continue
        value = converter(data[key]) if converter else data[key]
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

def _set_font_name(font, name: str):
    if not name:
        return
    rFonts = font.element.rPr.rFonts
    rFonts.set(qn("w:eastAsia"), name)
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:cs"), name)