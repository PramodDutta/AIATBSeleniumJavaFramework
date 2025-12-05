#!/usr/bin/env python3
"""Main entry point for AI Test Analysis Pipeline."""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings


def run_api(host: str = None, port: int = None):
    """Run the FastAPI server."""
    import uvicorn
    from src.api import app
    
    uvicorn.run(
        app,
        host=host or settings.API_HOST,
        port=port or settings.API_PORT,
        reload=False,
    )


def run_analysis():
    """Run analysis on current logs and print summary."""
    from src.analysis_service import AnalysisService
    
    print(f"\n📊 AI Test Analysis Pipeline")
    print(f"{'=' * 50}")
    print(f"Log file: {settings.LOGS_PATH}")
    
    if not settings.LOGS_PATH.exists():
        print(f"\n❌ Log file not found: {settings.LOGS_PATH}")
        print("Run tests first: ./mvnw clean test")
        return
    
    service = AnalysisService()
    
    # Load and index
    print(f"\n📥 Loading and indexing logs...")
    stats = service.load_and_index()
    
    print(f"\n📈 Index Statistics:")
    print(f"  Total events: {stats['total_events']}")
    print(f"  Tests passed: {stats['passed']}")
    print(f"  Failures indexed: {stats['failures_indexed']}")
    
    # Get summary
    summary = service.get_summary()
    
    print(f"\n📋 Failure Summary:")
    print(f"  Total tests: {summary['total_tests']}")
    print(f"  Total failures: {summary['total_failures']}")
    print(f"  Failure rate: {summary['failure_rate']:.1f}%")
    
    if summary['failures_by_test']:
        print(f"\n🔴 Failures by Test:")
        for test, count in summary['failures_by_test'].items():
            print(f"  - {test}: {count}")
    
    # Analyze each failure
    from src.log_parser import LogParser
    parser = LogParser(settings.LOGS_PATH)
    failures = parser.get_failures()
    
    if failures:
        print(f"\n🔍 Detailed Analysis:")
        for failure in failures:
            print(f"\n{'─' * 50}")
            analysis = service.analyze_failure(failure)
            print(f"Test: {analysis['test_name']}")
            print(f"Class: {analysis['class_name']}")
            print(f"Error: {analysis['error_message'][:100]}...")
            print(f"\n💡 Recommendation:")
            print(f"  {analysis['recommendation']}")
            
            if analysis['similar_failures']:
                print(f"\n📎 Similar Failures Found: {len(analysis['similar_failures'])}")
    
    print(f"\n{'=' * 50}")
    print(f"✅ Analysis complete!")
    print(f"\nTo start the API server, run:")
    print(f"  python main.py serve")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Test Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the API server")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Run analysis on logs")
    
    args = parser.parse_args()
    
    if args.command == "serve":
        print(f"🚀 Starting AI Test Analysis API at http://{args.host}:{args.port}")
        print(f"📚 API docs at http://localhost:{args.port}/docs")
        run_api(args.host, args.port)
    elif args.command == "analyze":
        run_analysis()
    else:
        # Default: run analysis
        run_analysis()


if __name__ == "__main__":
    main()

