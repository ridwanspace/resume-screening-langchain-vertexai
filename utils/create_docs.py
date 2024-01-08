
from langchain.schema import Document
from utils.create_pdf_text import get_pdf_text


def get_docs(user_pdf_list, unique_id):
    """
    Create a list of Document objects from a list of user PDF files.

    Args:
        user_pdf_list (List[Path]): A list of Path objects representing the user PDF files.
        unique_id (str): A unique identifier for the documents.

    Returns:
        List[Document]: A list of Document objects.

    """
    docs = []

    for filename in user_pdf_list:
        chunks, page_numbers = get_pdf_text(filename)

        # Adding items to our list - Adding data & its metadata
        docs.append(Document(
            page_content=chunks,
            metadata={
                "name": filename.name,
                "id": filename.id,
                "type": filename.type,
                "size": filename.size,
                "page_numbers": page_numbers,  # Adding page numbers to metadata
                "unique_id": unique_id
            },
        ))

    return docs

