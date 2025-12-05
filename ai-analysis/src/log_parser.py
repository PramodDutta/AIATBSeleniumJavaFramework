"""Parser for test analytics JSONL logs."""

import json
from pathlib import Path
from typing import Generator, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TestEvent:
    """Represents a single test event from the analytics logs."""
    event_id: str
    timestamp: str
    test_id: str
    test_name: str
    suite: str
    class_name: str
    environment: str
    level: str
    status: str
    message: str
    stacktrace: Optional[str] = None
    duration_ms: int = 0
    service: str = "selenium-ui-tests"
    attributes: dict = field(default_factory=dict)
    
    @property
    def is_failure(self) -> bool:
        """Check if this event represents a test failure."""
        return self.status == "FAILED" and self.level == "ERROR"
    
    @property
    def failure_signature(self) -> str:
        """Generate a searchable signature for this failure."""
        if not self.is_failure:
            return ""
        
        parts = [
            f"Test: {self.test_name}",
            f"Class: {self.class_name}",
            f"Error: {self.message}",
        ]
        
        if self.stacktrace:
            # Extract first meaningful line from stacktrace
            lines = self.stacktrace.split("\n")
            for line in lines[:5]:
                if line.strip() and not line.startswith("\t"):
                    parts.append(f"Exception: {line.strip()}")
                    break
        
        return " | ".join(parts)
    
    def to_embedding_text(self) -> str:
        """Generate text suitable for embedding generation."""
        text_parts = [
            f"Test failure in {self.test_name}",
            f"Class: {self.class_name}",
            f"Suite: {self.suite}",
            f"Error message: {self.message}",
        ]
        
        if self.stacktrace:
            # Include relevant parts of stacktrace
            stack_lines = self.stacktrace.split("\n")[:10]
            text_parts.append(f"Stacktrace: {' '.join(stack_lines)}")
        
        return " ".join(text_parts)


class LogParser:
    """Parser for JSONL test analytics logs."""
    
    def __init__(self, log_path: Path):
        """Initialize parser with path to JSONL file."""
        self.log_path = log_path
    
    def parse_line(self, line: str) -> Optional[TestEvent]:
        """Parse a single JSONL line into a TestEvent."""
        try:
            data = json.loads(line.strip())
            return TestEvent(
                event_id=data.get("eventId", ""),
                timestamp=data.get("timestamp", ""),
                test_id=data.get("testId", ""),
                test_name=data.get("testName", ""),
                suite=data.get("suite", ""),
                class_name=data.get("className", ""),
                environment=data.get("environment", "local"),
                level=data.get("level", "INFO"),
                status=data.get("status", ""),
                message=data.get("message", ""),
                stacktrace=data.get("stacktrace"),
                duration_ms=data.get("durationMs", 0),
                service=data.get("service", "selenium-ui-tests"),
                attributes=data.get("attributes", {}),
            )
        except json.JSONDecodeError as e:
            print(f"Failed to parse line: {e}")
            return None
    
    def parse_all(self) -> Generator[TestEvent, None, None]:
        """Parse all events from the log file."""
        if not self.log_path.exists():
            print(f"Log file not found: {self.log_path}")
            return
        
        with open(self.log_path, "r") as f:
            for line in f:
                if line.strip():
                    event = self.parse_line(line)
                    if event:
                        yield event
    
    def get_failures(self) -> list[TestEvent]:
        """Get all failure events from the logs."""
        return [event for event in self.parse_all() if event.is_failure]
    
    def get_all_events(self) -> list[TestEvent]:
        """Get all events from the logs."""
        return list(self.parse_all())


if __name__ == "__main__":
    # Test the parser
    from config import settings
    
    parser = LogParser(settings.LOGS_PATH)
    failures = parser.get_failures()
    
    print(f"Found {len(failures)} failure(s)")
    for failure in failures:
        print(f"\n--- Failure ---")
        print(f"Test: {failure.test_name}")
        print(f"Message: {failure.message[:100]}...")
        print(f"Embedding text: {failure.to_embedding_text()[:200]}...")

