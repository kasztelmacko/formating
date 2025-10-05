from xml.etree.ElementTree import Element

from docx.document import Document
from docx.text.paragraph import Paragraph


def ensure_child(parent: Element, tag: str) -> Element:
    """Create or find a child element with the given tag."""
    child = parent.find(tag)
    if child is None:
        child = Element(tag)
        parent.append(child)
    return child


def apply_list_indentation(
    level: Element, left: int, hanging: int, w_tags: dict[str, str]
) -> None:
    """
    Apply indentation on a numbering level (<w:lvl>).
    """
    pPr = ensure_child(level, w_tags["pPr"])
    ind = ensure_child(pPr, w_tags["ind"])
    ind.set(w_tags["left"], str(left))
    ind.set(w_tags["hanging"], str(hanging))


def apply_bullet_character_updates(
    doc: Document,
    list_config: dict[str, str | dict[str, str | int]],
    bullet_character_options: dict[str, str],
    w_tags: dict[str, str],
    default_nested_config: dict[str, dict[str, str | int]] | None,
    default_indentation: dict[str, int] | None,
) -> None:
    """
    Update bullet characters and indentation in the document based on list_config.
    Uses bullet_list_level_X configuration with inheritance from parent levels.
    Termination characters are applied later to paragraph text.
    """
    if not list_config:
        return

    numbering_xml = doc.part.numbering_part._element
    abstract_nums = numbering_xml.findall(f'.//{w_tags["abstractNum"]}')

    bullet_levels = _extract_bullet_level_configs(list_config)
    _apply_bullet_configuration_with_inheritance(
        doc,
        bullet_levels,
        bullet_character_options,
        w_tags,
        abstract_nums,
        default_nested_config,
        default_indentation,
    )


def apply_list_termination_characters(
    doc: Document, list_config: dict[str, str | dict[str, str]], w_tags: dict[str, str]
) -> None:
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

    _apply_termination_to_list_groups(
        list_paragraphs_info, intermediate_char, last_item_char
    )


def _apply_termination_to_list_groups(
    list_paragraphs_info: list[tuple[Paragraph, str, int]],
    intermediate_char: str,
    last_item_char: str,
) -> None:
    """
    Apply termination characters to grouped list paragraphs.
    """
    if not list_paragraphs_info:
        return

    current_group = []
    current_num_id = None

    for para_info in list_paragraphs_info:
        _, num_id, level = para_info

        if num_id != current_num_id or (
            current_group and level == 0 and current_group[-1][2] > 0
        ):
            if current_group:
                _apply_termination_to_single_group(
                    current_group, intermediate_char, last_item_char
                )

            current_group = [para_info]
            current_num_id = num_id
        else:
            current_group.append(para_info)

    if current_group:
        _apply_termination_to_single_group(
            current_group, intermediate_char, last_item_char
        )


def _apply_termination_to_single_group(
    group_paragraphs: list[tuple[Paragraph, str, int]],
    intermediate_char: str,
    last_item_char: str,
) -> None:
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


def _apply_termination_character(paragraph: Paragraph, termination_char: str) -> None:
    """
    Apply a termination character to a single paragraph if needed.
    """
    if not termination_char or not paragraph.text:
        return

    text = paragraph.text.strip()
    if not text:
        return

    cleaned_text = text.rstrip(".;,:").strip()

    if cleaned_text:
        paragraph.text = f"{cleaned_text}{termination_char}"


def _get_numbering_info(
    paragraph: Paragraph, w_tags: dict[str, str]
) -> tuple[str | None, int]:
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


def find_all_list_paragraphs(
    doc: Document, w_tags: dict[str, str]
) -> list[tuple[Paragraph, str, int]]:
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


def _extract_bullet_level_configs(
    list_config: dict[str, str | dict[str, str | int]],
) -> dict[int, dict[str, str | int]]:
    """
    Extract bullet list level configurations from the config.
    Looks for bullet_list_level_0, bullet_list_level_1, etc.
    """
    bullet_levels = {}

    for key, value in list_config.items():
        if key.startswith("bullet_list_level_"):
            try:
                level_num = int(key.split("_")[-1])
                if 0 <= level_num <= 8:
                    bullet_levels[level_num] = value
            except (ValueError, IndexError):
                continue

    return bullet_levels


