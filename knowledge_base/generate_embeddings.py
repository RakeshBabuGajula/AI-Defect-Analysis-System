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
    / "historical_bug_chunks.jsonl"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "embeddings"
    / "historical_bug_embeddings.jsonl"
)


# =========================================================
# CONFIGURATION
# =========================================================

MODEL_NAME = "all-MiniLM-L6-v2"


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

print("Loading historical bug chunks...")

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
# LOAD EMBEDDING MODEL
# =========================================================

print("\nLoading embedding model...")

print(
    f"Model: {MODEL_NAME}"
)

model = SentenceTransformer(
    MODEL_NAME
)

print("Embedding model loaded successfully!")


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
    show_progress_bar=True,
    normalize_embeddings=True
)


print("\nEmbedding generation completed!")


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
# DISPLAY RESULTS
# =========================================================

print("\n========================================")
print("EMBEDDINGS GENERATED SUCCESSFULLY")
print("========================================")

print(
    f"\nTotal embeddings: "
    f"{len(embeddings):,}"
)

print(
    f"Embedding dimensions: "
    f"{len(embeddings[0])}"
)

print("\nModel:")

print(MODEL_NAME)

print("\nOutput file:")

print(OUTPUT_FILE)