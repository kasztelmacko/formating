def apply_docx_style_definitions(doc, style_definitions: dict, style_attributes_names_mapping: dict, font_mapping: dict, paragraph_format_mapping: dict):
    """
    Apply a set of style definitions from a configuration dictionary to a docx Document.

    style_definitions: dict
        Keys are style names, values are style definitions (font + paragraph_format + based_on)
    """
    for style_name, style_def in style_definitions.items():
        try:
            style_obj = doc.styles[style_name]
        except KeyError:
            continue

        if not isinstance(style_def, dict):
            continue

        if style_attributes_names_mapping["based_on"] in style_def:
            try:
                style_obj.base_style = doc.styles[style_def[style_attributes_names_mapping["based_on"]]]
            except KeyError:
                pass

        apply_docx_style_attributes(
            style_obj=style_obj, 
            style_def= style_def, 
            style_attributes_names_mapping=style_attributes_names_mapping,
            font_mapping=font_mapping,
            paragraph_format_mapping=paragraph_format_mapping,
        )


def apply_docx_style_attributes(style_obj, style_def: dict, style_attributes_names_mapping: dict, font_mapping: dict, paragraph_format_mapping: dict):
    """
    Apply font and paragraph formatting attributes from a style definition to a docx style object.
    """
    font_def = style_def.get(style_attributes_names_mapping["font_format"], {})
    paragraph_def = style_def.get(style_attributes_names_mapping["paragraph_format"], {})
    
    if font_def:
        map_config_to_docx_attributes(
            target=style_obj.font, 
            config_data=font_def, 
            mapping=font_mapping
        )

    if paragraph_def:
        map_config_to_docx_attributes(
            target=style_obj.paragraph_format, 
            config_data=paragraph_def, 
            mapping=paragraph_format_mapping
        )



def map_config_to_docx_attributes(target, config_data: dict, mapping: dict):
    """
    Map configuration dictionary keys to docx object attributes using mapping rules.

    mapping: {"config_key": ("attribute_name", converter_function)}
    """
    for key, (attr, converter) in mapping.items():
        if key not in config_data or config_data[key] is None:
            continue

        if converter:
            try:
                value = converter(target, config_data[key])
            except TypeError:
                value = converter(config_data[key])
        else:
            value = config_data[key]

        if "." in attr:
            obj, subattr = attr.split(".", 1)
            setattr(getattr(target, obj), subattr, value)
        else:
            setattr(target, attr, value)
