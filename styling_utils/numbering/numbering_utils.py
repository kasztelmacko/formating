import re
from typing import Callable, Pattern

import roman
from docx.document import Document

from config.patterns import BASE_PATTERNS


def arabic_to_roman(num_str: str) -> str:
    """Convert Arabic numerals to Roman numerals."""
    return ".".join(
        roman.toRoman(int(p)) if p.isdigit() else p for p in num_str.split(".")
    )


def roman_to_arabic(roman_str: str) -> str:
    """Convert Roman numerals to Arabic numerals."""
    return ".".join(
        str(roman.fromRoman(p)) if p.isalpha() else p for p in roman_str.split(".")
    )


def expand_common_pattern(common_pattern: str, numbering_format: str = "ARABIC") -> str:
    """Expand a common pattern string into a regex pattern."""
    if not common_pattern:
        return ""

    if "number" not in common_pattern and "." not in common_pattern:
        return common_pattern

    number_type = numbering_format.upper()
    number_pattern = BASE_PATTERNS[
        "roman_number" if number_type == "ROMAN" else "arabic_number"
    ]

    return common_pattern.replace("number", number_pattern)


def remove_all_numbering(
    text: str,
    common_pattern: str = "",
    numbering_format: str = "ARABIC",
    renumbering_regex: dict[str, str] | None = None,
) -> str:
    """Remove all existing numbering from text, including Roman numerals, Arabic numbers, and common patterns.
    This function carefully removes Roman numerals without affecting letters in normal words."""
    if not text.strip():
        return text

    if common_pattern:
        expanded_pattern = expand_common_pattern(common_pattern, numbering_format)

        if not any(char in expanded_pattern for char in ["\\", "(", ")", "[", "]"]):
            common_word_pattern = renumbering_regex["common_word_pattern"].format(
                common_word=re.escape(expanded_pattern.strip())
            )
            text = re.sub(common_word_pattern, "", text).strip()
        else:
            if "." in expanded_pattern:
                precise_pattern = (
                    renumbering_regex["pattern_start"]
                    + expanded_pattern
                    + renumbering_regex["pattern_end"]
                )
            else:
                precise_pattern = (
                    renumbering_regex["word_boundary"]
                    + expanded_pattern
                    + renumbering_regex["word_boundary"]
                )
            text = re.sub(precise_pattern, "", text).strip()

    roman_patterns = [
        renumbering_regex["roman_uppercase"],
        renumbering_regex["roman_lowercase"],
    ]

    for pattern in roman_patterns:
        text = re.sub(pattern, "", text).strip()

    text = re.sub(renumbering_regex["arabic_numbers"], "", text).strip()
    text = re.sub(renumbering_regex["extra_spaces"], " ", text).strip()

    text = re.sub(renumbering_regex["leading_punctuation"], "", text)
    text = re.sub(renumbering_regex["trailing_punctuation"], "", text)
    text = re.sub(renumbering_regex["extra_spaces"], " ", text).strip()

    return text


def apply_numbering_to_text(
    text: str,
    new_numbering: str,
    numbering_format: str,
    numbering_side: str,
    separator: str = " ",
    chapter_section_numbering_regex: dict[str, str] | None = None,
    common_pattern: str = "",
    common_pattern_side: str = "LEFT",
    common_pattern_separator: str = " ",
    renumbering_regex: dict[str, str] | None = None,
) -> str:
    """Apply new numbering to text by first removing all existing numbering, then applying the new numbering."""
    cleaned_text = remove_all_numbering(
        text, common_pattern, numbering_format, renumbering_regex
    )

    if common_pattern:
        expanded_pattern = expand_common_pattern(common_pattern, numbering_format)

        if not any(char in expanded_pattern for char in ["\\", "(", ")", "[", "]"]):
            if common_pattern_side.upper() == "LEFT":
                new_numbering = (
                    f"{expanded_pattern}{common_pattern_separator}{new_numbering}"
                )
            else:
                new_numbering = (
                    f"{new_numbering}{common_pattern_separator}{expanded_pattern}"
                )
        else:
            pass

    if numbering_side == "LEFT":
        return f"{new_numbering}{separator}{cleaned_text}"
    else:
        return f"{cleaned_text}{separator}{new_numbering}"


def process_paragraph_text(
    text: str,
    numbering_format: str,
    numbering_side: str,
    regex_patterns: dict[str, Pattern[str]],
    separator: str = " ",
) -> str:
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

        convert_number = (
            arabic_to_roman if numbering_format == "ROMAN" else roman_to_arabic
        )
        new_numbering = convert_number(source_num)

        return apply_numbering_to_text(
            text, new_numbering, numbering_format, numbering_side, separator
        )

    except Exception:
        return text


