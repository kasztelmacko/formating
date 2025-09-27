from style_mapping import FONT_MAPPING, PARAGRAPH_FORMAT_MAPPING

def apply_style_group(doc, style_group: dict):
    """
    Apply a group of styles from a configuration dictionary to a docx Document.

    style_group: dict
        Keys are style names, values are style definitions (font + paragraph_format + based_on)
    """
    for style_name, style_def in style_group.items():
        try:
            style_obj = doc.styles[style_name]
        except KeyError:
            continue

        if not isinstance(style_def, dict):
            continue

        if "based_on" in style_def:
            try:
                style_obj.base_style = doc.styles[style_def["based_on"]]
            except KeyError:
                pass

        apply_style_properties(style_obj, style_def)


def apply_style_properties(style_obj, style_def: dict):
    """
    Apply font and paragraph formatting from a style definition to a docx style object.
    """
    font_def = style_def.get("font", {})
    para_def = style_def.get("paragraph_format", {})

    if font_def:
        apply_properties(style_obj.font, font_def, FONT_MAPPING)

    if para_def:
        apply_properties(style_obj.paragraph_format, para_def, PARAGRAPH_FORMAT_MAPPING)


def apply_properties(target, data: dict, mapping: dict):
    """
    Apply values from data to target attributes using mapping rules.
    mapping: {"json_key": ("attr_name", converter_function)}
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