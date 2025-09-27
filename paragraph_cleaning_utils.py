def clean_paragraph(paragraph, trim_spaces=True):
    """Remove unnecessary blank lines/spaces from a paragraph."""
    if trim_spaces:
        paragraph.text = paragraph.text.lstrip("\n\r ").rstrip("\n\r ")

def remove_empty_paragraph(paragraph):
    """Remove empty paragraph from the document."""
    if not paragraph.text.strip():
        p_element = paragraph._element
        p_element.getparent().remove(p_element)