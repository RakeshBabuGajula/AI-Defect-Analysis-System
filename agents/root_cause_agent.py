import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from llm.gemini_utils import generate_content_with_retry


# =========================================================
# PROJECT CONFIGURATION
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
        "GEMINI_API_KEY was not found."
    )


genai.configure(
    api_key=API_KEY
)

MODEL_NAME = "gemini-2.5-flash"


# =========================================================
# ROOT CAUSE AGENT INSTRUCTIONS
# =========================================================

ROOT_CAUSE_INSTRUCTION = """

You are the Root Cause Agent in an AI-powered
Software Defect Analysis System.

Your responsibility is to determine the most plausible
technical root cause of a software defect by correlating
multiple evidence sources.

You may receive:

1. Current bug report
2. Triage findings
3. Log analysis findings
4. Duplicate detection findings
5. Historical defects retrieved through RAG

============================================================
CORE PRINCIPLE
============================================================

Do not guess.

Root cause conclusions must be based on available evidence.

Distinguish clearly between:

- DIRECT EVIDENCE
- SUPPORTING HISTORICAL EVIDENCE
- TECHNICAL HYPOTHESES
- UNKNOWN INFORMATION

============================================================
EVIDENCE PRIORITY
============================================================

Use evidence in this order:

1. Direct stack traces and error logs
2. Explicit behavior in the current bug report
3. Repeated technical indicators
4. Historical defect evidence
5. General technical reasoning

Historical similarity alone must never establish a root cause.

============================================================
ROOT CAUSE CLASSIFICATION
============================================================

Use one of these:

CONFIRMED ROOT CAUSE
Only when direct technical evidence strongly establishes
the cause.

LIKELY ROOT CAUSE
When multiple pieces of evidence strongly support the cause,
but direct proof is incomplete.

POTENTIAL ROOT CAUSE
When the cause is technically plausible but evidence is limited.

INSUFFICIENT EVIDENCE
When the available information is not enough to determine
a meaningful root cause.

============================================================
REASONING RULES
============================================================

1. Correlate the evidence from all available agents.

2. Do not blindly accept conclusions from another agent.

3. Correct contradictions between evidence sources.

4. Explain why the selected cause is more plausible than
   alternative causes.

5. If logs directly identify the failure mechanism,
   prioritize them over semantic similarity.

6. Do not invent code behavior.

7. Do not invent missing logs or stack traces.

============================================================
OUTPUT FORMAT
============================================================

Return exactly these sections:

ROOT CAUSE SUMMARY

PRIMARY ROOT CAUSE

ROOT CAUSE STATUS

DIRECT EVIDENCE

SUPPORTING HISTORICAL EVIDENCE

ALTERNATIVE POSSIBLE CAUSES

EVIDENCE CORRELATION

RECOMMENDED VERIFICATION

CONFIDENCE

REASONING LIMITATIONS
"""


# =========================================================
# ROOT CAUSE ANALYSIS
# =========================================================

def analyze_root_cause(
    bug_description,
    triage_findings="",
    log_findings="",
    duplicate_findings="",
    historical_evidence=""
):

    """
    Correlate all available defect-analysis evidence and
    determine the most plausible root cause.
    """


    if not bug_description.strip():

        raise ValueError(
            "Bug description cannot be empty."
        )


    # -----------------------------------------------------
    # Build combined evidence
    # -----------------------------------------------------

    prompt = f"""

{ROOT_CAUSE_INSTRUCTION}

============================================================
CURRENT BUG REPORT
============================================================

{bug_description}

============================================================
TRIAGE FINDINGS
============================================================

{triage_findings}

============================================================
LOG ANALYSIS FINDINGS
============================================================

{log_findings}

============================================================
DUPLICATE DETECTION FINDINGS
============================================================

{duplicate_findings}

============================================================
HISTORICAL RAG EVIDENCE
============================================================

{historical_evidence}

============================================================
END OF EVIDENCE
============================================================

Now correlate the evidence and determine the most plausible
technical root cause.

Do not treat historical similarity as proof.

If direct technical evidence is available, prioritize it.

If evidence is insufficient, explicitly say so.
"""


    # -----------------------------------------------------
    # Gemini
    # -----------------------------------------------------

    print(
        "Root Cause Agent: correlating evidence..."
    )

    model = genai.GenerativeModel(MODEL_NAME)

    response = generate_content_with_retry(
        model,
        prompt
    )


    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {

        "bug_description":
            bug_description,

        "root_cause_analysis":
            response.text

    }