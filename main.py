import docx
from document_formatter_config import DocumentFormatterConfig
from document_formatting_agent import DocumentFormattingAgent
from paths import INPUT_DOCX, INPUT_DIR, STYLE_CONFIG_FILENAME, STYLE_SCHEMA_FILENAME, OUTPUT_DOCX

doc = docx.Document(INPUT_DOCX)
formatter_config = DocumentFormatterConfig.load_and_validate_yaml(
    input_dir=INPUT_DIR,
    style_filename=STYLE_CONFIG_FILENAME,
    schema_filename=STYLE_SCHEMA_FILENAME
)
agent = DocumentFormattingAgent(doc, formatter_config)
agent.apply_all_styles()
doc.save(OUTPUT_DOCX)