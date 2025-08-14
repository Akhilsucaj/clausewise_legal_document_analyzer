from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# ✅ Smaller & faster Granite model for testing
model_id = "ibm-granite/granite-3.3-2b-instruct"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map=None)  # Force CPU

# Create text-generation pipeline
simplifier_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1  # Force CPU
)

def simplify_clause(clause):
    """
    Simplifies a legal clause into plain English using Granite model.
    """
    prompt = f"Simplify this legal clause into plain English:\n\n{clause}"
    result = simplifier_pipeline(prompt, max_new_tokens=80, do_sample=True)
    return result[0]["generated_text"]