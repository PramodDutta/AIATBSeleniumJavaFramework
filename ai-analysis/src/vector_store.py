"""Qdrant vector store for test failure embeddings."""

from typing import List, Optional, Dict, Any
from dataclasses import asdict
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

import sys
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
from config import settings
from src.log_parser import TestEvent
from src.embedding_service import embedding_service


class VectorStore:
    """Qdrant-based vector store for test failure analysis."""
    
    def __init__(self, in_memory: bool = True):
        """
        Initialize the vector store.
        
        Args:
            in_memory: If True, use in-memory Qdrant (no server needed)
        """
        if in_memory:
            self.client = QdrantClient(":memory:")
        else:
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
            )
        
        self.collection_name = settings.QDRANT_COLLECTION
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                ),
            )
            print(f"Created collection: {self.collection_name}")
    
    def index_failure(self, event: TestEvent) -> str:
        """
        Index a single test failure event.
        
        Args:
            event: TestEvent representing a failure
            
        Returns:
            Point ID
        """
        if not event.is_failure:
            raise ValueError("Can only index failure events")
        
        # Generate embedding
        text = event.to_embedding_text()
        embedding = embedding_service.encode_single(text)
        
        # Create point
        point_id = str(uuid.uuid4())
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "event_id": event.event_id,
                        "test_id": event.test_id,
                        "test_name": event.test_name,
                        "class_name": event.class_name,
                        "suite": event.suite,
                        "message": event.message,
                        "stacktrace": event.stacktrace or "",
                        "timestamp": event.timestamp,
                        "duration_ms": event.duration_ms,
                        "embedding_text": text,
                    },
                )
            ],
        )
        
        return point_id
    
    def index_failures(self, events: List[TestEvent]) -> int:
        """
        Index multiple test failure events.
        
        Args:
            events: List of TestEvent failures
            
        Returns:
            Number of indexed events
        """
        failures = [e for e in events if e.is_failure]
        
        for event in failures:
            self.index_failure(event)
        
        return len(failures)
    
    def search_similar(
        self,
        query_text: str,
        top_k: int = None,
        threshold: float = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar failures based on text query.

        Args:
            query_text: Text describing the failure to search for
            top_k: Number of results to return
            threshold: Minimum similarity score

        Returns:
            List of similar failures with scores
        """
        top_k = top_k or settings.TOP_K_RESULTS
        threshold = threshold or settings.SIMILARITY_THRESHOLD

        # Generate query embedding
        query_embedding = embedding_service.encode_single(query_text)

        # Search using query_points (newer Qdrant API)
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=top_k,
            score_threshold=threshold,
        )

        return [
            {
                "score": hit.score,
                "test_name": hit.payload.get("test_name"),
                "class_name": hit.payload.get("class_name"),
                "message": hit.payload.get("message"),
                "stacktrace": hit.payload.get("stacktrace"),
                "timestamp": hit.payload.get("timestamp"),
            }
            for hit in results.points
        ]
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        info = self.client.get_collection(self.collection_name)
        return {
            "name": self.collection_name,
            "points_count": info.points_count,
        }

