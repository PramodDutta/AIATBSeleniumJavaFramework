"""FastAPI REST API for AI Test Analysis."""

from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
from config import settings
from src.analysis_service import AnalysisService


# Initialize FastAPI
app = FastAPI(
    title="AI Test Analysis API",
    description="API for analyzing Selenium test failures using AI/ML",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analysis service (lazy loading)
analysis_service: Optional[AnalysisService] = None


def get_analysis_service() -> AnalysisService:
    """Get or create the analysis service singleton."""
    global analysis_service
    if analysis_service is None:
        analysis_service = AnalysisService()
    return analysis_service


# Request/Response Models
class SimilarFailureQuery(BaseModel):
    """Query model for finding similar failures."""
    error_message: str = Field(..., description="Error message to search for")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results")


class AnalyzeFailureRequest(BaseModel):
    """Request model for analyzing a specific failure."""
    test_name: str = Field(..., description="Name of the test")
    class_name: str = Field(..., description="Full class name")
    error_message: str = Field(..., description="Error message")
    stacktrace: Optional[str] = Field(None, description="Full stacktrace")


class SimilarFailure(BaseModel):
    """Response model for a similar failure."""
    score: float
    test_name: str
    class_name: str
    message: str
    timestamp: Optional[str]


class AnalysisResponse(BaseModel):
    """Response model for failure analysis."""
    test_name: str
    class_name: str
    error_message: str
    similar_failures: List[SimilarFailure]
    patterns: dict
    recommendation: str


# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Test Analysis API",
        "version": "1.0.0",
    }


@app.post("/api/v1/index")
async def index_logs():
    """Load and index all test failure logs."""
    service = get_analysis_service()
    result = service.load_and_index()
    return {
        "status": "success",
        "message": "Logs indexed successfully",
        **result,
    }


@app.post("/api/v1/similar", response_model=List[SimilarFailure])
async def find_similar_failures(query: SimilarFailureQuery):
    """Find similar past failures based on error message."""
    service = get_analysis_service()
    
    if not service._indexed:
        service.load_and_index()
    
    results = service.find_similar_failures(
        error_message=query.error_message,
        top_k=query.top_k,
    )
    
    return results


@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_failure(request: AnalyzeFailureRequest):
    """Analyze a test failure and get recommendations."""
    service = get_analysis_service()
    
    if not service._indexed:
        service.load_and_index()
    
    from src.log_parser import TestEvent
    
    # Create a mock event for analysis
    event = TestEvent(
        event_id="query",
        timestamp="",
        test_id=f"{request.class_name}.{request.test_name}",
        test_name=request.test_name,
        suite="Query",
        class_name=request.class_name,
        environment="query",
        level="ERROR",
        status="FAILED",
        message=request.error_message,
        stacktrace=request.stacktrace,
    )
    
    result = service.analyze_failure(event)
    return result


@app.get("/api/v1/summary")
async def get_summary():
    """Get a summary of all test failures."""
    service = get_analysis_service()
    
    if not service._indexed:
        service.load_and_index()
    
    return service.get_summary()


@app.get("/api/v1/health")
async def health_check():
    """Detailed health check."""
    service = get_analysis_service()
    return {
        "status": "healthy",
        "log_path": str(settings.LOGS_PATH),
        "log_exists": settings.LOGS_PATH.exists(),
        "indexed": service._indexed if service else False,
        "collection": service.vector_store.get_collection_info() if service and service._indexed else None,
    }

