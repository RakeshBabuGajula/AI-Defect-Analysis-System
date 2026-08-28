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

COLLECTION_NAME = "historical_defects_v2"

MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("Loading embedding model...")

model = SentenceTransformer(
    MODEL_NAME
)

print("Embedding model loaded successfully!")


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
    f"Collection loaded: {COLLECTION_NAME}"
)

print(
    f"Vectors available: {collection.count():,}"
)


# =========================================================
# SEARCH FUNCTION
# =========================================================

def search_historical_bugs(query, top_k=5):

    # -----------------------------------------------------
    # Generate query embedding
    # -----------------------------------------------------

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )


    # -----------------------------------------------------
    # Search ChromaDB
    # -----------------------------------------------------

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

    print("\n")
    print("=" * 70)
    print("SEMANTIC SEARCH RESULTS")
    print("=" * 70)

    print(f"\nQuery:")
    print(query)


    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]


    for index, (
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

        # Chroma cosine distance:
        # similarity = 1 - distance

        similarity = 1 - distance


        print("\n" + "-" * 70)

        print(f"Rank: #{index}")

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
            f"Priority: "
            f"{metadata.get('priority', 'N/A')}"
        )

        print(
            f"Status: "
            f"{metadata.get('status', 'N/A')}"
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
            document[:800]
        )


# =========================================================
# TEST QUERIES
# =========================================================

test_queries = [

    "Application crashes during login after entering valid credentials",

    "Firefox freezes when opening settings",

    "Null pointer exception causes application crash"

]


# =========================================================
# RUN TESTS
# =========================================================

for query in test_queries:

    results = search_historical_bugs(
        query,
        TOP_K
    )

    display_results(
        query,
        results
    )


print("\n")
print("=" * 70)
print("SEMANTIC SEARCH TEST COMPLETED")
print("=" * 70)