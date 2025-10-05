import contextlib
from typing import Callable

from docx.document import Document
from docx.styles.style import BaseStyle
from docx.text.font import Font
from docx.text.paragraph import ParagraphFormat


def apply_docx_style_definitions(
    doc: Document,
    style_definitions: dict[str, dict[str, str | dict[str, str]]],
    style_attributes_names_mapping: dict[str, str],
    font_mapping: dict[str, tuple[str, Callable | None]],
    paragraph_format_mapping: dict[str, tuple[str, Callable | None]],
) -> None:
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
            with contextlib.suppress(KeyError):
                style_obj.base_style = doc.styles[
                    style_def[style_attributes_names_mapping["based_on"]]
                ]

        apply_docx_style_attributes(
            style_obj=style_obj,
            style_def=style_def,
            style_attributes_names_mapping=style_attributes_names_mapping,
            font_mapping=font_mapping,
            paragraph_format_mapping=paragraph_format_mapping,
        )


def apply_docx_style_attributes(
    style_obj: BaseStyle,
    style_def: dict[str, str | dict[str, str]],
    style_attributes_names_mapping: dict[str, str],
    font_mapping: dict[str, tuple[str, Callable | None]],
    paragraph_format_mapping: dict[str, tuple[str, Callable | None]],
) -> None:
    """
    Apply font and paragraph formatting attributes from a style definition to a docx style object.
    """
    font_def = style_def.get(style_attributes_names_mapping["font_format"], {})
    paragraph_def = style_def.get(
        style_attributes_names_mapping["paragraph_format"], {}
    )

    if font_def:
        map_config_to_docx_attributes(
            target=style_obj.font, config_data=font_def, mapping=font_mapping
        )

    if paragraph_def:
        map_config_to_docx_attributes(
            target=style_obj.paragraph_format,
            config_data=paragraph_def,
            mapping=paragraph_format_mapping,
        )


def map_config_to_docx_attributes(
    target: Font | ParagraphFormat,
    config_data: dict[str, str | int | float | bool],
    mapping: dict[str, tuple[str, Callable | None]],
) -> None:
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
