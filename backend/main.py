from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
import sys

app = FastAPI()

REWRITE_MODEL = "google/flan-t5-large"

tokenizer = AutoTokenizer.from_pretrained(REWRITE_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(REWRITE_MODEL)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

toxicity_pipe = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    return_all_scores=True
)

sentiment_pipe = pipeline("sentiment-analysis")


class EmailRequest(BaseModel):
    email: str


def analyze_text(text: str):
    tox = toxicity_pipe(text)[0]
    sentimental = sentiment_pipe(text)[0]

    rude_score = sum([t["score"] for t in tox if t["label"] != "neutral"])
    rude_score = min(round(rude_score * 100, 2), 100)

    return {
        "rude_percent": rude_score,
        "sentiment": sentimental["label"],
        "sentiment_confidence": round(sentimental["score"] * 100, 2)
    }


def rewrite_text(email: str):

    prompt = f"""
Paraphrase the email below so it becomes polite, calm, professional and respectful.

Rules:
- Keep the meaning the same
- Fix grammar
- Remove rude / aggressive tone
- Do NOT repeat the original words
- Do NOT add extra information
- Output ONLY the rewritten email

Email:
{email}

Polite version:
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        num_beams=8,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        no_repeat_ngram_size=3,
        repetition_penalty=2.5,
        early_stopping=True
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "Polite version:" in text:
        text = text.split("Polite version:")[-1]

    return text.strip()



@app.post("/rewrite")
def rewrite(req: EmailRequest):

    analysis = analyze_text(req.email)
    rewritten = rewrite_text(req.email)

    return {
        "rewritten_email": rewritten,
        "analysis": analysis
    }
