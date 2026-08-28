def build_rag_context(
    bug_description,
    retrieved_bugs
):

    """
    Build structured context for the LLM
    from historically similar defects.
    """


    context_parts = []


    # =====================================================
    # NEW BUG
    # =====================================================

    context_parts.append(
        "CURRENT BUG REPORT\n"
        "==================\n"
        f"{bug_description}\n"
    )


    # =====================================================
    # HISTORICAL EVIDENCE
    # =====================================================

    context_parts.append(
        "\nHISTORICAL DEFECT EVIDENCE\n"
        "===========================\n"
    )


    if not retrieved_bugs:

        context_parts.append(
            "No relevant historical defects were found."
        )

        return "\n".join(
            context_parts
        )


    for bug in retrieved_bugs:

        context_parts.append(

            f"\nHistorical Defect #{bug['rank']}\n"
            f"Bug ID: {bug['bug_id']}\n"
            f"Source: {bug['source']}\n"
            f"Title: {bug['title']}\n"
            f"Product: {bug['product']}\n"
            f"Component: {bug['component']}\n"
            f"Severity: {bug['severity']}\n"
            f"Priority: {bug['priority']}\n"
            f"Status: {bug['status']}\n"
            f"Resolution: {bug['resolution']}\n"
            f"Similarity: {bug['similarity']}\n"
            f"Historical Details:\n"
            f"{bug['text']}\n"
            f"{'-' * 60}\n"

        )


    return "\n".join(
        context_parts
    )