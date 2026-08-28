import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "historical"
    / "eclipse"
    / "raw"
    / "eclipse.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "historical"
    / "eclipse"
)

OUTPUT_FILE = OUTPUT_DIR / "eclipse_standardized.csv"


# =========================================================
# LOAD DATASET
# =========================================================

print("Loading Eclipse historical defect dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Loaded {len(df):,} Eclipse bug reports.")


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def clean_text(series):

    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )


# =========================================================
# CLEAN IMPORTANT FIELDS
# =========================================================

text_columns = [
    "id",
    "product",
    "component",
    "bug_status",
    "resolution",
    "priority",
    "bug_severity",
    "version",
    "short_desc",
    "dup_list",
    "root_id",
    "disc_id"
]


for column in text_columns:

    if column in df.columns:

        df[column] = clean_text(df[column])


# =========================================================
# CREATE STANDARDIZED DATASET
# =========================================================

standardized = pd.DataFrame()


standardized["bug_id"] = df["id"]

standardized["source"] = "Eclipse"

standardized["title"] = df["short_desc"]

# This dataset version does not provide a separate
# long description field.
standardized["description"] = df["short_desc"]

standardized["product"] = df["product"]

standardized["component"] = df["component"]

standardized["severity"] = df["bug_severity"]

standardized["priority"] = df["priority"]

standardized["status"] = df["bug_status"]

standardized["resolution"] = df["resolution"]

standardized["duplicate_info"] = df["dup_list"]

standardized["root_id"] = df["root_id"]

standardized["disc_id"] = df["disc_id"]


# =========================================================
# REMOVE RECORDS WITHOUT USEFUL TITLE
# =========================================================

standardized = standardized[
    standardized["title"].str.strip() != ""
]


# =========================================================
# REMOVE DUPLICATE BUG IDS
# =========================================================

standardized = standardized.drop_duplicates(
    subset=["bug_id"]
)


# =========================================================
# CREATE SEARCH TEXT
# =========================================================

standardized["search_text"] = (

    "Title: "
    + standardized["title"]

    + "\n\nProduct: "
    + standardized["product"]

    + "\n\nComponent: "
    + standardized["component"]

    + "\n\nSeverity: "
    + standardized["severity"]

    + "\n\nPriority: "
    + standardized["priority"]

    + "\n\nStatus: "
    + standardized["status"]

    + "\n\nResolution: "
    + standardized["resolution"]

)


# =========================================================
# SAVE DATASET
# =========================================================

standardized.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n========================================")
print("ECLIPSE STANDARDIZATION COMPLETED")
print("========================================")

print(
    f"\nFinal Eclipse bug reports: "
    f"{len(standardized):,}"
)

print("\nStandardized columns:")

for column in standardized.columns:

    print("-", column)


print("\nOutput file:")

print(OUTPUT_FILE)


print("\nFirst 5 standardized records:")

print(
    standardized[
        [
            "bug_id",
            "source",
            "title",
            "product",
            "component",
            "severity",
            "priority",
            "status",
            "resolution"
        ]
    ]
    .head()
    .to_string(index=False)
)


print("\nMissing values:")

print(
    standardized.isnull().sum()
)