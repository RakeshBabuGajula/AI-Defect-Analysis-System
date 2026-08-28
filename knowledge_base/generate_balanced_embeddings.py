import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "chunks"
    / "balanced_bug_chunks.jsonl"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "embeddings"
    / "balanced_bug_embeddings.jsonl"
)


# =========================================================
# CONFIGURATION
# =========================================================

MODEL_NAME = "all-MiniLM-L6-v2"

BATCH_SIZE = 64


# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# LOAD CHUNKS
# =========================================================

print("Loading balanced bug chunks...")

chunks = []

with open(
    CHUNKS_FILE,
    "r",
    encoding="utf-8"
) as file:

    for line in file:

        if line.strip():

            chunks.append(
                json.loads(line)
            )


print(
    f"Loaded {len(chunks):,} chunks."
)


# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading embedding model...")

print(
    f"Model: {MODEL_NAME}"
)

model = SentenceTransformer(
    MODEL_NAME
)

print(
    "Embedding model loaded successfully!"
)


# =========================================================
# EXTRACT TEXT
# =========================================================

texts = [

    chunk["text"]
    for chunk in chunks

]


# =========================================================
# GENERATE EMBEDDINGS
# =========================================================

print("\nGenerating embeddings...")

embeddings = model.encode(

    texts,

    batch_size=BATCH_SIZE,

    show_progress_bar=True,

    normalize_embeddings=True

)


print(
    "\nEmbedding generation completed!"
)


# =========================================================
# SAVE EMBEDDINGS
# =========================================================

print("\nSaving embeddings...")

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        record = {

            "chunk_id":
                chunk["chunk_id"],

            "bug_id":
                chunk["bug_id"],

            "source":
                chunk["source"],

            "chunk_index":
                chunk["chunk_index"],

            "total_chunks":
                chunk["total_chunks"],

            "text":
                chunk["text"],

            "metadata":
                chunk["metadata"],

            "embedding":
                embedding.tolist()

        }

        file.write(

            json.dumps(
                record,
                ensure_ascii=False
            )

            + "\n"

        )


# =========================================================
# RESULTS
# =========================================================

print("\n========================================")
print("BALANCED EMBEDDINGS COMPLETED")
print("========================================")

print(
    f"\nTotal chunks embedded: "
    f"{len(embeddings):,}"
)

print(
    f"Embedding dimensions: "
    f"{len(embeddings[0])}"
)

print(
    f"Model: "
    f"{MODEL_NAME}"
)

print(
    f"\nOutput file:\n{OUTPUT_FILE}"
)