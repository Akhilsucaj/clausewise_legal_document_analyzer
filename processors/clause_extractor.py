import re

def extract_clauses(text):
    clauses = re.split(r"\n\d+\.\s|\n\s*\d+\)", text)
    clauses = [c.strip() for c in clauses if c.strip()]
    return clauses