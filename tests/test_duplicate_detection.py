from agents.duplicate_detection_agent import detect_duplicate


# =========================================================
# TEST BUG
# =========================================================

bug = """
Users are unable to log into the application after entering
valid credentials. The login request reaches the server,
but the application terminates before the dashboard appears.

The issue occurs consistently during login.

No stack trace or error log is currently available.
"""


# =========================================================
# RUN DUPLICATE DETECTION
# =========================================================

result = detect_duplicate(

    bug,

    top_k=5

)


# =========================================================
# DISPLAY CANDIDATES
# =========================================================

print("\n")

print("=" * 75)

print("HISTORICAL DUPLICATE CANDIDATES")

print("=" * 75)


for candidate in result["candidates"]:

    print("\n" + "-" * 75)

    print(
        f"Rank: "
        f"{candidate['rank']}"
    )

    print(
        f"Bug ID: "
        f"{candidate['bug_id']}"
    )

    print(
        f"Source: "
        f"{candidate['source']}"
    )

    print(
        f"Title: "
        f"{candidate['title']}"
    )

    print(
        f"Product: "
        f"{candidate['product']}"
    )

    print(
        f"Component: "
        f"{candidate['component']}"
    )

    print(
        f"Similarity: "
        f"{candidate['similarity']}"
    )


# =========================================================
# DISPLAY ASSESSMENT
# =========================================================

print("\n")

print("=" * 75)

print("DUPLICATE DETECTION RESULT")

print("=" * 75)

print()

print(
    result["duplicate_assessment"]
)