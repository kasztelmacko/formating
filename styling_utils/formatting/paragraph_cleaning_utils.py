from docx.text.paragraph import Paragraph


def apply_paragraph_cleaning(paragraph: Paragraph, trim_spaces: bool = True) -> None:
    """
    Trim leading/trailing whitespace/newlines from paragraph text,
    without touching inline objects like images or equations.
    """
    if trim_spaces and paragraph.text:
        paragraph.text = paragraph.text.lstrip("\n\r ").rstrip("\n\r ")


def apply_empty_paragraph_removal(
    paragraph: Paragraph, openxml_formats: dict[str, str]
) -> None:
    """
    Remove a paragraph only if it is truly empty (no text, no runs, no images/equations).
    """
    if is_paragraph_empty(paragraph, openxml_formats):
        p_element = paragraph._element
        p_element.getparent().remove(p_element)


def is_paragraph_empty(paragraph: Paragraph, openxml_formats: dict[str, str]) -> bool:
    """
    Determine if a paragraph is truly empty (no text, no runs, no inline shapes, pictures, or math).
    """
    if paragraph.text.strip():
        return False

    p_elem = paragraph._element
    if (
        p_elem.findall(f".//{{{openxml_formats['M']}}}oMath")
        or p_elem.findall(f".//{{{openxml_formats['W']}}}drawing")
        or p_elem.findall(f".//{{{openxml_formats['PIC']}}}pic")
        or p_elem.findall(f".//{{{openxml_formats['V']}}}shape")
    ):
        return False

    return all(not run.text.strip() for run in paragraph.runs)
