from document_formatter_config import DocumentFormatterConfig
from styling_utils import apply_style_group
from paragraph_cleaning_utils import clean_paragraph, remove_empty_paragraph
from bullet_list_styling_util import update_bullet_characters

class DocumentFormattingAgent:
    def __init__(self, doc, config: DocumentFormatterConfig):
        self.doc = doc
        self.config = config

    def apply_all_styles(self):
        self.apply_paragraph_styles()
        self.apply_chapter_section_styles()
        self.apply_list_styles()
        self.clean_paragraphs()

    def apply_paragraph_styles(self):
        apply_style_group(self.doc, self.config.paragraph_styles)

    def apply_chapter_section_styles(self):
        apply_style_group(self.doc, self.config.chapter_and_section_rules)

    def apply_list_styles(self):
        update_bullet_characters(self.doc, self.config.list_rules)

    def clean_paragraphs(self, trim_spaces=True):
        for paragraph in self.doc.paragraphs[:]:
            clean_paragraph(paragraph, trim_spaces=trim_spaces)
            remove_empty_paragraph(paragraph)

