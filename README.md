# 🔬 AI-Powered Test Automation Framework

[![Java](https://img.shields.io/badge/Java-17+-orange.svg)](https://openjdk.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.27-green.svg)](https://selenium.dev/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **A comprehensive Selenium Java test automation framework with AI-powered failure analysis using local embeddings - no data leaves your machine!**

**Author:** [Pramod Dutta](https://thetestingacademy.com)  
**Website:** [The Testing Academy](https://thetestingacademy.com)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Step-by-Step Setup](#-step-by-step-setup)
- [Running Tests](#-running-tests)
- [AI Analysis Dashboard](#-ai-analysis-dashboard)
- [How AI Similarity Search Works](#-how-ai-similarity-search-works)
- [Configuration](#-configuration)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)

---

## ✨ Features

### Test Automation Framework (Java)
- ✅ **Page Object Model (POM)** - Clean separation of test logic and page elements
- ✅ **Selenium 4.27** - Latest Selenium with built-in WebDriver Manager
- ✅ **TestNG** - Powerful test framework with parallel execution support
- ✅ **Allure Reporting** - Beautiful test reports with screenshots on failure
- ✅ **Automatic Screenshots** - Captures screenshots, page source, and URL on test failure
- ✅ **Structured Logging** - JSONL format logs for AI analysis

### AI Analysis Pipeline (Python)
- 🧠 **Local AI Embeddings** - Sentence-Transformers running 100% locally
- 🔍 **Semantic Similarity Search** - Find similar failures by meaning, not just keywords
- 📊 **Interactive Dashboard** - Streamlit-based UI for visualizing test results
- 🔒 **Privacy First** - No data leaves your machine, no external API calls
- 📈 **Analytics** - Track failure patterns, test duration, and trends

---

<img width="3600" height="3972" alt="image" src="https://github.com/user-attachments/assets/ee4079b7-f789-4c6a-9df0-fc58762fcbb3" />


## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TEST AUTOMATION FRAMEWORK                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │  Test Cases  │───▶│  Page Objects │───▶│   Selenium   │          │
│  │  (TestNG)    │    │    (POM)      │    │   WebDriver  │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   Allure     │    │   JSONL      │    │  Screenshots │          │
│  │   Reports    │    │   Logs       │    │  on Failure  │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                             │                                       │
└─────────────────────────────┼───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AI ANALYSIS PIPELINE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │  Log Parser  │───▶│  Embeddings  │───▶│   Qdrant     │          │
│  │  (Python)    │    │  (Local AI)  │    │ Vector Store │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                 │                   │
│                                                 ▼                   │
│                      ┌──────────────────────────────────┐          │
│                      │      Streamlit Dashboard         │          │
│                      │  - Metrics & Charts              │          │
│                      │  - Failure Analysis              │          │
│                      │  - Similarity Search             │          │
│                      └──────────────────────────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Java JDK** | 17+ | Running Selenium tests |
| **Maven** | 3.8+ | Build and dependency management |
| **Python** | 3.9+ | AI analysis pipeline |
| **Chrome/Firefox** | Latest | Browser for testing |

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/pramods12/AIATBSeleniumJavaFramework.git
cd AIATBSeleniumJavaFramework

# 2. Install Java (macOS)
brew install openjdk@17

# 3. Run tests
./mvnw clean test

# 4. View Allure report
./mvnw allure:serve

# 5. Setup AI Analysis
cd ai-analysis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Launch Dashboard
streamlit run dashboard.py
```

---

## 📁 Project Structure

```
AIATBSeleniumJavaFramework/
├── 📄 pom.xml                      # Maven configuration
├── 📄 testng.xml                   # TestNG suite configuration
├── 📄 mvnw                         # Maven wrapper
│
├── 📂 src/
│   ├── 📂 main/java/com/automation/
│   │   ├── 📂 pages/               # Page Object classes
│   │   │   ├── BasePage.java
│   │   │   ├── LoginPage.java
│   │   │   └── DashboardPage.java
│   │   ├── 📂 listeners/           # TestNG listeners
│   │   │   └── AllureScreenshotListener.java
│   │   └── 📂 analytics/           # Test analytics
│   │       └── TestAnalyticsLogger.java
│   │
│   └── 📂 test/java/com/automation/
│       ├── 📂 base/                # Base test class
│       │   └── BaseTest.java
│       └── 📂 tests/               # Test classes
│           └── LoginTest.java
│
├── 📂 ai-analysis/                 # AI Analysis Pipeline
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 dashboard.py             # Streamlit dashboard
│   ├── 📄 main.py                  # CLI entry point
│   ├── 📂 config/
│   │   └── settings.py             # Configuration
│   └── 📂 src/
│       ├── log_parser.py           # JSONL log parser
│       ├── embedding_service.py    # Local AI embeddings
│       ├── vector_store.py         # Qdrant vector database
│       ├── analysis_service.py     # Analysis orchestration
│       └── api.py                  # FastAPI REST API
│
└── 📂 target/                      # Build output
    ├── 📂 allure-results/          # Allure report data
    └── 📂 analytics-logs/          # JSONL test logs
        └── test-events.jsonl
```

---

## 📝 Step-by-Step Setup

### Step 1: Install Java JDK 17+

**macOS (Homebrew):**
```bash
brew install openjdk@17
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
java -version
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install openjdk-17-jdk
java -version
```

**Windows:**
1. Download from [Adoptium](https://adoptium.net/temurin/releases/)
2. Run installer
3. Add to PATH

### Step 2: Clone and Build Project

```bash
# Clone repository
git clone https://github.com/yourusername/AIATBSeleniumJavaFramework.git
cd AIATBSeleniumJavaFramework

# Make Maven wrapper executable
chmod +x mvnw

# Build project (downloads dependencies)
./mvnw clean compile
```

### Step 3: Run Tests

```bash
# Run all tests
./mvnw clean test

# Run specific test class
./mvnw test -Dtest=LoginTest

# Run with specific browser (if configured)
./mvnw test -Dbrowser=firefox
```

### Step 4: View Allure Report

```bash
# Generate and open Allure report
./mvnw allure:serve
```

This opens a beautiful HTML report showing:
- ✅ Test results with pass/fail status
- 📸 Screenshots on failure
- 📄 Page source on failure
- 🔗 URLs where tests failed

### Step 5: Setup AI Analysis Pipeline

```bash
# Navigate to AI analysis directory
cd ai-analysis

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# First run downloads the AI model (~90MB, one-time)
```

### Step 6: Launch Dashboard

```bash
# Make sure you're in ai-analysis directory with venv activated
cd ai-analysis
source venv/bin/activate

# Launch Streamlit dashboard
streamlit run dashboard.py --server.port 8501
```

Open http://localhost:8501 in your browser.

### Step 7: Use the REST API (Optional)

```bash
# Start API server
python main.py serve

# Index test logs
curl -X POST http://localhost:8000/api/v1/index

# Get summary
curl http://localhost:8000/api/v1/summary

# Find similar failures
curl -X POST http://localhost:8000/api/v1/similar \
  -H "Content-Type: application/json" \
  -d '{"error_message": "Element not found"}'
```

---

## 🧪 Running Tests

### Basic Commands

```bash
# Run all tests
./mvnw clean test

# Run with Allure report generation
./mvnw clean test allure:serve

# Run specific test class
./mvnw test -Dtest=LoginTest

# Run specific test method
./mvnw test -Dtest=LoginTest#testSuccessfulLogin

# Run tests in parallel (configured in testng.xml)
./mvnw test -Dparallel=methods -DthreadCount=4
```

### Test Output Locations

| Output | Location | Description |
|--------|----------|-------------|
| Test Results | `target/surefire-reports/` | TestNG XML reports |
| Allure Data | `target/allure-results/` | Allure report data |
| Analytics Logs | `target/analytics-logs/test-events.jsonl` | JSONL for AI analysis |
| Screenshots | `target/allure-results/*.png` | Failure screenshots |

---

## 📊 AI Analysis Dashboard

### Dashboard Pages

| Page | Description |
|------|-------------|
| **📊 Dashboard** | Overview with pass/fail metrics, pie charts, duration analysis |
| **📋 Test Events** | Full list of all test events with filters and CSV export |
| **🔴 Failures** | Detailed failure view with error messages and stacktraces |
| **🔍 Similar Search** | AI-powered semantic search for similar past failures |
| **📈 Analytics** | Timeline visualization, failures by class, duration statistics |

### Screenshots

The dashboard provides:
- Real-time test metrics
- Interactive charts (Plotly)
- Semantic similarity search
- CSV export functionality
- Failure pattern analysis

---

## 🧠 How AI Similarity Search Works

### The Problem with Traditional Search

```
Traditional Keyword Search:
  "Connection timeout" ≠ "Network unavailable"  ❌ No match!

AI Embedding Search:
  "Connection timeout" ≈ "Network unavailable"  ✅ 85% similar!
```

### How Embeddings Work

1. **Text → Vector**: Error messages are converted to 384-dimensional vectors
2. **Semantic Meaning**: Similar meanings = similar vectors
3. **Cosine Similarity**: Find closest matches in vector space

```
Error Message                          → Vector (384 numbers)
─────────────────────────────────────────────────────────────
"Element not found: login button"      → [0.23, -0.15, 0.87, ...]
"Could not locate login button"        → [0.21, -0.14, 0.85, ...]  ← 92% Similar!
"Database connection failed"           → [-0.45, 0.32, 0.11, ...]  ← Different
```

### Privacy: 100% Local

| Component | Location | Data Sharing |
|-----------|----------|--------------|
| Sentence-Transformers | Local CPU | Model downloaded once, runs offline |
| Qdrant Vector DB | In-memory | Data stays in RAM |
| Dashboard | localhost | Never exposed externally |

**No data leaves your machine!**

---

## ⚙️ Configuration

### Java Framework Configuration

**testng.xml** - Test suite configuration:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Automation Test Suite" parallel="methods" thread-count="2">
    <listeners>
        <listener class-name="io.qameta.allure.testng.AllureTestNg"/>
        <listener class-name="com.automation.listeners.AllureScreenshotListener"/>
    </listeners>
    <test name="Login Tests">
        <classes>
            <class name="com.automation.tests.LoginTest"/>
        </classes>
    </test>
</suite>
```

### AI Analysis Configuration

**ai-analysis/config/settings.py**:
```python
# Paths
LOGS_PATH = "../target/analytics-logs/test-events.jsonl"

# Embedding Model (runs locally)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384 dimensions
EMBEDDING_DIMENSION = 384

# Vector Store
QDRANT_COLLECTION = "test_failures"
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity score
```

---

## 🔌 API Reference

### REST API Endpoints

Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/v1/health` | GET | Detailed health status |
| `/api/v1/index` | POST | Load and index test logs |
| `/api/v1/summary` | GET | Get failure summary |
| `/api/v1/similar` | POST | Find similar failures |
| `/api/v1/analyze` | POST | Analyze specific failure |

### Example API Calls

```bash
# Health check
curl http://localhost:8000/

# Index logs
curl -X POST http://localhost:8000/api/v1/index

# Get summary
curl http://localhost:8000/api/v1/summary

# Find similar failures
curl -X POST http://localhost:8000/api/v1/similar \
  -H "Content-Type: application/json" \
  -d '{
    "error_message": "Element not found: login button",
    "top_k": 5
  }'
```

### API Response Examples

**Index Response:**
```json
{
  "status": "success",
  "total_events": 10,
  "failures_indexed": 1,
  "passed": 4,
  "failed": 1
}
```

**Similar Failures Response:**
```json
[
  {
    "score": 0.85,
    "test_name": "testLoginButton",
    "class_name": "LoginTest",
    "message": "Element not found: signin-btn",
    "timestamp": "2024-01-15T10:30:00Z"
  }
]
```

---

## 🛠 Extending the Framework

### Adding New Page Objects

```java
// src/main/java/com/automation/pages/NewPage.java
public class NewPage extends BasePage {

    @FindBy(id = "element-id")
    private WebElement myElement;

    public NewPage(WebDriver driver) {
        super(driver);
    }

    public void clickElement() {
        click(myElement);
    }
}
```

### Adding New Tests

```java
// src/test/java/com/automation/tests/NewTest.java
public class NewTest extends BaseTest {

    @Test
    @Description("Test description for Allure")
    public void testNewFeature() {
        // Your test logic
    }
}
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 Generate Beautiful HTML Report

Generate a standalone HTML report with charts and failure details:

```bash
cd ai-analysis
source venv/bin/activate
python report_generator.py -o test_report.html
```

This generates a beautiful report with:
- 📊 Pass/fail metrics with charts
- 🔴 Detailed failure cards with stacktraces
- ✅ Passed test summary
- 🧠 AI analysis information

---

## 📋 Context YAML

The `context.yaml` file contains all the information needed to recreate this project. Use it as:

1. **Reference** - Understand the project structure and components
2. **AI Context** - Provide to AI assistants to understand the project
3. **Documentation** - Quick overview of all technologies and configurations

```yaml
# Key sections in context.yaml:
project:        # Project metadata
stack:          # Technology versions (Java, Python, libraries)
structure:      # File/folder organization
features:       # Detailed feature descriptions
commands:       # All CLI commands needed
test_site:      # Test application details
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Pramod Dutta**
- Website: [The Testing Academy](https://thetestingacademy.com)
- YouTube: [The Testing Academy](https://youtube.com/thetestingacademy)
- LinkedIn: [Pramod Dutta](https://linkedin.com/in/pramoddutta)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<p align="center">
  Made with ❤️ by <a href="https://thetestingacademy.com">The Testing Academy</a>
</p>

<img width="3600" height="2954" alt="image" src="https://github.com/user-attachments/assets/bec7ac92-225e-4592-a980-d07fc60878c5" />

