import time
from pathlib import Path
import sys


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# =========================================================
# IMPORT AGENTS
# =========================================================

from agents.triage_agent import triage_bug
from agents.duplicate_detection_agent import detect_duplicate
from agents.log_analysis_agent import analyze_logs
from agents.root_cause_agent import analyze_root_cause
from agents.remediation_agent import generate_remediation


# =========================================================
# ORCHESTRATOR
# =========================================================

class AgentOrchestrator:

    def __init__(self):

        print("=" * 75)
        print("AI DEFECT ANALYSIS SYSTEM")
        print("AGENT ORCHESTRATOR INITIALIZED")
        print("=" * 75)


    # =====================================================
    # RUN COMPLETE PIPELINE
    # =====================================================

    def analyze(
        self,
        bug_description,
        technical_logs=""
    ):

        if not bug_description.strip():

            raise ValueError(
                "Bug description cannot be empty."
            )


        # -------------------------------------------------
        # STEP 1: TRIAGE
        # -------------------------------------------------

        print("\n")
        print("=" * 75)
        print("STEP 1 / 5 : TRIAGE AGENT")
        print("=" * 75)

        triage_result = triage_bug(
            bug_description
        )

        triage_findings = triage_result[
            "triage"
        ]

        print("Triage analysis completed.")
        time.sleep(1.5)


        # -------------------------------------------------
        # STEP 2: DUPLICATE DETECTION
        # -------------------------------------------------

        print("\n")
        print("=" * 75)
        print("STEP 2 / 5 : DUPLICATE DETECTION AGENT")
        print("=" * 75)

        duplicate_result = detect_duplicate(

            bug_description,

            top_k=5

        )

        duplicate_findings = duplicate_result[
            "duplicate_assessment"
        ]

        print("Duplicate detection completed.")
        time.sleep(1.5)


        # -------------------------------------------------
        # STEP 3: LOG ANALYSIS
        # -------------------------------------------------

        print("\n")
        print("=" * 75)
        print("STEP 3 / 5 : LOG ANALYSIS AGENT")
        print("=" * 75)

        log_result = analyze_logs(

            bug_description,

            technical_logs

        )

        log_findings = log_result[
            "log_analysis"
        ]

        print("Log analysis completed.")
        time.sleep(1.5)


        # -------------------------------------------------
        # STEP 4: ROOT CAUSE
        # -------------------------------------------------

        print("\n")
        print("=" * 75)
        print("STEP 4 / 5 : ROOT CAUSE AGENT")
        print("=" * 75)

        root_cause_result = analyze_root_cause(

            bug_description,

            triage_findings=triage_findings,

            log_findings=log_findings,

            duplicate_findings=duplicate_findings

        )

        root_cause_findings = root_cause_result[
            "root_cause_analysis"
        ]

        print("Root cause analysis completed.")
        time.sleep(1.5)


        # -------------------------------------------------
        # STEP 5: REMEDIATION
        # -------------------------------------------------

        print("\n")
        print("=" * 75)
        print("STEP 5 / 5 : REMEDIATION AGENT")
        print("=" * 75)

        remediation_result = generate_remediation(

            bug_description,

            triage_findings=triage_findings,

            log_findings=log_findings,

            duplicate_findings=duplicate_findings,

            root_cause_findings=root_cause_findings

        )

        remediation_findings = remediation_result[
            "remediation"
        ]

        print("Remediation analysis completed.")


        # -------------------------------------------------
        # FINAL RESULT
        # -------------------------------------------------

        final_result = {

            "bug_description":
                bug_description,

            "technical_logs":
                technical_logs,

            "triage":
                triage_findings,

            "duplicate_detection":
                duplicate_findings,

            "rag_candidates":
                duplicate_result.get("candidates", []),

            "log_analysis":
                log_findings,

            "root_cause":
                root_cause_findings,

            "remediation":
                remediation_findings

        }


        return final_result


# =========================================================
# SIMPLE FUNCTION INTERFACE
# =========================================================

def run_defect_analysis(
    bug_description,
    technical_logs=""
):

    orchestrator = AgentOrchestrator()

    return orchestrator.analyze(

        bug_description,

        technical_logs

    )