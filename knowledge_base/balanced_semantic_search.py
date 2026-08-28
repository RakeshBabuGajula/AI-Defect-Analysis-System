from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_DB_DIR = (
    BASE_DIR
    / "data"
    / "vector_db"
)


# =========================================================
# CONFIGURATION
# =========================================================

COLLECTION_NAME = "historical_defects_balanced"

MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5


# =========================================================
# LOAD MODEL
# =========================================================

print("Loading embedding model...")

model = SentenceTransformer(
    MODEL_NAME
)

print(
    "Embedding model loaded successfully!"
)


# =========================================================
# CONNECT TO CHROMADB
# =========================================================

print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)


# =========================================================
# LOAD COLLECTION
# =========================================================

collection = client.get_collection(
    name=COLLECTION_NAME
)

print(
    f"Collection: {COLLECTION_NAME}"
)

print(
    f"Vectors available: "
    f"{collection.count():,}"
)


# =========================================================
# SEARCH FUNCTION
# =========================================================

def search_bugs(query, top_k=5):

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    results = collection.query(

        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=top_k

    )

    return results


# =========================================================
# DISPLAY RESULTS
# =========================================================

def display_results(query, results):

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]


    print("\n")
    print("=" * 75)
    print("SEMANTIC RETRIEVAL")
    print("=" * 75)

    print(
        f"\nQuery:\n{query}"
    )


    for rank, (
        document,
        metadata,
        distance
    ) in enumerate(
        zip(
            documents,
            metadatas,
            distances
        ),
        start=1
    ):

        similarity = 1 - distance


        print("\n" + "-" * 75)

        print(
            f"Rank: #{rank}"
        )

        print(
            f"Bug ID: "
            f"{metadata.get('bug_id', 'N/A')}"
        )

        print(
            f"Source: "
            f"{metadata.get('source', 'N/A')}"
        )

        print(
            f"Title: "
            f"{metadata.get('title', 'N/A')}"
        )

        print(
            f"Product: "
            f"{metadata.get('product', 'N/A')}"
        )

        print(
            f"Component: "
            f"{metadata.get('component', 'N/A')}"
        )

        print(
            f"Severity: "
            f"{metadata.get('severity', 'N/A')}"
        )

        print(
            f"Resolution: "
            f"{metadata.get('resolution', 'N/A')}"
        )

        print(
            f"Cosine Distance: "
            f"{distance:.4f}"
        )

        print(
            f"Similarity Score: "
            f"{similarity:.4f}"
        )

        print("\nHistorical Text:")

        print(
            document[:700]
        )


# =========================================================
# TEST CASES
# =========================================================

test_queries = [

    (
        "LOGIN",
        "Application crashes during login after entering valid credentials"
    ),

    (
        "FREEZE",
        "Firefox freezes when opening the settings page"
    ),

    (
        "NULL_POINTER",
        "Null pointer exception causes application crash"
    ),

    (
        "BUILD",
        "Software build fails unexpectedly after changing configuration"
    ),

    (
        "NETWORK",
        "Application fails when connecting to a remote server"
    )

]


# =========================================================
# RUN TESTS
# =========================================================

for test_name, query in test_queries:

    print("\n\n")
    print("#" * 75)

    print(
        f"TEST CASE: {test_name}"
    )

    print(
        "#" * 75
    )

    results = search_bugs(
        query,
        TOP_K
    )

    display_results(
        query,
        results
    )


# =========================================================
# COMPLETION
# =========================================================

print("\n\n")

print("=" * 75)

print(
    "BALANCED SEMANTIC RETRIEVAL TEST COMPLETED"
)

print("=" * 75)