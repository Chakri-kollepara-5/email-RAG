import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../../data")

def load_guidelines():
    with open(os.path.join(DATA_DIR, "company_guidelines.md"), "r", encoding="utf-8") as f:
        return f.read()

def load_examples():
    with open(os.path.join(DATA_DIR, "rewrite_examples.json"), "r", encoding="utf-8") as f:
        return json.load(f)
