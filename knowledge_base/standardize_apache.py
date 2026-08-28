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
    / "apache"
    / "raw"
    / "apache.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "historical"
    / "apache"
)

OUTPUT_FILE = OUTPUT_DIR / "apache_standardized.csv"


# =========================================================
# LOAD DATASET
# =========================================================

print("Loading Apache historical defect dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Loaded {len(df):,} Apache bug reports.")


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

standardized["source"] = "Apache"

standardized["title"] = df["short_desc"]

# Apache dataset does not provide a separate long
# description field in this version.
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
# REMOVE RECORDS WITHOUT A USEFUL TITLE
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
    + "\n\n"
    + "Product: "
    + standardized["product"]
    + "\n\n"
    + "Component: "
    + standardized["component"]
    + "\n\n"
    + "Severity: "
    + standardized["severity"]
    + "\n\n"
    + "Priority: "
    + standardized["priority"]
    + "\n\n"
    + "Status: "
    + standardized["status"]
    + "\n\n"
    + "Resolution: "
    + standardized["resolution"]
)


# =========================================================
# SAVE STANDARDIZED DATASET
# =========================================================

standardized.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n========================================")
print("STANDARDIZATION COMPLETED")
print("========================================")

print(
    f"\nFinal Apache bug reports: "
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
    ].head().to_string(index=False)
)

print("\nMissing values in standardized dataset:")

print(
    standardized.isnull().sum()
)