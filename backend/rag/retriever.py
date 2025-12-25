import numpy as np
import faiss

from .embedder import get_embedding
from .loader import load_guidelines, load_examples

guidelines_text = load_guidelines()
examples = load_examples()   # list of {original, rewritten}

docs = [guidelines_text] + [
    f"Original: {ex['original']}\nRewrite: {ex['rewritten']}"
    for ex in examples
]

embeddings = np.array([get_embedding(d) for d in docs])

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)


def retrieve_similar(query: str, k: int = 3):
    query_emb = np.array([get_embedding(query)])
    distances, indices = index.search(query_emb, k)

    return [docs[i] for i in indices[0]]