def _apply_bullet_configuration_with_inheritance(
    doc: Document,
    bullet_levels: dict[int, dict[str, str | int]],
    bullet_character_options: dict[str, str],
    w_tags: dict[str, str],
    abstract_nums: list[Element],
    default_nested_config: dict[str, dict[str, str | int]] | None,
    default_indentation: dict[str, int] | None,
) -> None:
    """
    Apply bullet configuration with inheritance from parent levels.
    If a level doesn't have a bullet_char specified, it inherits from the parent level.
    If indentation is not specified, uses default indentation values.
    """
    for abstract_num in abstract_nums:
        levels = abstract_num.findall(f'.//{w_tags["lvl"]}')

        for level in levels:
            level_num = _get_level_number(level, w_tags)

            level_config = _get_level_config_with_inheritance(
                level_num, bullet_levels, default_nested_config, default_indentation
            )

            if not level_config:
                continue

            left = level_config.get("left")
            hanging = level_config.get("hanging")
            if left is not None and hanging is not None:
                apply_list_indentation(level, left, hanging, w_tags)

            bullet_char = level_config.get("bullet_char")
            if bullet_char and bullet_char in bullet_character_options:
                lvl_text = ensure_child(level, w_tags["lvlText"])
                lvl_text.set(w_tags["val"], bullet_character_options[bullet_char])

            _remove_bullet_font_formatting(level, w_tags)


def _get_level_config_with_inheritance(
    level_num: int,
    bullet_levels: dict[int, dict[str, str | int]],
    default_nested_config: dict[str, dict[str, str | int]] | None,
    default_indentation: dict[str, int] | None,
) -> dict[str, str | int]:
    """
    Get configuration for a level with inheritance from parent levels.
    If bullet_char is not specified, inherit from the nearest parent level.
    If indentation is not specified, use default indentation values.
    """
    level_config = {}

    if default_nested_config and level_num in default_nested_config:
        default_config = default_nested_config[level_num]
        level_config.update(
            {
                "left": default_config.get("left"),
                "hanging": default_config.get("hanging"),
            }
        )

    if level_num in bullet_levels:
        level_config.update(bullet_levels[level_num])

    if "bullet_char" not in level_config:
        inherited_bullet = _find_inherited_bullet_char(
            level_num, bullet_levels, default_nested_config
        )
        if inherited_bullet:
            level_config["bullet_char"] = inherited_bullet
        elif default_nested_config and level_num in default_nested_config:
            default_bullet = default_nested_config[level_num].get("bullet_char")
            if default_bullet:
                level_config["bullet_char"] = default_bullet

    if default_indentation:
        if "left" not in level_config and "left" in default_indentation:
            base_left = default_indentation["left"]
            increment = default_indentation.get("increment")
            if increment is not None:
                level_config["left"] = base_left + (level_num * increment)
            else:
                level_config["left"] = base_left

        if "hanging" not in level_config and "hanging" in default_indentation:
            level_config["hanging"] = default_indentation["hanging"]

    return level_config


def _find_inherited_bullet_char(
    level_num: int,
    bullet_levels: dict[int, dict[str, str | int]],
    default_nested_config: dict[str, dict[str, str | int]] | None,
) -> str | None:
    """
    Find bullet character to inherit from parent levels.
    Looks for the nearest parent level that has an explicit bullet_char configuration.
    """
    for parent_level in range(level_num - 1, -1, -1):
        if parent_level in bullet_levels:
            parent_config = bullet_levels[parent_level]
            if "bullet_char" in parent_config:
                return parent_config["bullet_char"]
    if default_nested_config:
        for parent_level in range(level_num - 1, -1, -1):
            if parent_level in default_nested_config:
                parent_config = default_nested_config[parent_level]
                if "bullet_char" in parent_config:
                    return parent_config["bullet_char"]

    return None


