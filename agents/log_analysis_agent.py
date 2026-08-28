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
# LOG ANALYSIS INSTRUCTIONS
# =========================================================

LOG_ANALYSIS_INSTRUCTION = """

You are the Log Analysis Agent in an AI-powered
Software Defect Analysis System.

Your responsibility is to analyze technical evidence
contained in:

- application logs
- server logs
- client logs
- error messages
- exception messages
- stack traces
- crash reports

Your job is to extract and explain what the technical
evidence actually shows.

============================================================
IMPORTANT EVIDENCE RULES
============================================================

1. Never invent log entries or stack-trace information.

2. Never invent file names, class names, methods, or line numbers.

3. Only identify an exception when it appears in the supplied
   technical evidence.

4. Separate directly observed technical evidence from hypotheses.

5. Do not claim a root cause unless the supplied evidence
   directly supports it.

6. If no logs or stack trace are provided, explicitly state:

   "No technical log or stack-trace evidence was provided."

7. Do not treat a natural-language bug description as a
   technical stack trace.

============================================================
ANALYSIS TASKS
============================================================

Identify, when available:

- Exception type
- Error message
- Error code
- Stack trace
- Failure location
- File name
- Class name
- Method name
- Line number
- Call sequence
- Relevant timestamps
- Request/session identifiers
- Repeated errors
- Warning indicators
- Possible technical patterns

============================================================
HYPOTHESIS RULES
============================================================

If the evidence suggests a possible cause, label it:

"Potential Technical Hypothesis"

Do not present a hypothesis as a confirmed root cause.

============================================================
EVIDENCE QUALITY
============================================================

HIGH:
Detailed stack trace or strong technical evidence exists.

MEDIUM:
Useful technical errors exist but important details are missing.

LOW:
Only generic error messages or natural-language descriptions
are available.

NONE:
No technical log or stack-trace evidence is provided.

============================================================
OUTPUT FORMAT
============================================================

Return exactly these sections:

LOG ANALYSIS SUMMARY

EXCEPTION / ERROR TYPE

ERROR MESSAGE

STACK TRACE FINDINGS

FAILURE LOCATION

CALL SEQUENCE

TECHNICAL INDICATORS

POTENTIAL TECHNICAL HYPOTHESES

EVIDENCE QUALITY

MISSING TECHNICAL INFORMATION

RECOMMENDED NEXT INVESTIGATION

CONFIDENCE
"""


# =========================================================
# LOG ANALYSIS FUNCTION
# =========================================================

def analyze_logs(
    bug_description,
    technical_logs=""
):

    """
    Analyze a software defect together with technical logs
    or stack traces.
    """


    if not bug_description.strip():

        raise ValueError(
            "Bug description cannot be empty."
        )


    # -----------------------------------------------------
    # Prepare technical evidence
    # -----------------------------------------------------

    if technical_logs.strip():

        log_evidence = technical_logs

    else:

        log_evidence = (
            "No technical log or stack-trace evidence "
            "was provided."
        )


    # -----------------------------------------------------
    # Build prompt
    # -----------------------------------------------------

    prompt = f"""

{LOG_ANALYSIS_INSTRUCTION}

============================================================
CURRENT BUG DESCRIPTION
============================================================

{bug_description}

============================================================
TECHNICAL LOG / STACK TRACE
============================================================

{log_evidence}

============================================================
END TECHNICAL EVIDENCE
============================================================

Analyze only the evidence provided above.

Do not invent technical details.

If technical evidence is missing, explicitly identify
what must be collected next.
"""


    # -----------------------------------------------------
    # Gemini
    # -----------------------------------------------------

    print(
        "Log Analysis Agent: analyzing technical evidence..."
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

        "technical_logs":
            technical_logs,

        "log_analysis":
            response.text

    }