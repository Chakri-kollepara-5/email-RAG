from transformers import pipeline

pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-large"
)

def rewrite_with_local_model(prompt: str) -> str:
    out = pipe(
        prompt,
        max_new_tokens=120,
        num_beams=5,
        do_sample=False,
        temperature=0.0
    )[0]["generated_text"]

    return out.strip()