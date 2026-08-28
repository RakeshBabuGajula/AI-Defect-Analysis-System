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
    / "historical"
    / "unified_historical_bugs.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "chunks"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "historical_bug_chunks.jsonl"
)


# =========================================================
# CHUNKING CONFIGURATION
# =========================================================

MAX_CHARS = 2000

OVERLAP_CHARS = 300

# ---------------------------------------------------------
# DEVELOPMENT MODE
# ---------------------------------------------------------
# Start with 5,000 records.
#
# After successful testing, change this to:
#
# LIMIT_ROWS = None
#
# to process the complete 547,187 records.
# ---------------------------------------------------------

LIMIT_ROWS = 5000


# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# TEXT CHUNKING FUNCTION
# =========================================================

def create_chunks(text, max_chars=2000, overlap=300):

    text = str(text).strip()

    if not text:
        return []

    # Small document
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

print("Loading unified historical defect dataset...")

df = pd.read_csv(
    INPUT_FILE,
    nrows=LIMIT_ROWS
)


print(
    f"Loaded {len(df):,} bug reports for chunking."
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [

    "bug_id",
    "source",
    "title",
    "description",
    "product",
    "component",
    "severity",
    "priority",
    "status",
    "resolution",
    "duplicate_info",
    "root_id",
    "disc_id",
    "search_text"

]


missing_columns = [

    column
    for column in required_columns
    if column not in df.columns

]


if missing_columns:

    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# =========================================================
# CREATE / RESET OUTPUT FILE
# =========================================================

if OUTPUT_FILE.exists():

    OUTPUT_FILE.unlink()


# =========================================================
# PROCESS BUG REPORTS
# =========================================================

total_chunks = 0

total_bugs = 0

chunk_distribution = {}


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as output_file:

    for _, row in df.iterrows():

        # -------------------------------------------------
        # BUILD DOCUMENT
        # -------------------------------------------------

        document = (

            f"Bug Title: {row['title']}\n\n"

            f"Description: {row['description']}\n\n"

            f"Product: {row['product']}\n\n"

            f"Component: {row['component']}\n\n"

            f"Severity: {row['severity']}\n\n"

            f"Priority: {row['priority']}\n\n"

            f"Status: {row['status']}\n\n"

            f"Resolution: {row['resolution']}\n\n"

            f"Duplicate Information: "
            f"{row['duplicate_info']}\n\n"

            f"Root ID: {row['root_id']}\n\n"

            f"Discussion ID: {row['disc_id']}"

        )


        # -------------------------------------------------
        # CREATE CHUNKS
        # -------------------------------------------------

        chunks = create_chunks(
            document,
            MAX_CHARS,
            OVERLAP_CHARS
        )


        if not chunks:
            continue


        total_bugs += 1

        total_chunks += len(chunks)

        chunk_distribution[len(chunks)] = (
            chunk_distribution.get(
                len(chunks),
                0
            ) + 1
        )


        # -------------------------------------------------
        # STORE EACH CHUNK
        # -------------------------------------------------

        for chunk_index, chunk in enumerate(chunks):

            chunk_record = {

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
                    chunk_record,
                    ensure_ascii=False
                )
                + "\n"
            )


# =========================================================
# RESULTS
# =========================================================

print("\n========================================")

print("CHUNKING COMPLETED")

print("========================================")


print(
    f"\nBug reports processed: "
    f"{total_bugs:,}"
)


print(
    f"Total chunks created: "
    f"{total_chunks:,}"
)


if total_bugs > 0:

    average_chunks = (
        total_chunks / total_bugs
    )

    print(
        f"Average chunks per bug: "
        f"{average_chunks:.2f}"
    )


print("\nChunk distribution:")

for count, bugs in sorted(
    chunk_distribution.items()
):

    print(
        f"{count} chunk(s): "
        f"{bugs:,} bug reports"
    )


print("\nChunk configuration:")

print(
    f"Maximum characters per chunk: "
    f"{MAX_CHARS}"
)

print(
    f"Overlap characters: "
    f"{OVERLAP_CHARS}"
)


print("\nOutput file:")

print(OUTPUT_FILE)