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
    / "mozilla"
    / "raw"
    / "sample_mozilla_core.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "historical"
    / "mozilla"
)

OUTPUT_FILE = OUTPUT_DIR / "mozilla_standardized.csv"


# =========================================================
# LOAD DATASET
# =========================================================

print("Loading Mozilla historical defect dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Loaded {len(df):,} Mozilla bug reports.")


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
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

important_columns = [
    "ID",
    "Component",
    "Product",
    "Version",
    "Platform",
    "Op sys",
    "Status",
    "Resolution",
    "Depends on",
    "Dupe of",
    "Blocks",
    "Severity",
    "Priority",
    "Target Milestone",
    "Creator",
    "Creation time",
    "Assigned to",
    "Summary",
    "Description",
    "Keywords",
    "See also",
    "Last change time",
    "QA contact",
    "History/Activity Log",
    "Comments"
]


for column in important_columns:

    if column in df.columns:

        df[column] = clean_text(df[column])


# =========================================================
# CREATE STANDARDIZED DATASET
# =========================================================

standardized = pd.DataFrame()


# Bug ID
standardized["bug_id"] = df["ID"]


# Dataset source
standardized["source"] = "Mozilla"


# Bug title
standardized["title"] = df["Summary"]


# Full description
standardized["description"] = df["Description"]


# Product
standardized["product"] = df["Product"]


# Component
standardized["component"] = df["Component"]


# Severity
standardized["severity"] = df["Severity"]


# Priority
standardized["priority"] = df["Priority"]


# Status
standardized["status"] = df["Status"]


# Resolution
standardized["resolution"] = df["Resolution"]


# Duplicate relationship
standardized["duplicate_info"] = df["Dupe of"]


# Root/related defect
standardized["root_id"] = df["Dupe of"]


# Rediscovery information
standardized["disc_id"] = ""


# Additional useful metadata
standardized["version"] = df["Version"]

standardized["platform"] = df["Platform"]

standardized["operating_system"] = df["Op sys"]

standardized["keywords"] = df["Keywords"]

standardized["comments"] = df["Comments"]

standardized["creation_time"] = df["Creation time"]

standardized["last_change_time"] = df["Last change time"]


# =========================================================
# REMOVE BUGS WITHOUT A TITLE
# =========================================================

standardized = standardized[
    standardized["title"].str.strip() != ""
]


# =========================================================
# REMOVE DUPLICATE BUG IDs
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

    + "\n\nDescription: "
    + standardized["description"]

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

    + "\n\nKeywords: "
    + standardized["keywords"]

    + "\n\nComments: "
    + standardized["comments"]

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
print("MOZILLA STANDARDIZATION COMPLETED")
print("========================================")

print(
    f"\nFinal Mozilla bug reports: "
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