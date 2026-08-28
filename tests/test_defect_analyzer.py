from llm.defect_analyzer import analyze_bug


# =========================================================
# TEST BUG
# =========================================================

bug = """
The application crashes immediately after a user enters
valid credentials and clicks the Login button. The login
request reaches the server, but the application terminates
before the dashboard is displayed.
"""


# =========================================================
# RUN AI DEFECT ANALYSIS
# =========================================================

result = analyze_bug(
    bug,
    top_k=5
)


# =========================================================
# DISPLAY HISTORICAL EVIDENCE
# =========================================================

print("\n")
print("=" * 75)
print("RETRIEVED HISTORICAL DEFECTS")
print("=" * 75)


for historical_bug in result["retrieved_bugs"]:

    print("\n" + "-" * 75)

    print(
        f"Rank: "
        f"{historical_bug['rank']}"
    )

    print(
        f"Bug ID: "
        f"{historical_bug['bug_id']}"
    )

    print(
        f"Source: "
        f"{historical_bug['source']}"
    )

    print(
        f"Title: "
        f"{historical_bug['title']}"
    )

    print(
        f"Similarity: "
        f"{historical_bug['similarity']}"
    )


# =========================================================
# DISPLAY AI ANALYSIS
# =========================================================

print("\n")
print("=" * 75)
print("AI DEFECT ANALYSIS")
print("=" * 75)

print(
    result["analysis"]
)