import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "historical"
    / "sample_historical_bugs.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "historical"
)

OUTPUT_FILE = OUTPUT_DIR / "cleaned_historical_bugs.csv"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

print("Loading historical bug dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Loaded {len(df)} bug reports.")


# ---------------------------------------------------------
# STANDARDIZE COLUMN NAMES
# ---------------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# ---------------------------------------------------------
# CLEAN TEXT COLUMNS
# ---------------------------------------------------------

text_columns = [
    "bug_id",
    "source",
    "title",
    "description",
    "component",
    "severity",
    "status",
    "resolution"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )


# ---------------------------------------------------------
# REMOVE EMPTY BUG REPORTS
# ---------------------------------------------------------

df = df[
    (df["bug_id"] != "") &
    (df["title"] != "") &
    (df["description"] != "")
]


# ---------------------------------------------------------
# REMOVE DUPLICATE BUG IDS
# ---------------------------------------------------------

df = df.drop_duplicates(
    subset=["bug_id"]
)


# ---------------------------------------------------------
# CREATE COMBINED SEARCH TEXT
# ---------------------------------------------------------

df["search_text"] = (
    "Title: "
    + df["title"]
    + "\n\n"
    + "Description: "
    + df["description"]
    + "\n\n"
    + "Component: "
    + df["component"]
    + "\n\n"
    + "Severity: "
    + df["severity"]
    + "\n\n"
    + "Resolution: "
    + df["resolution"]
)


# ---------------------------------------------------------
# SAVE CLEAN DATASET
# ---------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

print("\nCleaning completed successfully!")

print(f"Final bug reports: {len(df)}")

print(f"\nSaved cleaned dataset to:")
print(OUTPUT_FILE)

print("\nColumns:")
print(list(df.columns))

print("\nPreview:")
print(
    df[
        [
            "bug_id",
            "source",
            "title",
            "search_text"
        ]
    ].head()
)