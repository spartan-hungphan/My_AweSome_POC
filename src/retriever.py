import json
from sentence_transformers import SentenceTransformer
from typing import List
from rapidfuzz import fuzz

from .vectordb import FaissVectordb


class Retriever:
    def __init__(self, 
                 model_name = "BAAI/bge-small-en-v1.5", 
                 faiss_dir = "dataset/bge-small-en-v1.5.bin",
                 mapping_dir = "./dataset/mapping.json", 
                 feature_dim = 384,
                 top_k : int = 3, 
                 threshold : int = 0.7):
        # VectorDB
        self.feature_dim = feature_dim
        self.index = FaissVectordb(feature_shape= feature_dim)
        self.index.read_index(input_dir = faiss_dir)
        # Model
        self.model = SentenceTransformer(model_name)

        with open(mapping_dir, "r") as INFILE:
            self.mapping = json.load(INFILE)

        self.top_k = top_k
        self.threshold = threshold

    def fuzzy_search(self, input_text : str, common_steps : List[str]) -> List:
        def fuzzy_compute(text : str, common_step : str) -> List: 
            score = fuzz.partial_ratio(text, common_step) / 100
            return [common_step, score]

        result = [fuzzy_compute(input_text, list(common_step)[1]) for common_step in common_steps]
        result = sorted(result, key = lambda x: x[1], reverse = True)[:self.top_k]
        return [res[0] for res in result if res[1] > self.threshold]

    def faiss_retrieve(self, input_text : str) -> List:
        text_features = self.model.encode(input_text, normalize_embeddings=True).reshape((1,self.feature_dim))
        scores, indexes = self.index.search(query_vecs = text_features, top_k = self.top_k)
        print(scores)
        return [self.mapping[str(index)] for i, index in enumerate(indexes[0]) if scores[0][i] >= self.threshold]