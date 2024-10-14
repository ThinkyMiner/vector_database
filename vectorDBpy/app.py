import json
from typing import List, Tuple, Dict
import numpy as np
import google.generativeai as gemini

gemini.configure(api_key="AIzaSyC1xOKaJPP0p5Y493lIQ5HnKgfx93Y6bj0")

class Embedding:
    def __init__(self, sentence: str, embedding: List[float]):
        self.sentence = sentence
        self.embedding = embedding

    @staticmethod
    def read_json(file_path: str) -> List[Tuple[str, List[float]]]:
        with open(file_path, 'r') as file:
            entries = json.load(file)
        return [(entry['sentence'], entry['embedding']) for entry in entries]

class VectorStore:
    def __init__(self):
        self.vector_data: Dict[str, np.ndarray] = {}
        self.sentences: Dict[str, str] = {}

    def add_vector(self, data: List[float], sentence: str):
        vector_id = str(len(self.vector_data))
        self.vector_data[vector_id] = np.array(data)
        self.sentences[vector_id] = sentence

    def find_similar_vectors(self, query_vector: np.ndarray, num_results: int) -> List[Tuple[str, float, str]]:
        results = []
        for vector_id, vector in self.vector_data.items():
            if isinstance(vector, np.ndarray):
                # Ensure both vectors are 1D and have the same shape
                if vector.ndim > 1:
                    vector = vector.flatten()
                if query_vector.ndim > 1:
                    query_vector = query_vector.flatten()
                
                if vector.shape == query_vector.shape:
                    similarity = self.cosine_similarity(query_vector, vector)
                    sentence = self.sentences[vector_id]
                    results.append((vector_id, similarity, sentence))
                else:
                    print(f"Shape mismatch: query_vector {query_vector.shape}, stored vector {vector.shape}")
            else:
                print(f"Invalid vector type for id {vector_id}: {type(vector)}")
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:num_results]

    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)

def main():
    store = VectorStore()
    path_to_embedding_file = "/Users/kartik/Desktop/vector_database/vectorDBpy/embeddings.json"
    res = Embedding.read_json(path_to_embedding_file)

    for sentence, embedding in res:
        store.add_vector(embedding, sentence)

    print(f"Number of vectors added: {len(store.vector_data)}")

    prompt = input("What do you want to know? ")

    embedding_response = gemini.embed_content(
        model="models/text-embedding-004",
        content=prompt.strip(),
        task_type="retrieval_document",
        title="Embedding of single string"
    )

    # Extract the actual embedding from the response
    query_vector = np.array(embedding_response['embedding'])
    print(f"Query vector shape: {query_vector.shape}")

    similar_vectors = store.find_similar_vectors(query_vector, 5)

    if not similar_vectors:
        print("No similar vectors found. This could be due to shape mismatch or empty results.")
    else:
        print("Most similar vectors:")
        for vector_id, similarity, sentence in similar_vectors:
            print(f"Sentence: {sentence}")
            print(f"Similarity: {similarity}")
            print("---")

if __name__ == "__main__":
    main()