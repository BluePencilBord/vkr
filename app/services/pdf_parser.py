import fitz
import io


async def extract_text_from_pdf(file_bytes: bytes) -> str:
    pages_of_text = []
    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")

    for page_num in range(len(pdf_doc)):
        pages_of_text.append(pdf_doc.load_page(page_num).get_text())

    return "".join(pages_of_text)
