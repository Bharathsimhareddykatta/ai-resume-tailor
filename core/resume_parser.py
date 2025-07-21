import fitz  
import docx
import os
import tempfile

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def parse_resume(resume_file):
    file_extension = resume_file.name.split(".")[-1].lower()

    if file_extension == "pdf":
        return extract_text_from_pdf(resume_file)
    elif file_extension == "docx":
        return extract_text_from_docx(resume_file)
    else:
        return "Unsupported file format."
