import pdfplumber
import docx

def load_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise ValueError(f"Unable to read PDF file: {str(e)}")
        if not text.strip():
            raise ValueError("The PDF file appears to be empty or unreadable.")
        return text

    elif file.name.endswith(".docx"):
        try:
            doc = docx.Document(file)
            text = "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Unable to read DOCX file: {str(e)}")
        if not text.strip():
            raise ValueError("The DOCX file appears to be empty or unreadable.")
        return text

    elif file.name.endswith(".txt"):
        try:
            text = file.read().decode("utf-8")
        except Exception as e:
            raise ValueError(f"Unable to read TXT file: {str(e)}")
        if not text.strip():
            raise ValueError("The TXT file appears to be empty or unreadable.")
        return text

    else:
        raise ValueError("Unsupported file format")
