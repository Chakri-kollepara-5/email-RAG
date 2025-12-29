from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

print("\nLoading model...")

model_name = "google/flan-t5-large"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

prompt = """
Paraphrase the text to be polite and grammatically correct.
Only return the rewritten text.

Text: hello iam chakri who are you
Polite version:
"""

inputs = tokenizer(prompt, return_tensors="pt").to(device)

outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    num_beams=4,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    no_repeat_ngram_size=3,
    early_stopping=True
)

text = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("\nOUTPUT:\n")
print(text.strip())