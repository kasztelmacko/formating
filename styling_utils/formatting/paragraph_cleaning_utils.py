from config import OPENXML_FORMATS

def apply_paragraph_cleaning(paragraph, trim_spaces=True):
    """
    Trim leading/trailing whitespace/newlines from paragraph text,
    without touching inline objects like images or equations.
    """
    if trim_spaces and paragraph.text:
        paragraph.text = paragraph.text.lstrip("\n\r ").rstrip("\n\r ")

def apply_empty_paragraph_removal(paragraph):
    """
    Remove a paragraph only if it is truly empty (no text, no runs, no images/equations).
    """
    if is_paragraph_empty(paragraph):
        p_element = paragraph._element
        p_element.getparent().remove(p_element)

def is_paragraph_empty(paragraph) -> bool:
    """
    Determine if a paragraph is truly empty (no text, no runs, no inline shapes, pictures, or math).
    """
    if paragraph.text.strip():
        return False

    p_elem = paragraph._element
    if (
        p_elem.findall(f".//{{{OPENXML_FORMATS['M']}}}oMath") or
        p_elem.findall(f".//{{{OPENXML_FORMATS['W']}}}drawing") or
        p_elem.findall(f".//{{{OPENXML_FORMATS['PIC']}}}pic") or
        p_elem.findall(f".//{{{OPENXML_FORMATS['V']}}}shape")
    ):
        return False

    for run in paragraph.runs:
        if run.text.strip():
            return False

    return True