import os

MAIN_DIR = os.getcwd()
INPUT_DIR = os.path.join(MAIN_DIR, "data/input/")
OUTPUT_DIR = os.path.join(MAIN_DIR, "data/output/")
INPUT_DOCX = os.path.join(INPUT_DIR, "test_yaml.docx")
OUTPUT_DOCX = os.path.join(OUTPUT_DIR, "test_modified.docx")

STYLE_CONFIG_FILENAME = "style_config.yaml"
STYLE_SCHEMA_FILENAME = "style_config_schema.yaml"
