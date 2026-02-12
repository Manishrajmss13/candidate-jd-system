from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List


class EmbeddingEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, 384))
        embs = self.model.encode(texts, convert_to_numpy=True)
        return np.array(embs)
