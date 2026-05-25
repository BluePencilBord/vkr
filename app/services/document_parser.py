import fitz
import docx
import io


class UnsupportedDocumentFormat(Exception):
    pass


async def extract_text_from_document(file_bytes: bytes, file_name: str) -> str:
    extension = file_name.split(".")[-1].lower() if "." in file_name else ""

    if extension == "pdf":
        return await extract_text_from_pdf(file_bytes)
    elif extension == "docx":
        return await extract_text_from_docx(file_bytes)
    else:
        raise UnsupportedDocumentFormat(f"Формат файла '.{extension}' пока не поддерживается.")


async def extract_text_from_pdf(file_bytes: bytes) -> str:
    pages_of_text = []
    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")

    for page_num in range(len(pdf_doc)):
        pages_of_text.append(pdf_doc.load_page(page_num).get_text())

    return "".join(pages_of_text)


async def extract_text_from_docx(file_bytes: bytes) -> str:
    file_stream = io.BytesIO(file_bytes)
    doc = docx.Document(file_stream)
    full_text = []

    for par in doc.paragraphs:
        if par.text.strip():
            full_text.append(par.text)
    
    return "\n".join(full_text)
