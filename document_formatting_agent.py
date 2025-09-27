from style_mapping import STYLE_ATTRIBUTES_NAMES_MAPPING, STYLE_NAMES_MAPPING

from document_formatter_config import DocumentFormatterConfig
from styling_utils import apply_docx_style_definitions
from paragraph_cleaning_utils import clean_paragraph, remove_empty_paragraph
from bullet_list_styling_util import update_bullet_characters
from chapter_section_styles_utils import enforce_chapter_page_breaks

class DocumentFormattingAgent:
    def __init__(self, doc, config: DocumentFormatterConfig):
        self.doc = doc
        self.config = config

    def apply_all_styles(self):
        self.clean_paragraphs()
        self.apply_paragraph_styles()
        self.apply_chapter_section_styles()
        self.apply_list_styles()

    def apply_paragraph_styles(self):
        """Apply paragraph styles from the configuration."""
        apply_docx_style_definitions(
            doc=self.doc, 
            style_definitions=self.config.paragraph_styles, 
            style_attributes_names_mapping=STYLE_ATTRIBUTES_NAMES_MAPPING
        )

    def apply_chapter_section_styles(self):
        """Apply chapter and section styles from the configuration."""
        apply_docx_style_definitions(
            doc=self.doc, 
            style_definitions=self.config.chapter_and_section_rules, 
            style_attributes_names_mapping=STYLE_ATTRIBUTES_NAMES_MAPPING
        )

    def apply_list_styles(self):
        """Apply bullet list rules from the configuration."""
        update_bullet_characters(doc=self.doc, list_config=self.config.list_rules)
        enforce_chapter_page_breaks(doc=self.doc, style_names_mapping=STYLE_NAMES_MAPPING)

    def clean_paragraphs(self, trim_spaces: bool = True):
        """
        Perform paragraph cleanup for all paragraphs in the document:
        trim spaces and remove empty paragraphs.
        """
        for paragraph in self.doc.paragraphs[:]:
            clean_paragraph(paragraph=paragraph, trim_spaces=trim_spaces)
            remove_empty_paragraph(paragraph=paragraph)

