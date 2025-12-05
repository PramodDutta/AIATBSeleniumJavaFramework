"""Test failure analysis service combining all components."""

from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from collections import Counter

import sys
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
from config import settings
from src.log_parser import LogParser, TestEvent
from src.embedding_service import embedding_service
from src.vector_store import VectorStore


class AnalysisService:
    """Main service for AI-powered test failure analysis."""
    
    def __init__(self, log_path: Optional[Path] = None):
        """Initialize the analysis service."""
        self.log_path = log_path or settings.LOGS_PATH
        self.parser = LogParser(self.log_path)
        self.vector_store = VectorStore(in_memory=True)
        self._indexed = False
    
    def load_and_index(self) -> Dict[str, int]:
        """Load logs and index all failures."""
        events = self.parser.get_all_events()
        failures = [e for e in events if e.is_failure]
        
        indexed_count = self.vector_store.index_failures(failures)
        self._indexed = True
        
        return {
            "total_events": len(events),
            "failures_indexed": indexed_count,
            "passed": len([e for e in events if e.status == "PASSED"]),
            "started": len([e for e in events if e.status == "STARTED"]),
        }
    
    def find_similar_failures(
        self,
        error_message: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Find similar past failures based on error message.
        
        Args:
            error_message: The error message to search for
            top_k: Number of similar results to return
            
        Returns:
            List of similar failures with similarity scores
        """
        if not self._indexed:
            self.load_and_index()
        
        return self.vector_store.search_similar(
            query_text=error_message,
            top_k=top_k,
        )
    
    def analyze_failure(self, event: TestEvent) -> Dict[str, Any]:
        """
        Analyze a single test failure.
        
        Args:
            event: TestEvent to analyze
            
        Returns:
            Analysis results including similar failures and patterns
        """
        if not event.is_failure:
            return {"error": "Not a failure event"}
        
        similar = self.find_similar_failures(event.to_embedding_text())
        
        # Pattern analysis
        patterns = self._extract_patterns(event, similar)
        
        return {
            "test_name": event.test_name,
            "class_name": event.class_name,
            "error_message": event.message,
            "similar_failures": similar,
            "patterns": patterns,
            "recommendation": self._generate_recommendation(event, similar, patterns),
        }
    
    def _extract_patterns(
        self,
        event: TestEvent,
        similar: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Extract failure patterns from similar failures."""
        if not similar:
            return {"recurring": False, "frequency": 0}
        
        # Check for recurring patterns
        test_names = [s["test_name"] for s in similar]
        class_names = [s["class_name"] for s in similar]
        
        test_counts = Counter(test_names)
        class_counts = Counter(class_names)
        
        return {
            "recurring": len(similar) > 0 and any(s["score"] > 0.85 for s in similar),
            "frequency": len(similar),
            "affected_tests": dict(test_counts.most_common(5)),
            "affected_classes": dict(class_counts.most_common(5)),
            "avg_similarity": sum(s["score"] for s in similar) / len(similar) if similar else 0,
        }
    
    def _generate_recommendation(
        self,
        event: TestEvent,
        similar: List[Dict[str, Any]],
        patterns: Dict[str, Any],
    ) -> str:
        """Generate a recommendation based on analysis."""
        recommendations = []
        
        if patterns.get("recurring"):
            recommendations.append(
                f"⚠️ This appears to be a RECURRING failure. "
                f"Found {patterns['frequency']} similar failures."
            )
        
        if patterns.get("avg_similarity", 0) > 0.9:
            recommendations.append(
                "🔴 Very high similarity with past failures - likely same root cause."
            )
        
        # Check for common error types
        msg = event.message.lower()
        if "timeout" in msg:
            recommendations.append(
                "⏱️ Timeout error detected. Consider increasing wait times or checking element locators."
            )
        elif "element not found" in msg or "nosuchelement" in msg:
            recommendations.append(
                "🔍 Element not found. Verify locator strategy and page load state."
            )
        elif "assertion" in msg:
            recommendations.append(
                "✅ Assertion failure. Check expected vs actual values in test data."
            )
        
        if not recommendations:
            recommendations.append(
                "ℹ️ Review the stacktrace for more details on this failure."
            )
        
        return " ".join(recommendations)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all analyzed failures."""
        events = self.parser.get_all_events()
        failures = [e for e in events if e.is_failure]
        
        return {
            "total_tests": len([e for e in events if e.status in ["PASSED", "FAILED"]]),
            "total_failures": len(failures),
            "failure_rate": len(failures) / len(events) * 100 if events else 0,
            "failures_by_class": dict(Counter(f.class_name for f in failures).most_common()),
            "failures_by_test": dict(Counter(f.test_name for f in failures).most_common()),
            "index_info": self.vector_store.get_collection_info(),
        }

