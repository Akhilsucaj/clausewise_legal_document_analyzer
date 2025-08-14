import docx
import fitz  # PyMuPDF

def read_file(uploaded_file):
    ext = uploaded_file.name.lower().split(".")[-1]
    
    if ext == "txt":
        return uploaded_file.read().decode("utf-8")
    
    elif ext == "docx":
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    
    elif ext == "pdf":
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in pdf])
    
    else:
        raise ValueError(f"Unsupported file type: {ext}")