def update_paragraph_numbering(
    text: str,
    chapter_num: int,
    subchapter_level_2_num: int | None = None,
    subchapter_level_3_num: int | None = None,
    style_definitions: dict[str, dict[str, str | dict[str, str]]] | None = None,
    style_attributes_names_mapping: dict[str, str] | None = None,
    style_name: str | None = None,
    chapter_section_numbering_regex: dict[str, str] | None = None,
    common_pattern: str = "",
    common_pattern_side: str = "LEFT",
    common_pattern_separator: str = " ",
    renumbering_regex: dict[str, str] | None = None,
) -> str:
    """Update paragraph text with new numbering based on the hierarchy level."""
    if not text.strip():
        return text

    numbering_type = "ARABIC"
    numbering_side = "LEFT"
    separator = " "

    if style_definitions and style_attributes_names_mapping and style_name:
        style_def = style_definitions.get(style_name)
        if style_def:
            numbering_def = style_def.get(
                style_attributes_names_mapping.get(
                    "numbering_format", "numbering_format"
                ),
                {},
            )
            numbering_type = numbering_def.get("type", "ARABIC")
            numbering_side = numbering_def.get("side", "LEFT")
            separator = numbering_def.get("separator", " ")

            if not common_pattern:
                common_pattern_def = style_def.get(
                    style_attributes_names_mapping.get(
                        "common_pattern_format", "common_pattern_format"
                    ),
                    {},
                )
                common_pattern = common_pattern_def.get("pattern", "")
                common_pattern_side = common_pattern_def.get("side", "LEFT")
                common_pattern_separator = common_pattern_def.get("separator", " ")

    if subchapter_level_3_num is not None:
        base_numbering = (
            f"{chapter_num}.{subchapter_level_2_num}.{subchapter_level_3_num}"
        )
    elif subchapter_level_2_num is not None:
        base_numbering = f"{chapter_num}.{subchapter_level_2_num}"
    else:
        base_numbering = str(chapter_num)

    if numbering_type.upper() == "ROMAN":
        new_numbering = arabic_to_roman(base_numbering)
    else:
        new_numbering = base_numbering

    return apply_numbering_to_text(
        text,
        new_numbering,
        numbering_type,
        numbering_side,
        separator,
        chapter_section_numbering_regex,
        common_pattern,
        common_pattern_side,
        common_pattern_separator,
        renumbering_regex,
    )


def apply_chapter_based_numbering(
    doc: Document,
    style_names_mapping: dict[str, str],
    style_definitions: dict[str, dict[str, str | dict[str, str]]] | None = None,
    style_attributes_names_mapping: dict[str, str] | None = None,
    chapter_section_numbering_regex: dict[str, str] | None = None,
    target_styles: list[str] | None = None,
    use_common_pattern: bool = True,
    renumbering_regex: dict[str, str] | None = None,
) -> dict[str, int]:
    """Apply chapter-based numbering for specified styles."""
    current_chapter = 0
    counters = dict.fromkeys(target_styles, 0) if target_styles else {}

    in_chapter = False
    chapter_numbering_applied = False

    for paragraph in doc.paragraphs:
        style_name = paragraph.style.name

        if style_name == style_names_mapping.get("chapter_titles"):
            if not chapter_numbering_applied:
                current_chapter += 1
                for style in counters:
                    counters[style] = 0
                in_chapter = True
                chapter_numbering_applied = True
        else:
            chapter_numbering_applied = False

        if (
            target_styles
            and style_name
            in [style_names_mapping.get(style) for style in target_styles]
            and in_chapter
        ):
            target_style = None
            for style in target_styles:
                if style_name == style_names_mapping.get(style):
                    target_style = style
                    break

            if target_style:
                counters[target_style] += 1
                new_numbering = f"{current_chapter}.{counters[target_style]}"

                style_def = (
                    style_definitions.get(target_style, {}) if style_definitions else {}
                )
                numbering_def = style_def.get(
                    style_attributes_names_mapping.get(
                        "numbering_format", "numbering_format"
                    ),
                    {},
                )

                common_pattern = ""
                common_pattern_side = "LEFT"
                common_pattern_separator = " "

                if use_common_pattern:
                    common_pattern_def = style_def.get(
                        style_attributes_names_mapping.get(
                            "common_pattern_format", "common_pattern_format"
                        ),
                        {},
                    )
                    common_pattern = common_pattern_def.get("pattern", "")
                    common_pattern_side = common_pattern_def.get("side", "LEFT")
                    common_pattern_separator = common_pattern_def.get("separator", " ")

                paragraph.text = apply_numbering_to_text(
                    paragraph.text,
                    new_numbering,
                    numbering_def.get("type", "ARABIC"),
                    numbering_def.get("side", "LEFT"),
                    numbering_def.get("separator", " "),
                    chapter_section_numbering_regex,
                    common_pattern,
                    common_pattern_side,
                    common_pattern_separator,
                    renumbering_regex,
                )

    return counters