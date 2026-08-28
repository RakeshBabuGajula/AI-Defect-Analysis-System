import pandas as pd
import json
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "balanced_test_bugs.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "chunks"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "balanced_bug_chunks.jsonl"
)


# =========================================================
# CHUNK CONFIGURATION
# =========================================================

MAX_CHARS = 2000

OVERLAP_CHARS = 300


# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# CHUNKING FUNCTION
# =========================================================

def create_chunks(
    text,
    max_chars=2000,
    overlap=300
):

    text = str(text).strip()

    if not text:
        return []

    if len(text) <= max_chars:
        return [text]

    chunks = []

    start = 0

    while start < len(text):

        end = start + max_chars

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# =========================================================
# LOAD DATASET
# =========================================================

print("Loading balanced historical defect dataset...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Loaded {len(df):,} bug reports."
)


# =========================================================
# VALIDATE SOURCE DISTRIBUTION
# =========================================================

print("\nSource distribution:")

print(
    df["source"].value_counts()
)


# =========================================================
# REMOVE OLD OUTPUT
# =========================================================

if OUTPUT_FILE.exists():

    OUTPUT_FILE.unlink()


# =========================================================
# PROCESS RECORDS
# =========================================================

total_chunks = 0

chunk_distribution = {}


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as output_file:

    for _, row in df.iterrows():

        # -------------------------------------------------
        # Build structured document
        # -------------------------------------------------

        document = (

            f"Bug Title: "
            f"{row['title']}\n\n"

            f"Description: "
            f"{row['description']}\n\n"

            f"Product: "
            f"{row['product']}\n\n"

            f"Component: "
            f"{row['component']}\n\n"

            f"Severity: "
            f"{row['severity']}\n\n"

            f"Priority: "
            f"{row['priority']}\n\n"

            f"Status: "
            f"{row['status']}\n\n"

            f"Resolution: "
            f"{row['resolution']}\n\n"

            f"Duplicate Information: "
            f"{row['duplicate_info']}\n\n"

            f"Root ID: "
            f"{row['root_id']}\n\n"

            f"Discussion ID: "
            f"{row['disc_id']}"

        )


        # -------------------------------------------------
        # Create chunks
        # -------------------------------------------------

        chunks = create_chunks(
            document,
            MAX_CHARS,
            OVERLAP_CHARS
        )


        if not chunks:
            continue


        chunk_distribution[
            len(chunks)
        ] = (
            chunk_distribution.get(
                len(chunks),
                0
            ) + 1
        )


        total_chunks += len(chunks)


        # -------------------------------------------------
        # Save chunks
        # -------------------------------------------------

        for chunk_index, chunk in enumerate(chunks):

            record = {

                "chunk_id":
                    f"{row['source']}_"
                    f"{row['bug_id']}_"
                    f"chunk_{chunk_index}",

                "bug_id":
                    str(row["bug_id"]),

                "source":
                    str(row["source"]),

                "chunk_index":
                    chunk_index,

                "total_chunks":
                    len(chunks),

                "text":
                    chunk,

                "metadata": {

                    "title":
                        str(row["title"]),

                    "product":
                        str(row["product"]),

                    "component":
                        str(row["component"]),

                    "severity":
                        str(row["severity"]),

                    "priority":
                        str(row["priority"]),

                    "status":
                        str(row["status"]),

                    "resolution":
                        str(row["resolution"]),

                    "duplicate_info":
                        str(row["duplicate_info"]),

                    "root_id":
                        str(row["root_id"]),

                    "disc_id":
                        str(row["disc_id"])

                }

            }


            output_file.write(
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
print("BALANCED CHUNKING COMPLETED")
print("========================================")

print(
    f"\nBug reports processed: "
    f"{len(df):,}"
)

print(
    f"Total chunks created: "
    f"{total_chunks:,}"
)

print("\nChunk distribution:")

for count, bugs in sorted(
    chunk_distribution.items()
):

    print(
        f"- {count} chunk(s): "
        f"{bugs:,} bug reports"
    )


print("\nConfiguration:")

print(
    f"- Maximum characters: "
    f"{MAX_CHARS}"
)

print(
    f"- Overlap characters: "
    f"{OVERLAP_CHARS}"
)


print("\nOutput file:")

print(OUTPUT_FILE)