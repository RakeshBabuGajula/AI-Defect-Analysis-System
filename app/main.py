import streamlit as st
import json
import uuid
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Defect Analysis System",
    page_icon="🐞",
    layout="wide"
)


# ---------------------------------------------------------
# STORAGE CONFIGURATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
SUBMISSION_DIR = BASE_DIR / "data" / "submissions"

SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🐞 AI-Powered Software Defect Analysis System")

st.markdown(
    """
    ### Intelligent Bug Submission & Analysis Platform

    Submit software defects, stack traces, and error logs for
    intelligent analysis using semantic search, RAG, and AI agents.
    """
)

st.divider()


# ---------------------------------------------------------
# BUG SUBMISSION FORM
# ---------------------------------------------------------

st.subheader("📋 Submit a Software Defect")

st.info(
    "Provide as much information as possible. "
    "Detailed bug reports help the system perform better analysis."
)

with st.form("bug_submission_form"):

    bug_title = st.text_input(
        "Bug Title *",
        placeholder="Example: Application crashes during login"
    )

    bug_description = st.text_area(
        "Bug Description *",
        placeholder=(
            "Describe what happened, what you expected to happen, "
            "and the steps that caused the problem."
        ),
        height=150
    )

    col1, col2 = st.columns(2)

    with col1:

        severity = st.selectbox(
            "Severity",
            [
                "Critical",
                "High",
                "Medium",
                "Low"
            ]
        )

    with col2:

        component = st.text_input(
            "Affected Component",
            placeholder="Example: Authentication Service"
        )

    stack_trace = st.text_area(
        "Stack Trace",
        placeholder="Paste the stack trace here...",
        height=180
    )

    error_logs = st.text_area(
        "Error Logs",
        placeholder="Paste relevant error logs here...",
        height=180
    )

    st.markdown("### 📎 Upload Bug Report / Log")

    uploaded_file = st.file_uploader(
        "Upload a bug report or log file",
        type=["txt", "log", "json", "csv"],
        help="Supported formats: TXT, LOG, JSON and CSV"
    )

    submitted = st.form_submit_button(
        "🔍 Submit Bug",
        use_container_width=True
    )


# ---------------------------------------------------------
# SUBMISSION PROCESSING
# ---------------------------------------------------------

if submitted:

    # Validate required fields

    if not bug_title.strip():
        st.error("Please enter a bug title.")

    elif not bug_description.strip():
        st.error("Please enter a bug description.")

    else:

        # Generate unique submission ID

        submission_id = f"BUG-{uuid.uuid4().hex[:8].upper()}"

        # Read uploaded file if available

        uploaded_content = ""

        if uploaded_file is not None:

            try:

                uploaded_content = uploaded_file.getvalue().decode(
                    "utf-8",
                    errors="ignore"
                )

            except Exception:

                uploaded_content = "Unable to decode uploaded file."

        # Create structured bug report

        bug_report = {

            "submission_id": submission_id,

            "submitted_at": datetime.now().isoformat(),

            "bug_title": bug_title.strip(),

            "bug_description": bug_description.strip(),

            "severity": severity,

            "affected_component": component.strip(),

            "stack_trace": stack_trace.strip(),

            "error_logs": error_logs.strip(),

            "uploaded_file": (
                uploaded_file.name
                if uploaded_file is not None
                else None
            ),

            "uploaded_content": uploaded_content

        }

        # Save JSON file

        output_file = SUBMISSION_DIR / f"{submission_id}.json"

        with open(output_file, "w", encoding="utf-8") as file:

            json.dump(
                bug_report,
                file,
                indent=4,
                ensure_ascii=False
            )

        # Success message

        st.success(
            f"Bug submitted successfully! Submission ID: {submission_id}"
        )

        st.markdown("### 📊 Submission Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Submission ID",
                submission_id
            )

        with col2:
            st.metric(
                "Severity",
                severity
            )

        with col3:
            st.metric(
                "Status",
                "Received"
            )

        st.markdown("### 🔄 What happens next?")

        st.write(
            """
            Your bug report has been securely stored and is ready for
            the next stages of the defect analysis pipeline:

            **Bug Processing → Semantic Retrieval → RAG → AI Agents → Diagnosis**
            """
        )