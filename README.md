# ⚡ AI Defect Analysis System
### RAG-Powered Multi-Agent Architecture for Autonomous Software Defect Triage, Duplicate Detection, Root Cause Diagnosis & Remediation

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6F61?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Embeddings](https://img.shields.io/badge/Sentence--Transformers-all--MiniLM--L6--v2-green?style=for-the-badge)

---

## 📌 Executive Overview

Modern software development teams receive hundreds of bug reports, stack traces, and crash logs daily across repositories and issue trackers. Manual triage, duplicate identification, root cause investigation, and remediation planning are slow, expensive, and heavily reliant on tribal knowledge.

The **AI Defect Analysis System** is an enterprise-grade, autonomous software defect analysis platform powered by **Retrieval-Augmented Generation (RAG)** and a **5-Agent Sequential LLM Orchestrator**. 

By indexing **4,125 real-world historical defect vectors** across major open-source ecosystems (**Apache Bugzilla, Eclipse Issue Tracker, Mozilla Bugzilla**), the system correlates live bug reports with historical evidence and technical stack traces to produce an executive-ready defect diagnosis in seconds.

---

## 🌟 Key Architecture & Capabilities

### 📚 1. Balanced RAG Knowledge Base
- **Vector Collection**: `historical_defects_balanced` stored in persistent **ChromaDB**.
- **Dataset Corpora**: 2,000 Apache chunks, 2,000 Eclipse chunks, 125 Mozilla chunks (**4,125 total vectors**).
- **Dense Vector Space**: **384-Dimensional** embeddings generated via `sentence-transformers/all-MiniLM-L6-v2`.
- **Distance Metric**: Normalized **Cosine Similarity**.
- **Chunking Strategy**: 2,000-character sliding windows with 300-character overlap preserving context integrity.

### 🤖 2. Autonomous 5-Agent Pipeline
1. **🏷️ Triage Agent**: Categorizes defect type (*Application Crash, UI Freeze, Data Corruption*), evaluates severity (*CRITICAL, HIGH, MEDIUM, LOW*), assigns priority (*P1, P2, P3*), assesses reproducibility, and outlines business impact.
2. **🔎 Duplicate Detection Agent**: Queries ChromaDB vector space for top-k candidates, cross-references multi-attribute metadata (*Title, Product, Component, Status, Resolution*), and determines duplicate status (*DUPLICATE, RELATED DEFECT, NEW ISSUE*), avoiding false-positive matches.
3. **🧾 Log Analysis Agent**: Parses raw unformatted stack traces, exceptions, class paths, and line numbers (*e.g., `java.lang.NullPointerException` at `AuthenticationService.java:142`*). Strictly separates observed evidence from hypotheses with zero hallucination.
4. **🎯 Root Cause Agent**: Correlates evidence from Triage, Log Analysis, Duplicate Candidates, and RAG retrieval using an evidence priority hierarchy (*Log Traces > Bug Description > RAG Similarity*) to output a confirmed or likely technical root cause.
5. **🛠️ Remediation Agent**: Formulates defensive code safeguards (*obeying strict Source Code Limitation rules without inventing synthetic exception classes*), multi-level testing strategies (*unit, integration, regression*), CI/CD static analysis guardrails, and logging/monitoring rules.

### 💻 3. Enterprise Streamlit Web Dashboard
- **Glassmorphism UI**: Styled with modern Google Fonts (`Outfit` + `Inter`), ambient glow headers, and KPI metric cards.
- **1-Click Presets**: Pre-loaded demonstration presets (*NullPointerException, UI Freeze, Connection Pool Timeout*) for 1-click recruiter/reviewer evaluation.
- **Visual Architecture Flowchart**: Embedded pipeline execution flowchart.
- **Dedicated RAG Explorer**: `🔬 RAG Evidence` tab displaying candidate metadata tables and raw vector text snippets.
- **Executive Summary Banner**: `🎯 DEFECT ANALYSIS EXECUTIVE SUMMARY` top card with color-coded status pill badges.
- **Report Exporter**: 1-click JSON report exporter for CI/CD or ticket system integration.

---

## 📐 Multi-Agent System Architecture

```text
                               ┌─────────────────────────────┐
                               │   User Defect Submission    │
                               │  (Bug Text + Error Logs)    │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │  RAG Knowledge Retrieval    │
                               │  (ChromaDB: 4,125 Vectors)  │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │     1. TRIAGE AGENT         │
                               │ Category, Severity, Scope   │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │ 2. DUPLICATE DETECTION AGENT│
                               │ Cosine Match & Metadata     │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │   3. LOG ANALYSIS AGENT     │
                               │ Stack Trace & Exception Line│
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │    4. ROOT CAUSE AGENT      │
                               │  Multi-Evidence Correlation │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │    5. REMEDIATION AGENT     │
                               │ Action Plan & Test Strategy │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │  Executive Report Dashboard │
                               │  (Streamlit / JSON Export)  │
                               └─────────────────────────────┘
```
## 📸 Application Screenshots
<img width="1918" height="1144" alt="image" src="https://github.com/user-attachments/assets/9e9148f1-7f1f-4978-90dd-5d519e54b4b5" />
<img width="1917" height="1144" alt="image" src="https://github.com/user-attachments/assets/30b8fb76-cbf2-4923-b798-f2d66c3e53f4" />
<img width="1917" height="1140" alt="image" src="https://github.com/user-attachments/assets/d3c3ac03-efe0-462a-96b3-74ad35bb8555" />
<img width="1918" height="1135" alt="image" src="https://github.com/user-attachments/assets/6505a6bd-49cf-4c68-a907-568849e62711" />


---

## 📁 Repository Folder Structure

```text
AI-Defect-Analysis-System/
├── .env                                         # Environment configuration (GEMINI_API_KEY)
├── requirements.txt                             # Python dependencies
├── sample_bug.log                               # Sample stack trace log file
│
├── agents/                                      # Specialized Multi-Agent System Modules
│   ├── __init__.py
│   ├── agent_orchestrator.py                    # 5-Agent Sequential Orchestrator Engine
│   ├── triage_agent.py                          # Triage & Severity Classification Agent
│   ├── duplicate_detection_agent.py             # Duplicate Candidate & Similarity Agent
│   ├── log_analysis_agent.py                    # Log Parser & Stack Trace Analysis Agent
│   ├── root_cause_agent.py                      # Multi-Source Root Cause Correlation Agent
│   └── remediation_agent.py                     # Remediation & Action Plan Agent
│
├── app/                                         # Streamlit Enterprise Web Dashboard
│   ├── __init__.py
│   ├── main.py                                  # CLI / Entry point module
│   └── streamlit_app.py                         # Full Streamlit Web UI Implementation
│
├── llm/                                         # Gemini LLM Integration Layer
│   ├── __init__.py
│   ├── gemini_utils.py                          # Rate-Limit (429) Retry & Backoff Helper
│   ├── defect_analyzer.py                      # Standalone LLM Analyzer
│   └── test_gemini.py                           # Gemini API Connection Verification
│
├── knowledge_base/                              # RAG Pipeline & Vector DB Generation
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── retriever.py                         # ChromaDB Vector Retriever Module
│   │   └── context_builder.py                   # RAG Context Formatter
│   ├── build_balanced_vector_database.py        # Balanced Vector DB Builder Script
│   ├── create_balanced_dataset.py               # Dataset Sampler (Apache, Eclipse, Mozilla)
│   ├── create_balanced_chunks.py                # 2000-char Sliding Window Chunking Script
│   ├── generate_balanced_embeddings.py          # SentenceTransformer Vector Embedder
│   └── balanced_semantic_search.py              # Vector DB Query Test Script
│
├── data/                                        # Datasets & Vector Storage
│   ├── historical/                              # Standardized Raw Defect Datasets
│   ├── processed/
│   │   ├── chunks/                              # JSONL Chunks (balanced_bug_chunks.jsonl)
│   │   └── embeddings/                          # JSONL Embeddings (balanced_bug_embeddings.jsonl)
│   └── vector_db/                               # ChromaDB Store (historical_defects_balanced)
│
└── tests/                                       # Comprehensive Test Suite
    ├── test_agent_orchestrator.py               # 5-Agent End-to-End Orchestration Test
    ├── test_triage_agent.py                     # Triage Agent Test
    ├── test_duplicate_detection.py              # Duplicate Detection Agent Test
    ├── test_log_analysis_no_logs.py             # Log Analysis (No-Logs Scenario Test)
    ├── test_log_analysis_stacktrace.py          # Log Analysis (Stack-Trace Test)
    ├── test_root_cause_agent.py                 # Root Cause Agent Test
    └── test_remediation_agent.py                # Remediation Agent Test
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.13)
- **Google Gemini API Key** (Free Tier or Pay-as-you-go key from [Google AI Studio](https://aistudio.google.com/))

### 2. Environment Setup & Installation
Clone the repository and set up a Python virtual environment:

```bash
# Clone repository
git clone https://github.com/yourusername/AI-Defect-Analysis-System.git
cd AI-Defect-Analysis-System

# Create virtual environment
python -m venv venv

# Activate environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# Activate environment (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. API Key Configuration
Create a `.env` file in the root directory and add your Gemini API Key:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

### 4. Build Vector Knowledge Base (Optional / Pre-Built)
If rebuilding the ChromaDB vector database from raw datasets:

```bash
# Set PYTHONPATH and execute vector database build
$env:PYTHONPATH=".;knowledge_base"
python knowledge_base/build_balanced_vector_database.py
```

### 5. Launch Streamlit Web Application
Run the Streamlit web dashboard locally:

```bash
python -m streamlit run app/streamlit_app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Verification & Testing

Run the automated test suite to verify agent functionality:

```bash
# Set PYTHONPATH for local module resolution
$env:PYTHONPATH=".;knowledge_base"

# Run complete 5-Agent Orchestrator Test
python tests/test_agent_orchestrator.py

# Run individual agent tests
python tests/test_triage_agent.py
python tests/test_duplicate_detection.py
python tests/test_log_analysis_stacktrace.py
python tests/test_root_cause_agent.py
python tests/test_remediation_agent.py
```

---

## 🛠️ Technology Stack

| Component | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core Backend Logic & Agent Framework |
| **LLM Core** | Google Gemini 2.5 Flash | Autonomous Agent Reasoning Engine |
| **Vector DB** | ChromaDB (Persistent) | Vector Store for Defect Embeddings |
| **Embedding Model** | `all-MiniLM-L6-v2` | 384D Dense Vector Space Embeddings |
| **Web UI** | Streamlit | Executive Glassmorphic Web Dashboard |
| **Data Processing** | Pandas, NumPy | Dataset Formatting & Metric Aggregation |
| **Environment** | Python-Dotenv | Secure Secret Management |

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
