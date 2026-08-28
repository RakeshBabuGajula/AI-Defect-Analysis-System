import json
from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "chunks"
    / "historical_bug_chunks.jsonl"
)


# =========================================================
# LOAD AND INSPECT CHUNKS
# =========================================================

print("Loading generated historical bug chunks...")

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
    f"\nTotal chunks loaded: "
    f"{len(chunks):,}"
)


# =========================================================
# DISPLAY FIRST 3 CHUNKS
# =========================================================

print("\n========================================")
print("FIRST 3 CHUNKS")
print("========================================")


for index, chunk in enumerate(chunks[:3], start=1):

    print(
        f"\n\n========== CHUNK {index} =========="
    )

    print(
        f"\nChunk ID: "
        f"{chunk['chunk_id']}"
    )

    print(
        f"Bug ID: "
        f"{chunk['bug_id']}"
    )

    print(
        f"Source: "
        f"{chunk['source']}"
    )

    print(
        f"Chunk index: "
        f"{chunk['chunk_index']}"
    )

    print(
        f"Total chunks for bug: "
        f"{chunk['total_chunks']}"
    )

    print("\n--- TEXT ---")

    print(chunk["text"])

    print("\n--- METADATA ---")

    for key, value in chunk["metadata"].items():

        print(
            f"{key}: {value}"
        )


# =========================================================
# BASIC VALIDATION
# =========================================================

print("\n\n========================================")
print("CHUNK VALIDATION")
print("========================================")


required_fields = [
    "chunk_id",
    "bug_id",
    "source",
    "chunk_index",
    "total_chunks",
    "text",
    "metadata"
]


validation_passed = True


for index, chunk in enumerate(chunks):

    for field in required_fields:

        if field not in chunk:

            print(
                f"ERROR: Chunk {index} "
                f"missing field: {field}"
            )

            validation_passed = False


# =========================================================
# EMPTY TEXT CHECK
# =========================================================

empty_text_chunks = [

    chunk
    for chunk in chunks
    if not str(chunk["text"]).strip()

]


print(
    f"\nEmpty text chunks: "
    f"{len(empty_text_chunks)}"
)


# =========================================================
# DUPLICATE CHUNK ID CHECK
# =========================================================

chunk_ids = [
    chunk["chunk_id"]
    for chunk in chunks
]


duplicate_ids = (
    len(chunk_ids)
    - len(set(chunk_ids))
)


print(
    f"Duplicate chunk IDs: "
    f"{duplicate_ids}"
)


# =========================================================
# SOURCES
# =========================================================

sources = {}

for chunk in chunks:

    source = chunk["source"]

    sources[source] = (
        sources.get(source, 0) + 1
    )


print("\nChunks by source:")

for source, count in sources.items():

    print(
        f"- {source}: {count:,}"
    )


# =========================================================
# FINAL RESULT
# =========================================================

print("\n========================================")

if validation_passed and not empty_text_chunks and duplicate_ids == 0:

    print("VALIDATION PASSED [PASSED]")

else:

    print("VALIDATION FAILED [FAILED]")

print("========================================")