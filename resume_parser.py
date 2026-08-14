"""
resume_parser.py
Extracts raw text from an uploaded resume file (PDF, DOCX, or TXT).
The extracted text is later sent to Gemini so it can infer skills itself —
we don't try to regex-match skills here, the LLM does that reasoning.
"""
 
import io
import PyPDF2
import docx
 
 
def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file's raw bytes."""
    text_chunks = []
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_chunks.append(page_text)
    return "\n".join(text_chunks)
 
 
def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a .docx file's raw bytes."""
    document = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in document.paragraphs if p.text.strip())
 
 
def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode a plain text file's raw bytes."""
    return file_bytes.decode("utf-8", errors="ignore")
 
 
def extract_resume_text(uploaded_file) -> str:
    """
    Main entry point. Takes a Streamlit UploadedFile object and routes it
    to the correct extractor based on file extension.
    """
    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()
 
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif filename.endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    else:
        raise ValueError(
            f"Unsupported file type: {filename}. Please upload a PDF, DOCX, or TXT file."
        )
 