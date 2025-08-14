from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

def classify_document(text):
    labels = ["NDA", "Lease", "Employment Contract", "Service Agreement", "Other"]

    # Check for empty or None text
    if text is None:
        raise ValueError("❌ The document could not be read. Please upload a valid and readable file.")
    if not isinstance(text, str):
        raise TypeError("❌ The document content is not valid text. Please upload a supported file format.")
    if not text.strip():
        raise ValueError("❌ The document appears to be empty. Please upload a file with readable content.")

    # Check for empty labels list
    if not labels:
        raise ValueError("❌ No candidate labels provided for classification.")

    try:
        result = classifier(text, candidate_labels=labels)
        return result
    except Exception as e:
        raise RuntimeError(f"❌ An error occurred during classification: {str(e)}")
