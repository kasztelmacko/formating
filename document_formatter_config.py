import os
import yaml
from typing import Any, Dict
from jsonschema import validate, ValidationError

class DocumentFormatterConfig:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the configuration object with a validated config dictionary.
        """
        doc_config = config.get("document_formatter_config", {})

        self.document_setup = doc_config.get("document_setup", {})
        self.paragraph_styles = doc_config.get("paragraph_styles", {})
        self.chapter_and_section_rules = doc_config.get("chapter_and_section_rules", {})
        self.table_rules = doc_config.get("table_rules", {})
        self.figure_rules = doc_config.get("figure_rules", {})
        self.formula_rules = doc_config.get("formula_rules", {})
        self.list_rules = doc_config.get("list_rules", {})

    @staticmethod
    def load_yaml_file(input_dir: str, filename: str) -> dict:
        """
        Load a YAML file and return its content as a dictionary.
        """
        path = os.path.join(input_dir,filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @classmethod
    def load_and_validate_yaml(
        cls, input_dir: str, style_filename: str, schema_filename: str
    ) -> "DocumentFormatterConfig":
        """
        Load a styles YAML file and validate it against a JSON schema.

        Returns an instance of DocumentFormatterConfig if valid.
        """
        style_config = cls.load_yaml_file(input_dir=input_dir, filename=style_filename)
        style_schema = cls.load_yaml_file(input_dir=input_dir, filename=schema_filename)

        try:
            validate(instance=style_config, schema=style_schema)
        except ValidationError as e:
            raise ValueError(f"❌ YAML validation error: {e.message}") from e

        return cls(style_config)
