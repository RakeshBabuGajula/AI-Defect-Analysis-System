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
    / "balanced_bug_embeddings.jsonl"
)

VECTOR_DB_DIR = (
    BASE_DIR
    / "data"
    / "vector_db"
)


# =========================================================
# CONFIGURATION
# =========================================================

COLLECTION_NAME = "historical_defects_balanced"

BATCH_SIZE = 500


# =========================================================
# CONNECT TO CHROMADB
# =========================================================

print("Initializing ChromaDB...")

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)


# =========================================================
# CREATE COSINE COLLECTION
# =========================================================

print(
    f"Creating collection: {COLLECTION_NAME}"
)

collection = client.get_or_create_collection(

    name=COLLECTION_NAME,

    metadata={
        "description":
            "Balanced multi-source historical "
            "software defect knowledge base",

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

print("\nLoading balanced embeddings...")

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
# PREPARE RECORDS
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

    metadata["chunk_index"] = int(
        record["chunk_index"]
    )

    metadata["total_chunks"] = int(
        record["total_chunks"]
    )

    metadatas.append(metadata)


# =========================================================
# INDEX INTO CHROMADB
# =========================================================

print("\nIndexing vectors into ChromaDB...")

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

    indexed = min(
        end,
        len(ids)
    )

    print(
        f"Indexed {indexed:,} / "
        f"{len(ids):,}"
    )


# =========================================================
# VALIDATE
# =========================================================

total_vectors = collection.count()


print("\n========================================")
print("BALANCED VECTOR DATABASE COMPLETED")
print("========================================")

print(
    f"\nCollection: "
    f"{COLLECTION_NAME}"
)

print(
    f"Expected vectors: "
    f"{len(records):,}"
)

print(
    f"Stored vectors: "
    f"{total_vectors:,}"
)

print(
    "\nDistance metric: cosine"
)

print(
    "\nSources represented:"
)

source_counts = {}

for record in records:

    source = record["source"]

    source_counts[source] = (
        source_counts.get(source, 0) + 1
    )


for source, count in sorted(
    source_counts.items()
):

    print(
        f"- {source}: "
        f"{count:,} chunks"
    )


print(
    "\nVector database directory:"
)

print(VECTOR_DB_DIR)


print("\n========================================")

if total_vectors == len(records):

    print(
        "VALIDATION PASSED ✅"
    )

else:

    print(
        "VALIDATION FAILED ❌"
    )

print("========================================")