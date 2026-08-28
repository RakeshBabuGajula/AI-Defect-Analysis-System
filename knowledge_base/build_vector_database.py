import json
from pathlib import Path

import chromadb


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

EMBEDDINGS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "embeddings"
    / "historical_bug_embeddings.jsonl"
)

VECTOR_DB_DIR = (
    BASE_DIR
    / "data"
    / "vector_db"
)


# =========================================================
# CONFIGURATION
# =========================================================

COLLECTION_NAME = "historical_defects_v2"


# =========================================================
# CREATE VECTOR DATABASE
# =========================================================

print("Initializing ChromaDB...")

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)


# =========================================================
# CREATE / RESET COLLECTION
# =========================================================

print(
    f"Creating collection: "
    f"{COLLECTION_NAME}"
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={
        "description":
            "Historical software defect knowledge base",
        "embedding_model":
            "all-MiniLM-L6-v2"
    },
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)

# =========================================================
# LOAD EMBEDDINGS
# =========================================================

print("\nLoading generated embeddings...")

records = []

with open(
    EMBEDDINGS_FILE,
    "r",
    encoding="utf-8"
) as file:

    for line in file:

        if line.strip():

            records.append(
                json.loads(line)
            )


print(
    f"Loaded {len(records):,} embedding records."
)


# =========================================================
# PREPARE DATA
# =========================================================

ids = []

documents = []

embeddings = []

metadatas = []


for record in records:

    ids.append(
        str(record["chunk_id"])
    )

    documents.append(
        str(record["text"])
    )

    embeddings.append(
        record["embedding"]
    )

    metadata = record["metadata"].copy()

    metadata["bug_id"] = str(
        record["bug_id"]
    )

    metadata["source"] = str(
        record["source"]
    )

    metadatas.append(
        metadata
    )


# =========================================================
# INSERT INTO CHROMADB
# =========================================================

print("\nIndexing vectors into ChromaDB...")

BATCH_SIZE = 500


for start in range(
    0,
    len(ids),
    BATCH_SIZE
):

    end = start + BATCH_SIZE

    collection.upsert(

        ids=ids[start:end],

        documents=documents[start:end],

        embeddings=embeddings[start:end],

        metadatas=metadatas[start:end]

    )

    print(
        f"Indexed {min(end, len(ids)):,} "
        f"/ {len(ids):,}"
    )


# =========================================================
# VERIFY COLLECTION
# =========================================================

total = collection.count()


print("\n========================================")

print("CHROMADB INDEXING COMPLETED")

print("========================================")


print(
    f"\nCollection: "
    f"{COLLECTION_NAME}"
)

print(
    f"Vectors stored: "
    f"{total:,}"
)

print(
    f"Vector database location:"
)

print(VECTOR_DB_DIR)


# =========================================================
# BASIC VALIDATION
# =========================================================

if total == len(records):

    print(
        "\nVALIDATION PASSED [PASSED]"
    )

else:

    print(
        "\nVALIDATION FAILED [FAILED]"
    )

    print(
        f"Expected: {len(records):,}"
    )

    print(
        f"Found: {total:,}"
    )