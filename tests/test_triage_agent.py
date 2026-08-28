from agents.triage_agent import triage_bug


# =========================================================
# TEST BUG
# =========================================================

bug = """
The application crashes immediately after a user enters
valid credentials and clicks the Login button.

The login request reaches the server, but the application
terminates before the dashboard is displayed.

The issue occurs consistently during login.
No stack trace or error log is currently available.
"""


# =========================================================
# RUN TRIAGE
# =========================================================

result = triage_bug(

    bug,

    top_k=5

)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\n")

print("=" * 75)

print("TRIAGE AGENT RESULT")

print("=" * 75)

print()

print(
    result["triage"]
)


# =========================================================
# DISPLAY HISTORICAL EVIDENCE
# =========================================================

print("\n")

print("=" * 75)

print("HISTORICAL DEFECTS USED BY TRIAGE AGENT")

print("=" * 75)


for bug in result["historical_bugs"]:

    print("\n" + "-" * 75)

    print(
        f"Rank: {bug['rank']}"
    )

    print(
        f"Bug ID: {bug['bug_id']}"
    )

    print(
        f"Source: {bug['source']}"
    )

    print(
        f"Title: {bug['title']}"
    )

    print(
        f"Similarity: {bug['similarity']}"
    )