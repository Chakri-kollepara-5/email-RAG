from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/")
def health():
    return {"status": "ok"}


def analyze_text(text: str):
    tox_scores = toxicity_pipe(text)[0]

    toxic_labels = [
        "toxic", "insult", "threat",
        "obscene", "identity_hate", "severe_toxic"
    ]

    rude = max(
        [t["score"] for t in tox_scores if t["label"] in toxic_labels] or [0]
    )

    sentimental = sentiment_pipe(text)[0]

    return {
        "rude_percent": round(rude * 100, 2),
        "sentiment": sentimental["label"],
        "sentiment_confidence": round(sentimental["score"] * 100, 2)
    }


def rewrite_text(email: str):
    prompt = f"""
Rewrite the email to make it polite, calm and professional.

RULES:
• Keep the meaning the same
• DO NOT reuse the same wording
• Remove rude or harsh tone
• Fix grammar
• Output ONLY the rewritten email

Examples:
Harsh: "Fix this issue now"
Polite: "Could you please help me resolve this issue?"

Harsh: "This delay is unacceptable. Do your job properly."
Polite: "I’m concerned about the delay. Could you please look into this when you have a moment?"

Rewrite this email:
"{email}"
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        num_beams=4,
        do_sample=False,
        no_repeat_ngram_size=3,
        repetition_penalty=2.8,
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


@app.post("/rewrite")
def rewrite(req: EmailRequest):
    analysis = analyze_text(req.email)
    rewritten = rewrite_text(req.email)

    return {
        "rewritten_email": rewritten,
        "analysis": analysis
    }