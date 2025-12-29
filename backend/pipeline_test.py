from transformers import pipeline

print("\nLoading model...\n")

pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-large"
)

prompt = """
Rewrite the following text in polite, grammatically correct English.

Text:
hello iam chakri who are you

Answer:
"""

out = pipe(
    prompt.strip(),
    max_new_tokens=60,
    do_sample=False
)

print("\nOUTPUT:\n")
print(out[0]["generated_text"])