def _get_level_number(level: Element, w_tags: dict[str, str]) -> int:
    """
    Extract the level number from a level element.
    """
    try:
        ilvl_attr = level.get(w_tags["ilvl"])
        if ilvl_attr is not None:
            return int(ilvl_attr)
    except (ValueError, TypeError):
        pass
    return 0


def analyze_list_structure(doc: Document, w_tags: dict[str, str]) -> dict:
    """
    Analyze the document's list structure to understand nesting patterns.
    Returns a dictionary with information about list levels and their usage.
    """
    list_paragraphs_info = find_all_list_paragraphs(doc, w_tags)

    analysis = {
        "total_list_items": len(list_paragraphs_info),
        "levels_used": set(),
        "level_distribution": {},
        "max_nesting_depth": 0,
        "list_groups": [],
    }

    current_group = []
    current_num_id = None

    for para_info in list_paragraphs_info:
        _, num_id, level = para_info

        analysis["levels_used"].add(level)
        analysis["level_distribution"][level] = (
            analysis["level_distribution"].get(level, 0) + 1
        )
        analysis["max_nesting_depth"] = max(analysis["max_nesting_depth"], level)

        if num_id != current_num_id or (
            current_group and level == 0 and current_group[-1][2] > 0
        ):
            if current_group:
                analysis["list_groups"].append(
                    {
                        "num_id": current_num_id,
                        "items": current_group,
                        "levels": [item[2] for item in current_group],
                    }
                )

            current_group = [para_info]
            current_num_id = num_id
        else:
            current_group.append(para_info)

    if current_group:
        analysis["list_groups"].append(
            {
                "num_id": current_num_id,
                "items": current_group,
                "levels": [item[2] for item in current_group],
            }
        )

    return analysis


def preserve_nested_structure(doc: Document, w_tags: dict[str, str]) -> bool:
    """
    Ensure that nested list structure is preserved during formatting.
    Returns True if structure is preserved, False if issues are detected.
    """
    analysis = analyze_list_structure(doc, w_tags)

    if analysis["max_nesting_depth"] > 0:
        for group in analysis["list_groups"]:
            levels = group["levels"]
            for i in range(1, len(levels)):
                if levels[i] > levels[i - 1] + 1:
                    print(
                        f"Warning: Detected irregular nesting jump from level {levels[i-1]} to {levels[i]}"
                    )
                    return False

    return True


def get_level_specific_config(
    level: int,
    nested_levels: dict[str, dict[str, str | int]],
    default_config: dict[int, dict[str, str | int]] | None,
) -> dict[str, str | int]:
    """
    Get configuration for a specific list level, falling back to defaults if needed.
    """
    level_config = nested_levels.get(str(level), {})
    if not level_config and default_config:
        level_config = default_config.get(level, {})

    return level_config


def validate_bullet_list_config(
    list_config: dict[str, str | dict[str, str | int]],
    bullet_character_options: dict[str, str],
) -> list[str]:
    """
    Validate bullet list level configuration and return any issues found.
    """
    issues = []
    bullet_levels = _extract_bullet_level_configs(list_config)

    for level_num, config in bullet_levels.items():
        if level_num < 0 or level_num > 8:
            issues.append(f"Level {level_num} is out of range (0-8)")
            continue

        bullet_char = config.get("bullet_char")
        if bullet_char and bullet_char not in bullet_character_options:
            issues.append(
                f"Unknown bullet character '{bullet_char}' for level {level_num}"
            )

        left = config.get("left")
        hanging = config.get("hanging")
        if left is not None and (not isinstance(left, int) or left < 0):
            issues.append(f"Invalid left indentation {left} for level {level_num}")
        if hanging is not None and (not isinstance(hanging, int) or hanging < 0):
            issues.append(
                f"Invalid hanging indentation {hanging} for level {level_num}"
            )

    return issues


def _remove_bullet_font_formatting(level: Element, w_tags: dict[str, str]) -> None:
    """
    Remove font formatting from bullet level to ensure consistent appearance.
    """
    rPr = level.find(w_tags["rPr"])
    if rPr is not None:
        rFonts = rPr.find(w_tags["rFonts"])
        if rFonts is not None:
            rPr.remove(rFonts)
