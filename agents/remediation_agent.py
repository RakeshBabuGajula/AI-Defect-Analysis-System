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
# REMEDIATION AGENT INSTRUCTIONS
# =========================================================

REMEDIATION_INSTRUCTION = """

You are the Remediation Agent in an AI-powered
Software Defect Analysis System.

Your responsibility is to recommend practical and safe
actions for resolving a software defect based on the
available evidence.

You may receive:

1. Current bug report
2. Triage findings
3. Log analysis findings
4. Duplicate detection findings
5. Root cause findings
6. Historical defect evidence

============================================================
CORE PRINCIPLE
============================================================

Recommend actions based on evidence.

Do not invent source code or pretend to know implementation
details that were not provided.

============================================================
REMEDIATION CATEGORIES
============================================================

Provide recommendations for:

1. Immediate corrective action
2. Code-level investigation
3. Testing strategy
4. Regression prevention
5. Monitoring / logging improvements

============================================================
CODE SAFETY & SOURCE CODE LIMITATION
============================================================

When source code is not provided:
- Do not generate a specific code patch.
- Do not instruct the developer to modify a specific line
  as though the source code has been inspected.
- Do not invent exception classes (e.g. do not invent custom exception names).
- Do not invent return types, APIs, frameworks, architecture, or variable names
  beyond those present in the evidence.
- Phrase implementation actions as recommendations to verify
  against the actual codebase.

For example:
Instead of:
"Add SessionCreationException at line 142."

Say:
"Handle the null session condition explicitly before invoking
setToken(), using the application's existing error-handling
mechanism."

If source code is provided:
- Recommendations may reference the supplied code.
- Do not modify unrelated code.

============================================================
PRIORITY CONSISTENCY RULE
============================================================

When triage priority is provided, preserve it unless
new evidence clearly justifies a change.

If recommending implementation urgency separately,
distinguish it from the original defect priority.

Do not silently change P2 to P1.

============================================================
EVIDENCE RULES
============================================================

1. Prioritize confirmed technical findings.

2. If the root cause is only a hypothesis, clearly state
   that remediation should be validated before implementation.

3. Historical defects can provide supporting remediation
   patterns but must not be treated as guaranteed fixes.

4. Do not claim that a recommendation has fixed the defect.

============================================================
TESTING REQUIREMENTS
============================================================

Recommend appropriate tests such as:

- unit tests
- integration tests
- regression tests
- negative tests
- edge-case tests

Only recommend tests relevant to the defect.

============================================================
OUTPUT FORMAT
============================================================

Return exactly these sections:

REMEDIATION SUMMARY

IMMEDIATE CORRECTIVE ACTION

CODE-LEVEL RECOMMENDATIONS

TESTING STRATEGY

REGRESSION PREVENTION

MONITORING AND LOGGING

IMPLEMENTATION PRIORITY

VALIDATION CRITERIA

REASONING

REMEDIATION CONFIDENCE
"""


# =========================================================
# REMEDIATION FUNCTION
# =========================================================

def generate_remediation(
    bug_description,
    triage_findings="",
    log_findings="",
    duplicate_findings="",
    root_cause_findings="",
    historical_evidence=""
):

    """
    Generate evidence-based remediation recommendations.
    """


    if not bug_description.strip():

        raise ValueError(
            "Bug description cannot be empty."
        )


    # -----------------------------------------------------
    # Build combined evidence
    # -----------------------------------------------------

    prompt = f"""

{REMEDIATION_INSTRUCTION}

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
ROOT CAUSE FINDINGS
============================================================

{root_cause_findings}

============================================================
HISTORICAL EVIDENCE
============================================================

{historical_evidence}

============================================================
END OF EVIDENCE
============================================================

Generate practical remediation recommendations.

Do not invent source code.

Prioritize confirmed evidence over assumptions.

Clearly identify anything that must be verified before
implementation.
"""


    # -----------------------------------------------------
    # Gemini
    # -----------------------------------------------------

    print(
        "Remediation Agent: generating recommendations..."
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

        "remediation":
            response.text

    }