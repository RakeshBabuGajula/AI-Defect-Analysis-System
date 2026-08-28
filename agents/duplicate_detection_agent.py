import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

from knowledge_base.rag.retriever import retrieve_similar_bugs
from knowledge_base.rag.context_builder import build_rag_context
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
# DUPLICATE DETECTION INSTRUCTIONS
# =========================================================

DUPLICATE_INSTRUCTION = """

You are the Duplicate Detection Agent in an
AI-powered Software Defect Analysis System.

Your responsibility is to determine whether a newly submitted
defect may represent an existing historical defect.

You will receive:

1. A current defect report.
2. Semantically retrieved historical defects.

============================================================
IMPORTANT PRINCIPLES
============================================================

Semantic similarity is NOT sufficient to declare a duplicate.

A defect should only be considered a strong duplicate candidate
when multiple characteristics align.

Compare:

- symptoms
- observed behavior
- error behavior
- product
- component
- affected functionality
- environment when available
- historical duplicate metadata
- resolution
- root/discussion relationships

============================================================
DUPLICATE CATEGORIES
============================================================

EXACT / LIKELY DUPLICATE:
Strong evidence that the current defect describes the same
underlying issue as an existing defect.

POSSIBLE DUPLICATE:
Significant overlap exists, but technical evidence is
insufficient to confirm the same underlying issue.

RELATED DEFECT:
The historical defect concerns a similar area or symptom,
but appears to represent a different issue.

NOT A DUPLICATE:
Available evidence indicates materially different behavior.

INSUFFICIENT EVIDENCE:
There is not enough information to make a meaningful
duplicate assessment.

============================================================
EVIDENCE RULES
============================================================

1. Never claim two defects are duplicates based only on
   their similarity score.

2. Do not invent technical details.

3. Historical metadata should be treated as supporting evidence.

4. If the current defect lacks stack traces, logs, version,
   or environment information, acknowledge that limitation.

5. Clearly identify both matching and conflicting evidence.

6. A high similarity score does not prove causation.

============================================================
OUTPUT FORMAT
============================================================

Return exactly these sections:

DUPLICATE ASSESSMENT

MOST LIKELY CANDIDATE

MATCHING EVIDENCE

CONFLICTING EVIDENCE

HISTORICAL METADATA

DUPLICATE STATUS

RECOMMENDATION

MISSING INFORMATION

CONFIDENCE
"""


# =========================================================
# DUPLICATE DETECTION FUNCTION
# =========================================================

def detect_duplicate(
    bug_description,
    top_k=5
):

    """
    Detect whether a newly submitted defect is potentially
    duplicated by a historical defect.
    """


    if not bug_description.strip():

        raise ValueError(
            "Bug description cannot be empty."
        )


    # -----------------------------------------------------
    # Retrieve candidates
    # -----------------------------------------------------

    print(
        "Duplicate Agent: retrieving candidate defects..."
    )

    candidates = retrieve_similar_bugs(

        bug_description,

        top_k=top_k

    )


    # -----------------------------------------------------
    # Build RAG evidence
    # -----------------------------------------------------

    print(
        "Duplicate Agent: building evidence context..."
    )

    rag_context = build_rag_context(

        bug_description,

        candidates

    )


    # -----------------------------------------------------
    # Create prompt
    # -----------------------------------------------------

    prompt = f"""

{DUPLICATE_INSTRUCTION}

============================================================
CURRENT DEFECT
============================================================

{bug_description}

============================================================
HISTORICAL CANDIDATES
============================================================

{rag_context}

============================================================
END EVIDENCE
============================================================

Compare the current defect against the historical candidates.

Identify the strongest candidate, if one exists.

Do not declare a duplicate unless the evidence supports
substantial overlap.

If the evidence is insufficient, explicitly say so.
"""


    # -----------------------------------------------------
    # Gemini analysis
    # -----------------------------------------------------

    print(
        "Duplicate Agent: analyzing candidates..."
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

        "candidates":
            candidates,

        "duplicate_assessment":
            response.text

    }