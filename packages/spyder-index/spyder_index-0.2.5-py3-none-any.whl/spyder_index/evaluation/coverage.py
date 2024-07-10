import numpy as np
from typing import Optional, Literal, List

from spyder_index.embeddings import HuggingFaceEmbeddings
from spyder_index.core.embeddings import embedding_similarity

class KnowledgeBaseCoverage():

    def __init__(self,
                 embed_model_name: Optional[str] = "sentence-transformers/all-MiniLM-L6-v2",
                 similarity_mode: Literal["cosine", "dot_product", "euclidean"] = "cosine",
                 similarity_threshold: float = 0.8,) -> None:
        
        self._embed = HuggingFaceEmbeddings(model_name=embed_model_name)
        self._similarity_threshold = similarity_threshold
        self._similarity_mode = similarity_mode

    def evaluate(self, contexts: List[str], response: str):
                            
        if not contexts or not response:
            raise ValueError("Must provide these parameters [`contexts`, `response`]")
            
        coverage = { "contexts_score": [], "score": 0 }
        output_embedding = self._embed.get_query_embedding(response)
            
        for context in contexts:
            context_embedding = self._embed.get_query_embedding(context)
            coverage["contexts_score"].append(embedding_similarity(output_embedding, context_embedding, mode=self._similarity_mode))

        coverage["score"] = np.mean(coverage["contexts_score"])
        coverage["passing"] = coverage["score"] >= self._similarity_threshold

        return coverage
            

