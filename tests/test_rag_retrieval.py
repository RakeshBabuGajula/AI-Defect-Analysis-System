from knowledge_base.rag.retriever import retrieve_similar_bugs

from knowledge_base.rag.context_builder import build_rag_context


# =========================================================
# TEST BUG
# =========================================================

bug_description = """
The application crashes when a user enters valid credentials
and attempts to log into the system.
"""


# =========================================================
# RETRIEVE HISTORICAL BUGS
# =========================================================

results = retrieve_similar_bugs(

    bug_description,

    top_k=5

)


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n========================================")

print("RAG RETRIEVAL TEST")

print("========================================")


for bug in results:

    print(
        f"\nRank: {bug['rank']}"
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


# =========================================================
# BUILD CONTEXT
# =========================================================

context = build_rag_context(

    bug_description,

    results

)


# =========================================================
# DISPLAY CONTEXT
# =========================================================

print("\n\n========================================")

print("GENERATED RAG CONTEXT")

print("========================================\n")

print(context)