"""Embedding service using Sentence-Transformers."""

from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

import sys
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
from config import settings


class EmbeddingService:
    """Service for generating text embeddings using Sentence-Transformers."""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        """Singleton pattern to reuse model instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the embedding model."""
        if self._model is None:
            print(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            print(f"Model loaded. Embedding dimension: {self._model.get_sentence_embedding_dimension()}")
    
    @property
    def model(self) -> SentenceTransformer:
        """Get the sentence transformer model."""
        return self._model
    
    @property
    def dimension(self) -> int:
        """Get the embedding dimension."""
        return self._model.get_sentence_embedding_dimension()
    
    def encode(self, texts: Union[str, List[str]], normalize: bool = True) -> np.ndarray:
        """
        Generate embeddings for one or more texts.
        
        Args:
            texts: Single text or list of texts to encode
            normalize: Whether to normalize embeddings (for cosine similarity)
            
        Returns:
            Numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self._model.encode(
            texts,
            normalize_embeddings=normalize,
            show_progress_bar=len(texts) > 10
        )
        
        return embeddings
    
    def encode_single(self, text: str, normalize: bool = True) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to encode
            normalize: Whether to normalize embedding
            
        Returns:
            List of floats representing the embedding
        """
        embedding = self.encode(text, normalize=normalize)
        return embedding[0].tolist()
    
    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Cosine similarity score (0-1)
        """
        embeddings = self.encode([text1, text2], normalize=True)
        return float(np.dot(embeddings[0], embeddings[1]))
    
    def batch_similarity(self, query: str, documents: List[str]) -> List[float]:
        """
        Calculate similarity between a query and multiple documents.
        
        Args:
            query: Query text
            documents: List of document texts
            
        Returns:
            List of similarity scores
        """
        query_embedding = self.encode(query, normalize=True)[0]
        doc_embeddings = self.encode(documents, normalize=True)
        
        similarities = np.dot(doc_embeddings, query_embedding)
        return similarities.tolist()


# Singleton instance
embedding_service = EmbeddingService()


if __name__ == "__main__":
    # Test the embedding service
    service = EmbeddingService()
    
    test_texts = [
        "Test failure: Element not found - button[@id='submit']",
        "Test failure: Timeout waiting for element - button[@id='login']",
        "Test passed: Login successful",
    ]
    
    print(f"Model: {settings.EMBEDDING_MODEL}")
    print(f"Dimension: {service.dimension}")
    
    embeddings = service.encode(test_texts)
    print(f"Embeddings shape: {embeddings.shape}")
    
    # Test similarity
    sim = service.similarity(test_texts[0], test_texts[1])
    print(f"Similarity between failures: {sim:.4f}")
    
    sim2 = service.similarity(test_texts[0], test_texts[2])
    print(f"Similarity failure vs pass: {sim2:.4f}")

