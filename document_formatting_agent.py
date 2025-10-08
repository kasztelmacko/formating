from docx import Document

import config as MAPPING_CONF
from document_formatter_config import DocumentFormatterConfig
from styling_utils import (
    apply_bullet_character_updates,
    apply_chapter_page_breaks,
    apply_chapter_section_numbering_format,
    apply_docx_style_definitions,
    apply_empty_paragraph_removal,
    apply_header_footer_to_all_sections,
    apply_list_termination_characters,
    apply_nested_styling_to_paragraphs,
    apply_paragraph_cleaning,
    apply_section_numbering_order,
    apply_source_styles,
    apply_table_figure_styles,
)


class DocumentFormattingAgent:
    def __init__(self, doc: Document, config: DocumentFormatterConfig):
        self.doc = doc
        self.config = config

    def apply_all_styles(self):
        self.clean_paragraphs()
        self.apply_paragraph_styles()
        self.apply_chapter_section_styles()
        self.apply_table_figure_styles()
        self.apply_source_styles()
        self.apply_list_styles()
        self.apply_header_footer_styles()
        self.apply_nested_styling()

    def apply_paragraph_styles(self):
        """Apply paragraph styles from the configuration."""
        apply_docx_style_definitions(
            doc=self.doc,
            style_definitions=self.config.paragraph_styles,
            style_attributes_names_mapping=MAPPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
            font_mapping=MAPPING_CONF.FONT_MAPPING,
            paragraph_format_mapping=MAPPING_CONF.PARAGRAPH_FORMAT_MAPPING,
        )

    def apply_chapter_section_styles(self):
        """Apply chapter and section styles from the configuration."""
        apply_docx_style_definitions(
            doc=self.doc,
            style_definitions=self.config.chapter_and_section_rules,
            style_attributes_names_mapping=MAPPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
            font_mapping=MAPPING_CONF.FONT_MAPPING,
            paragraph_format_mapping=MAPPING_CONF.PARAGRAPH_FORMAT_MAPPING,
        )

        refactor_section_numbering = self.config.document_setup.get(
            "refactor_section_numbering", False
        )

        if refactor_section_numbering:
            apply_section_numbering_order(
                doc=self.doc,
                style_definitions=self.config.chapter_and_section_rules,
                style_names_mapping=MAPPING_CONF.STYLE_NAMES_MAPPING,
                style_attributes_names_mapping=MAPPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
                chapter_section_numbering_regex=MAPPING_CONF.CHAPTER_SECTION_NUMBERING_REGEX,
                renumbering_regex=MAPPING_CONF.RENUMBERING_REGEX,
            )
        else:
            apply_chapter_section_numbering_format(
                doc=self.doc,
                style_definitions=self.config.chapter_and_section_rules,
                style_attributes_names_mapping=MAPPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
                chapter_section_numbering_regex=MAPPING_CONF.CHAPTER_SECTION_NUMBERING_REGEX,
                renumbering_regex=MAPPING_CONF.RENUMBERING_REGEX,
            )

    def apply_table_figure_styles(self):
        """Apply table and figure title styles from the configuration."""
        apply_table_figure_styles(
            doc=self.doc,
            config=self.config,
            style_attributes_names_mapping=MAPPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
            font_mapping=MAPPING_CONF.FONT_MAPPING,
            paragraph_format_mapping=MAPPING_CONF.PARAGRAPH_FORMAT_MAPPING,
            style_names_mapping=MAPPING_CONF.STYLE_NAMES_MAPPING,
            chapter_section_numbering_regex=MAPPING_CONF.CHAPTER_SECTION_NUMBERING_REGEX,
            renumbering_regex=MAPPING_CONF.RENUMBERING_REGEX,
        )

    def apply_source_styles(self):
        """Apply source text styles from the configuration."""
        apply_source_styles(
            doc=self.doc,
            config=self.config,
            style_attributes_names_mapping=MAPPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
            font_mapping=MAPPING_CONF.FONT_MAPPING,
            paragraph_format_mapping=MAPPING_CONF.PARAGRAPH_FORMAT_MAPPING,
        )

    def apply_list_styles(self):
        """Apply bullet list rules from the configuration."""
        apply_bullet_character_updates(
            doc=self.doc,
            list_config=self.config.list_rules,
            bullet_character_options=MAPPING_CONF.BULLET_CHARACTER_OPTIONS,
            w_tags=MAPPING_CONF.W_TAGS,
            default_nested_config=MAPPING_CONF.DEFAULT_NESTED_LEVEL_CONFIG,
            default_indentation=MAPPING_CONF.DEFAULT_BULLET_LIST_INDENTATION,
        )
        apply_chapter_page_breaks(
            doc=self.doc, style_names_mapping=MAPPING_CONF.STYLE_NAMES_MAPPING
        )
        apply_list_termination_characters(
            doc=self.doc, list_config=self.config.list_rules, w_tags=MAPPING_CONF.W_TAGS
        )

    def apply_header_footer_styles(self):
        """Apply header and footer styles from the configuration."""
        apply_header_footer_to_all_sections(
            doc=self.doc,
            header_footer_config=self.config.header_footer_rules,
            style_attributes_names_mapping=MAPPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
            field_mappings=MAPPING_CONF.HEADER_FOOTER_FIELD_MAPPINGS,
            font_mapping=MAPPING_CONF.FONT_MAPPING,
            layout_config=MAPPING_CONF.HEADER_FOOTER_LAYOUT_CONFIG,
        )

    def apply_nested_styling(self):
        """Apply nested styling to paragraphs with common_pattern_format font formatting."""
        all_style_definitions = {}
        all_style_definitions.update(self.config.chapter_and_section_rules)
        all_style_definitions.update(self.config.source_rules)

        if hasattr(self.config, 'table_rules') and self.config.table_rules:
            all_style_definitions.update(self.config.table_rules)

        if hasattr(self.config, 'figure_rules') and self.config.figure_rules:
            all_style_definitions.update(self.config.figure_rules)

        apply_nested_styling_to_paragraphs(
            doc=self.doc,
            style_names_mapping=MAPPING_CONF.STYLE_NAMES_MAPPING,
            font_mapping=MAPPING_CONF.FONT_MAPPING,
            style_definitions=all_style_definitions,
            style_attributes_names_mapping=MAPPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
        )

    def clean_paragraphs(self):
        """
        Perform paragraph cleanup for all paragraphs in the document:
        trim spaces and remove empty paragraphs.
        """
        trim_spaces = self.config.document_setup.get("trim_spaces", True)
        for paragraph in self.doc.paragraphs[:]:
            apply_paragraph_cleaning(paragraph=paragraph, trim_spaces=trim_spaces)
            apply_empty_paragraph_removal(
                paragraph=paragraph, openxml_formats=MAPPING_CONF.OPENXML_FORMATS
            )
