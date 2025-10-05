from docx import Document

from styling_utils.core.style_appliers import apply_docx_style_definitions
from styling_utils.numbering.numbering_utils import apply_chapter_based_numbering


def apply_table_figure_styles(
    doc: Document,
    config,
    style_attributes_names_mapping,
    font_mapping,
    paragraph_format_mapping,
    style_names_mapping,
    chapter_section_numbering_regex,
    renumbering_regex,
):
    """Apply table and figure title styles from the configuration."""
    table_figure_styles = {}
    if "table_titles" in config.chapter_and_section_rules:
        table_figure_styles["table_titles"] = config.chapter_and_section_rules[
            "table_titles"
        ]
    if "figure_titles" in config.chapter_and_section_rules:
        table_figure_styles["figure_titles"] = config.chapter_and_section_rules[
            "figure_titles"
        ]

    if table_figure_styles:
        apply_docx_style_definitions(
            doc=doc,
            style_definitions=table_figure_styles,
            style_attributes_names_mapping=style_attributes_names_mapping,
            font_mapping=font_mapping,
            paragraph_format_mapping=paragraph_format_mapping,
        )

        apply_table_figure_numbering(
            doc,
            config,
            style_names_mapping,
            style_attributes_names_mapping,
            chapter_section_numbering_regex,
            renumbering_regex,
        )


def apply_source_styles(
    doc: Document,
    config,
    style_attributes_names_mapping,
    font_mapping,
    paragraph_format_mapping,
):
    """Apply source text styles from the configuration."""
    if hasattr(config, "source_rules") and config.source_rules:
        apply_docx_style_definitions(
            doc=doc,
            style_definitions=config.source_rules,
            style_attributes_names_mapping=style_attributes_names_mapping,
            font_mapping=font_mapping,
            paragraph_format_mapping=paragraph_format_mapping,
        )


def apply_table_figure_numbering(
    doc: Document,
    config,
    style_names_mapping,
    style_attributes_names_mapping,
    chapter_section_numbering_regex,
    renumbering_regex,
):
    """Apply chapter-based numbering for table and figure titles using reusable utilities."""
    target_styles = []
    if "table_titles" in config.chapter_and_section_rules:
        target_styles.append("table_titles")
    if "figure_titles" in config.chapter_and_section_rules:
        target_styles.append("figure_titles")

    if target_styles:
        filtered_style_definitions = {}
        for style in target_styles:
            if style in config.chapter_and_section_rules:
                filtered_style_definitions[style] = config.chapter_and_section_rules[
                    style
                ]

        apply_chapter_based_numbering(
            doc=doc,
            style_names_mapping=style_names_mapping,
            style_definitions=filtered_style_definitions,
            style_attributes_names_mapping=style_attributes_names_mapping,
            chapter_section_numbering_regex=chapter_section_numbering_regex,
            target_styles=target_styles,
            use_common_pattern=True,
            renumbering_regex=renumbering_regex,
        )
