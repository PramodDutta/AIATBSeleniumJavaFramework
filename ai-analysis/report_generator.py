"""Beautiful HTML Report Generator for AI Test Analysis."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import sys

sys.path.insert(0, str(Path(__file__).parent))
from src.log_parser import LogParser
from config import settings


def generate_html_report(output_path: str = "test_report.html") -> str:
    """Generate a beautiful HTML report from test logs."""
    
    parser = LogParser(settings.LOGS_PATH)
    events = list(parser.parse_all())
    
    if not events:
        print("No test events found!")
        return ""
    
    # Calculate statistics
    total_tests = len([e for e in events if e.status in ['PASSED', 'FAILED']])
    passed = len([e for e in events if e.status == 'PASSED'])
    failed = len([e for e in events if e.status == 'FAILED'])
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    
    failures = [e for e in events if e.status == 'FAILED']
    passes = [e for e in events if e.status == 'PASSED']
    
    # Calculate durations
    durations = [e.duration_ms for e in events if e.duration_ms and e.duration_ms > 0]
    avg_duration = sum(durations) / len(durations) if durations else 0
    max_duration = max(durations) if durations else 0
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Test Analysis Report</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .gradient-bg {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .card {{ background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .success {{ color: #10B981; }}
        .failure {{ color: #EF4444; }}
        .pulse {{ animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
    </style>
</head>
<body class="bg-gray-100 min-h-screen">
    <!-- Header -->
    <header class="gradient-bg text-white py-8 px-4">
        <div class="max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold flex items-center gap-3">
                        <i class="fas fa-flask"></i>
                        AI Test Analysis Report
                    </h1>
                    <p class="text-purple-200 mt-2">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                <div class="text-right">
                    <p class="text-sm text-purple-200">Powered by</p>
                    <p class="font-semibold">The Testing Academy</p>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-8 px-4">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="card p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-500 text-sm">Total Tests</p>
                        <p class="text-3xl font-bold text-gray-800">{total_tests}</p>
                    </div>
                    <div class="bg-blue-100 p-3 rounded-full">
                        <i class="fas fa-list-check text-blue-600 text-xl"></i>
                    </div>
                </div>
            </div>
            <div class="card p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-500 text-sm">Passed</p>
                        <p class="text-3xl font-bold success">{passed}</p>
                    </div>
                    <div class="bg-green-100 p-3 rounded-full">
                        <i class="fas fa-check-circle text-green-600 text-xl"></i>
                    </div>
                </div>
            </div>
            <div class="card p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-500 text-sm">Failed</p>
                        <p class="text-3xl font-bold failure">{failed}</p>
                    </div>
                    <div class="bg-red-100 p-3 rounded-full">
                        <i class="fas fa-times-circle text-red-600 text-xl"></i>
                    </div>
                </div>
            </div>
            <div class="card p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-500 text-sm">Pass Rate</p>
                        <p class="text-3xl font-bold text-purple-600">{pass_rate:.1f}%</p>
                    </div>
                    <div class="bg-purple-100 p-3 rounded-full">
                        <i class="fas fa-percentage text-purple-600 text-xl"></i>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="card p-6">
                <h2 class="text-xl font-semibold mb-4">Test Results Distribution</h2>
                <canvas id="pieChart" height="200"></canvas>
            </div>
            <div class="card p-6">
                <h2 class="text-xl font-semibold mb-4">Test Duration (ms)</h2>
                <canvas id="barChart" height="200"></canvas>
            </div>
        </div>

        <!-- Failures Section -->
        <div class="card p-6 mb-8">
            <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
                <i class="fas fa-exclamation-triangle text-red-500"></i>
                Failed Tests ({failed})
            </h2>
            {"".join(_generate_failure_cards(failures)) if failures else '<p class="text-green-600 flex items-center gap-2"><i class="fas fa-check-circle"></i> All tests passed!</p>'}
        </div>

        <!-- Passed Tests Section -->
        <div class="card p-6 mb-8">
            <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
                <i class="fas fa-check-circle text-green-500"></i>
                Passed Tests ({passed})
            </h2>
            <div class="space-y-2">
                {"".join(_generate_pass_items(passes))}
            </div>
        </div>

        <!-- AI Analysis Info -->
        <div class="card p-6 bg-gradient-to-r from-purple-50 to-blue-50">
            <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
                <i class="fas fa-brain text-purple-600"></i>
                AI Analysis Available
            </h2>
            <p class="text-gray-600 mb-4">
                This report is enhanced with AI-powered similarity search. Find similar past failures 
                using semantic embeddings - no data leaves your machine!
            </p>
            <div class="flex gap-4">
                <div class="bg-white rounded-lg p-4 flex-1">
                    <p class="font-semibold text-purple-600">Local AI Model</p>
                    <p class="text-sm text-gray-500">all-MiniLM-L6-v2 (384 dimensions)</p>
                </div>
                <div class="bg-white rounded-lg p-4 flex-1">
                    <p class="font-semibold text-purple-600">Vector Database</p>
                    <p class="text-sm text-gray-500">Qdrant (in-memory)</p>
                </div>
                <div class="bg-white rounded-lg p-4 flex-1">
                    <p class="font-semibold text-purple-600">Privacy</p>
                    <p class="text-sm text-gray-500">100% Local Processing</p>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-6 mt-8">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p class="text-gray-400">
                Generated by <strong>AI Test Analysis Framework</strong> | 
                <a href="https://thetestingacademy.com" class="text-purple-400 hover:text-purple-300">The Testing Academy</a>
            </p>
        </div>
    </footer>
"""
    
    # Add JavaScript for charts
    html += _generate_chart_scripts(passed, failed, events)
    html += "</body></html>"
    
    # Write to file
    output_file = Path(output_path)
    output_file.write_text(html)
    print(f"✅ Report generated: {output_file.absolute()}")

    return str(output_file.absolute())


