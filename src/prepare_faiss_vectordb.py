import json
from typing import List
import torch
import argparse
from tqdm import tqdm
import logging
from sentence_transformers import SentenceTransformer

from extractor import extract_common_steps
from vectordb import FaissVectordb

class VectorDB:
    def __init__(self, args):
        self.device = args.device
        
        self.model = SentenceTransformer(args.model_name)
        self.index = FaissVectordb(feature_shape=args.feature_shape)
        # Reproducibility
        self.model.to(self.device)
        self.model.eval()

        self.json_object = dict()
        self.feature_shape = args.feature_shape
        self.batch_size = args.batch_size

    @torch.no_grad()
    def create_embedding(self, text : str):
        return self.model.encode(text, normalize_embeddings=True).reshape((1, self.feature_shape))
    
    def create_mapping(self, id : int ,step : str):
        self.json_object[id] = step

    def create_vectordb(self, steps : List[str]):
        logging.info('Start to create the Database')
        count = 0
        
        # Create Embedding
        embedding_vectors = []
        for idx in tqdm(range(0, len(steps)), position = 0, leave = True):
            embedding = self.create_embedding(steps[idx])
            embedding_vectors.append(embedding)
        
        # Build Faiss VectorDatabase
        for vector, step in tqdm(zip(embedding_vectors, steps), position = 0, leave=True):
            self.index.add(vector)
            self.create_mapping(count, step)
            count += 1

        logging.info("Total steps: {} steps.".format(count))

        self.index.write_index(output_dir = f"./dataset/bge-small-en-v1.5.bin")

        with open(f"./dataset/mapping.json", "w") as f:
            json.dump(self.json_object, f)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type = str, default = "cpu")
    parser.add_argument("--run-name", type = str, default = "clip_database")
    parser.add_argument("--batch-size", type = int, default = 1)
    parser.add_argument("--feature-shape", type = int, default = 384)
    parser.add_argument("--model-name", type=str, default="BAAI/bge-small-en-v1.5")
    args = parser.parse_args()

    database = VectorDB(args = args)

    with open("./dataset/sample/common.step.ts", "r") as INFILE:
        common_steps = INFILE.read()
    
    common_steps = extract_common_steps(common_steps)
    common_steps = [list(common_step)[1] for common_step in common_steps]
    print(common_steps)
    database.create_vectordb(common_steps)
