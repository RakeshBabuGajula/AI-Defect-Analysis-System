import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

from knowledge_base.rag.retriever import retrieve_similar_bugs
from knowledge_base.rag.context_builder import build_rag_context


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not API_KEY:

    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Check the .env file."
    )


genai.configure(
    api_key=API_KEY
)


MODEL_NAME = "gemini-2.5-flash"


# =========================================================
# SYSTEM INSTRUCTIONS
# =========================================================

SYSTEM_INSTRUCTION = """
You are an expert Software Defect Analysis Assistant
working as part of an enterprise AI defect management system.

Your task is to analyze a newly submitted software defect
using evidence retrieved from a historical defect knowledge base.

The historical defects are supporting evidence only.
They are NOT proof that the current defect has the same
root cause.

============================================================
STRICT EVIDENCE RULES
============================================================

1. Separate information into:
   - OBSERVED FACTS
   - HISTORICAL EVIDENCE
   - HYPOTHESES
   - UNKNOWN / MISSING INFORMATION

2. Never invent:
   - stack traces
   - logs
   - source code
   - HTTP responses
   - authentication results
   - application versions
   - operating systems
   - root causes
   - resolutions

3. If information is not provided, explicitly state:
   "Not provided in the current defect report."

4. Do not assume that a request reaching the server means
   authentication succeeded.

5. Do not treat semantic similarity as proof of causation.

6. Historical defects may be from completely different
   products or projects. Explain their relevance carefully.

============================================================
ROOT CAUSE RULES
============================================================

Root causes must be presented as hypotheses unless the
current report contains direct evidence proving the cause.

Use phrases such as:

- "Potential cause"
- "Possible explanation"
- "This should be investigated"
- "The available evidence suggests"

Do NOT state an unverified hypothesis as a confirmed fact.

============================================================
SEVERITY RULES
============================================================

Severity must be treated as an assessment, not an absolute fact.

Consider:

- user impact
- system availability
- reproducibility
- affected functionality
- business impact
- scope of affected users

If important information is missing, say that final severity
requires confirmation.

============================================================
CONFIDENCE RULES
============================================================

Use:

HIGH:
Only when the available evidence strongly supports the
conclusion.

MEDIUM:
When historical evidence and the defect description support
a reasonable hypothesis but direct technical evidence is
missing.

LOW:
When the available evidence is weak, ambiguous, or unrelated.

============================================================
OUTPUT FORMAT
============================================================

Return exactly these sections:

BUG SUMMARY

OBSERVED FACTS

LIKELY CATEGORY

SEVERITY ASSESSMENT

HISTORICAL EVIDENCE

EVIDENCE INTERPRETATION

LIKELY ROOT CAUSE

REASONING

RECOMMENDED INVESTIGATION

RECOMMENDED REMEDIATION

MISSING INFORMATION

CONFIDENCE
"""


# =========================================================
# ANALYZE BUG
# =========================================================

def analyze_bug(
    bug_description,
    top_k=5
):

    """
    Perform RAG-based AI defect analysis.

    Pipeline:

    Bug
      ↓
    Embedding
      ↓
    ChromaDB
      ↓
    Historical Evidence
      ↓
    RAG Context
      ↓
    Gemini
      ↓
    AI Defect Analysis
    """


    if not bug_description.strip():

        raise ValueError(
            "Bug description cannot be empty."
        )


    # -----------------------------------------------------
    # STEP 1: Retrieve historical defects
    # -----------------------------------------------------

    print(
        "Retrieving historical defects..."
    )

    retrieved_bugs = retrieve_similar_bugs(
        bug_description,
        top_k=top_k
    )


    # -----------------------------------------------------
    # STEP 2: Build RAG context
    # -----------------------------------------------------

    print(
        "Building RAG context..."
    )

    rag_context = build_rag_context(
        bug_description,
        retrieved_bugs
    )


    # -----------------------------------------------------
    # STEP 3: Create LLM prompt
    # -----------------------------------------------------

    prompt = f"""
{SYSTEM_INSTRUCTION}

Below is the current defect report and the historical
evidence retrieved from the defect knowledge base.

Analyze the current defect using this evidence.

Do not blindly copy historical conclusions.

==============================
RAG CONTEXT
==============================

{rag_context}

==============================
END RAG CONTEXT
==============================

Now produce the structured defect analysis.
"""


    # -----------------------------------------------------
    # STEP 4: Call Gemini
    # -----------------------------------------------------

    print(
        "Sending evidence to Gemini..."
    )

    model = genai.GenerativeModel(MODEL_NAME)

    response = model.generate_content(
        prompt
    )


    # -----------------------------------------------------
    # STEP 5: Return result
    # -----------------------------------------------------

    return {

        "bug_description":
            bug_description,

        "retrieved_bugs":
            retrieved_bugs,

        "analysis":
            response.text

    }