def _generate_failure_cards(failures: list) -> list:
    """Generate HTML cards for failures."""
    cards = []
    for f in failures:
        card = f"""
        <div class="border-l-4 border-red-500 bg-red-50 p-4 mb-4 rounded-r-lg">
            <div class="flex items-start justify-between">
                <div>
                    <h3 class="font-semibold text-red-800">{f.test_name}</h3>
                    <p class="text-sm text-gray-600">{f.class_name}</p>
                </div>
                <span class="bg-red-100 text-red-800 px-2 py-1 rounded text-sm">
                    {f.duration_ms or 0}ms
                </span>
            </div>
            <div class="mt-3">
                <p class="text-sm text-gray-700 bg-white p-2 rounded border">
                    {(f.message or 'No error message')[:300]}{'...' if f.message and len(f.message) > 300 else ''}
                </p>
            </div>
            {f'<details class="mt-2"><summary class="text-sm text-gray-500 cursor-pointer">View Stacktrace</summary><pre class="text-xs bg-gray-900 text-gray-100 p-3 rounded mt-2 overflow-x-auto">{f.stacktrace[:1000] if f.stacktrace else "No stacktrace"}</pre></details>' if f.stacktrace else ''}
        </div>
        """
        cards.append(card)
    return cards


def _generate_pass_items(passes: list) -> list:
    """Generate HTML items for passed tests."""
    items = []
    for p in passes:
        item = f"""
        <div class="flex items-center justify-between p-3 bg-green-50 rounded-lg">
            <div class="flex items-center gap-3">
                <i class="fas fa-check-circle text-green-500"></i>
                <div>
                    <span class="font-medium text-gray-800">{p.test_name}</span>
                    <span class="text-sm text-gray-500 ml-2">({p.class_name})</span>
                </div>
            </div>
            <span class="text-sm text-gray-500">{p.duration_ms or 0}ms</span>
        </div>
        """
        items.append(item)
    return items


def _generate_chart_scripts(passed: int, failed: int, events: list) -> str:
    """Generate JavaScript for charts."""
    # Get duration data
    duration_data = []
    for e in events:
        if e.status in ['PASSED', 'FAILED'] and e.duration_ms and e.duration_ms > 0:
            duration_data.append({
                'name': e.test_name[:20],
                'duration': e.duration_ms,
                'status': e.status
            })

    labels = [d['name'] for d in duration_data]
    durations = [d['duration'] for d in duration_data]
    colors = ['#10B981' if d['status'] == 'PASSED' else '#EF4444' for d in duration_data]

    return f"""
    <script>
        // Pie Chart
        new Chart(document.getElementById('pieChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['Passed', 'Failed'],
                datasets: [{{
                    data: [{passed}, {failed}],
                    backgroundColor: ['#10B981', '#EF4444'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'bottom' }}
                }}
            }}
        }});

        // Bar Chart
        new Chart(document.getElementById('barChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Duration (ms)',
                    data: {json.dumps(durations)},
                    backgroundColor: {json.dumps(colors)},
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});
    </script>
    """


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate HTML test report")
    parser.add_argument("-o", "--output", default="test_report.html", help="Output file path")
    args = parser.parse_args()

    generate_html_report(args.output)

