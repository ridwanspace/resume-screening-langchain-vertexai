from PyPDF2 import PdfReader


def get_pdf_text(pdf_doc):
    """
    Extracts the text from a PDF document and returns it along with the page numbers.

    Args:
        pdf_doc: The path to the PDF document.

    Returns:
        A tuple containing the extracted text and a list of page numbers.
    """
    text = ""
    page_numbers = []
    pdf_reader = PdfReader(pdf_doc)
    for i, page in enumerate(pdf_reader.pages):
        text += page.extract_text()
        page_numbers.append(i + 1)  # Page numbers start from 1
    return text, page_numbers


