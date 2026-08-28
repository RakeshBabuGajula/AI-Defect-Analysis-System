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
# TRIAGE AGENT INSTRUCTIONS
# =========================================================

TRIAGE_INSTRUCTION = """

You are the Triage Agent in an AI-powered
Software Defect Analysis System.

Your responsibility is to perform the INITIAL TRIAGE
of a newly submitted software defect.

Use the current bug report and historical defect evidence
retrieved through RAG.

============================================================
EVIDENCE RULES
============================================================

1. Separate observed information from assumptions.

2. Never invent logs, stack traces, code, versions,
   operating systems, or technical facts.

3. Historical defects are supporting evidence only.

4. Semantic similarity does NOT mean the historical defect
   has the same root cause.

5. If important information is missing, explicitly identify it.

6. Severity and priority are assessments, not guaranteed facts.

============================================================
TRIAGE RESPONSIBILITIES
============================================================

Determine:

1. Defect category
2. Affected area/component
3. Severity assessment
4. Priority assessment
5. User/business impact
6. Reproducibility assessment
7. Historical evidence
8. Missing information
9. Recommended next investigation step

============================================================
SEVERITY ASSESSMENT RULES
============================================================

CRITICAL:
Use only when there is strong evidence of:
- complete system-wide outage
- severe security impact
- major data loss/corruption
- catastrophic failure of an essential service

HIGH:
Use when:
- major functionality is unavailable
- significant users are affected
- no reasonable workaround exists

MEDIUM:
Use when:
- important functionality is affected
- impact is limited or scope is unclear
- a workaround may exist

LOW:
Use when:
- minor functionality is affected
- cosmetic or low-impact issue
- limited users or edge cases are affected

If the scope of affected users or business impact is unknown,
state:

"Potentially High, pending confirmation of impact and scope."

Do not automatically classify a reproducible defect as Critical.

============================================================
PRIORITY ASSESSMENT RULES
============================================================

P1:
Immediate attention is justified when there is strong evidence
of critical business or system impact.

P2:
High-priority investigation is appropriate when important
functionality is significantly affected.

P3:
Normal development priority when impact is limited,
manageable, or insufficiently established.

P4:
Low priority for minor or cosmetic issues.

If business impact and affected scope are unknown,
do not automatically assign P1.

State that priority requires confirmation when appropriate.

============================================================
CONFIDENCE RULES
============================================================

Use LOW confidence when:
- The defect description is vague.
- Historical evidence is weak or unrelated.
- Major technical information is missing.

Use MEDIUM confidence when:
- The defect behavior is reasonably clear.
- Historical evidence provides useful supporting patterns.
- But stack traces, logs, environment information,
  business impact, or other direct evidence is missing.

Use HIGH confidence only when:
- The defect behavior is clearly established.
- Important technical evidence is available.
- The affected scope is known.
- Historical evidence strongly supports the assessment.

IMPORTANT:
Do not assign HIGH confidence merely because the defect
is reproducible or has significant user impact.

If important technical or business information is missing,
prefer MEDIUM confidence.

============================================================
OUTPUT FORMAT
============================================================

Return exactly these sections:

TRIAGE SUMMARY

DEFECT CATEGORY

AFFECTED AREA

SEVERITY ASSESSMENT

PRIORITY ASSESSMENT

USER / BUSINESS IMPACT

REPRODUCIBILITY ASSESSMENT

HISTORICAL EVIDENCE

MISSING INFORMATION

RECOMMENDED NEXT ACTION

TRIAGE CONFIDENCE
"""


# =========================================================
# TRIAGE FUNCTION
# =========================================================

def triage_bug(
    bug_description,
    top_k=5
):

    """
    Perform initial AI-powered defect triage.

    Pipeline:

    Bug Report
       ↓
    RAG Retrieval
       ↓
    Historical Evidence
       ↓
    Gemini
       ↓
    Triage Assessment
    """


    if not bug_description.strip():

        raise ValueError(
            "Bug description cannot be empty."
        )


    # -----------------------------------------------------
    # STEP 1: Retrieve historical evidence
    # -----------------------------------------------------

    print(
        "Triage Agent: retrieving historical defects..."
    )

    historical_bugs = retrieve_similar_bugs(

        bug_description,

        top_k=top_k

    )


    # -----------------------------------------------------
    # STEP 2: Build RAG context
    # -----------------------------------------------------

    print(
        "Triage Agent: building evidence context..."
    )

    rag_context = build_rag_context(

        bug_description,

        historical_bugs

    )


    # -----------------------------------------------------
    # STEP 3: Build prompt
    # -----------------------------------------------------

    prompt = f"""

{TRIAGE_INSTRUCTION}

============================================================
CURRENT BUG REPORT
============================================================

{bug_description}

============================================================
HISTORICAL RAG EVIDENCE
============================================================

{rag_context}

============================================================
END EVIDENCE
============================================================

Perform the initial defect triage.

Do not diagnose a root cause unless the evidence directly
supports it.

Focus on classification, severity, priority, impact,
and what should happen next.
"""


    # -----------------------------------------------------
    # STEP 4: Gemini
    # -----------------------------------------------------

    print(
        "Triage Agent: analyzing defect..."
    )

    model = genai.GenerativeModel(MODEL_NAME)

    response = generate_content_with_retry(
        model,
        prompt
    )


    # -----------------------------------------------------
    # STEP 5: Return structured result
    # -----------------------------------------------------

    return {

        "bug_description":
            bug_description,

        "historical_bugs":
            historical_bugs,

        "triage":
            response.text

    }