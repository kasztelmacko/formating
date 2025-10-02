import style_mapping_config as MAPING_CONF
from docx import Document

from document_formatter_config import DocumentFormatterConfig
from styling_utils.style_appliers import apply_docx_style_definitions
from styling_utils.paragraph_cleaning_utils import clean_paragraph, remove_empty_paragraph
from styling_utils.bullet_list_styling_util import update_bullet_characters, apply_list_termination_characters
from styling_utils.chapter_section_styles_utils import enforce_chapter_page_breaks, adjust_chapter_section_numbering_format, adjust_section_numbering_order
from styling_utils.header_footer_styling_util import apply_header_footer_to_all_sections

class DocumentFormattingAgent:
    def __init__(self, doc: Document, config: DocumentFormatterConfig):
        self.doc = doc
        self.config = config

    def apply_all_styles(self):
        self.clean_paragraphs()
        self.apply_paragraph_styles()
        self.apply_chapter_section_styles()
        self.apply_list_styles()
        self.apply_header_footer_styles()

    def apply_paragraph_styles(self):
        """Apply paragraph styles from the configuration."""
        apply_docx_style_definitions(
            doc=self.doc, 
            style_definitions=self.config.paragraph_styles, 
            style_attributes_names_mapping=MAPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
            font_mapping=MAPING_CONF.FONT_MAPPING,
            paragraph_format_mapping=MAPING_CONF.PARAGRAPH_FORMAT_MAPPING
        )

    def apply_chapter_section_styles(self):
        """Apply chapter and section styles from the configuration."""
        apply_docx_style_definitions(
            doc=self.doc, 
            style_definitions=self.config.chapter_and_section_rules, 
            style_attributes_names_mapping=MAPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
            font_mapping=MAPING_CONF.FONT_MAPPING,
            paragraph_format_mapping=MAPING_CONF.PARAGRAPH_FORMAT_MAPPING
        )
        
        refactor_section_numbering = self.config.document_setup.get("refactor_section_numbering", False)
        
        if refactor_section_numbering:
            adjust_section_numbering_order(
                doc=self.doc,
                style_definitions=self.config.chapter_and_section_rules,
                style_names_mapping=MAPING_CONF.STYLE_NAMES_MAPPING,
                style_attributes_names_mapping=MAPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
                chapter_section_numbering_regex=MAPING_CONF.CHAPTER_SECTION_NUMBERING_REGEX
            )
        else:
            adjust_chapter_section_numbering_format(
                doc=self.doc,
                style_definitions=self.config.chapter_and_section_rules,
                style_attributes_names_mapping=MAPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
                chapter_section_numbering_regex=MAPING_CONF.CHAPTER_SECTION_NUMBERING_REGEX
            )

    def apply_list_styles(self):
        """Apply bullet list rules from the configuration."""
        update_bullet_characters(
            doc=self.doc, 
            list_config=self.config.list_rules, 
            bullet_character_options=MAPING_CONF.BULLET_CHARACTER_OPTIONS,
            w_tags=MAPING_CONF.W_TAGS
        )
        enforce_chapter_page_breaks(
            doc=self.doc, 
            style_names_mapping=MAPING_CONF.STYLE_NAMES_MAPPING
        )
        apply_list_termination_characters(
            doc=self.doc, 
            list_config=self.config.list_rules,
            w_tags=MAPING_CONF.W_TAGS
        )

    def apply_header_footer_styles(self):
        """Apply header and footer styles from the configuration."""
        apply_header_footer_to_all_sections(
            doc=self.doc,
            header_footer_config=self.config.header_footer_rules,
            style_attributes_names_mapping=MAPING_CONF.STYLE_ATTRIBUTES_NAMES_MAPPING,
            field_mappings=MAPING_CONF.HEADER_FOOTER_FIELD_MAPPINGS,
            font_mapping=MAPING_CONF.FONT_MAPPING,
            layout_config=MAPING_CONF.HEADER_FOOTER_LAYOUT_CONFIG,
        )

    def clean_paragraphs(self):
        """
        Perform paragraph cleanup for all paragraphs in the document:
        trim spaces and remove empty paragraphs.
        """
        trim_spaces = self.config.document_setup.get("trim_spaces", True)
        for paragraph in self.doc.paragraphs[:]:
            clean_paragraph(
                paragraph=paragraph, 
                trim_spaces=trim_spaces
            )
            remove_empty_paragraph(
                paragraph=paragraph
            )

