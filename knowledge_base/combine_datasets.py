import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

HISTORICAL_DIR = (
    BASE_DIR
    / "data"
    / "historical"
)


# =========================================================
# INPUT FILES
# =========================================================

APACHE_FILE = (
    HISTORICAL_DIR
    / "apache"
    / "apache_standardized.csv"
)

ECLIPSE_FILE = (
    HISTORICAL_DIR
    / "eclipse"
    / "eclipse_standardized.csv"
)

MOZILLA_FILE = (
    HISTORICAL_DIR
    / "mozilla"
    / "mozilla_standardized.csv"
)


# =========================================================
# OUTPUT FILE
# =========================================================

OUTPUT_FILE = (
    HISTORICAL_DIR
    / "unified_historical_bugs.csv"
)


# =========================================================
# LOAD DATASETS
# =========================================================

print("Loading standardized historical datasets...")

apache = pd.read_csv(APACHE_FILE)

eclipse = pd.read_csv(ECLIPSE_FILE)

mozilla = pd.read_csv(MOZILLA_FILE)


print("\nDataset sizes:")

print(f"Apache  : {len(apache):,}")

print(f"Eclipse : {len(eclipse):,}")

print(f"Mozilla : {len(mozilla):,}")


# =========================================================
# FIND COMMON COLUMNS
# =========================================================

common_columns = [

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


# =========================================================
# ENSURE ALL DATASETS HAVE REQUIRED COLUMNS
# =========================================================

for dataset_name, dataset in [

    ("Apache", apache),
    ("Eclipse", eclipse),
    ("Mozilla", mozilla)

]:

    missing_columns = [
        column
        for column in common_columns
        if column not in dataset.columns
    ]

    if missing_columns:

        raise ValueError(
            f"{dataset_name} is missing columns: "
            f"{missing_columns}"
        )


# =========================================================
# SELECT COMMON SCHEMA
# =========================================================

apache = apache[common_columns]

eclipse = eclipse[common_columns]

mozilla = mozilla[common_columns]


# =========================================================
# COMBINE DATASETS
# =========================================================

print("\nCombining datasets...")

unified = pd.concat(
    [
        apache,
        eclipse,
        mozilla
    ],
    ignore_index=True
)


# =========================================================
# CLEAN TEXT FIELDS
# =========================================================

text_columns = [

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


for column in text_columns:

    unified[column] = (
        unified[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# =========================================================
# REMOVE DUPLICATES
# =========================================================

before_duplicates = len(unified)

unified = unified.drop_duplicates(
    subset=["source", "bug_id"]
)

after_duplicates = len(unified)

duplicates_removed = (
    before_duplicates - after_duplicates
)


# =========================================================
# REMOVE EMPTY TITLES
# =========================================================

before_empty = len(unified)

unified = unified[
    unified["title"].str.strip() != ""
]

empty_removed = (
    before_empty - len(unified)
)


# =========================================================
# RESET INDEX
# =========================================================

unified = unified.reset_index(drop=True)


# =========================================================
# SAVE DATASET
# =========================================================

unified.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================================================
# RESULTS
# =========================================================

print("\n========================================")
print("UNIFIED DATASET CREATED")
print("========================================")

print(
    f"\nTotal records before cleaning: "
    f"{before_duplicates:,}"
)

print(
    f"Duplicate records removed: "
    f"{duplicates_removed:,}"
)

print(
    f"Empty-title records removed: "
    f"{empty_removed:,}"
)

print(
    f"\nFinal unified records: "
    f"{len(unified):,}"
)

print("\nRecords by source:")

print(
    unified["source"]
    .value_counts()
)


print("\nFinal schema:")

for column in unified.columns:

    print("-", column)


print("\nOutput file:")

print(OUTPUT_FILE)


print("\nFirst 5 records:")

print(
    unified[
        [
            "bug_id",
            "source",
            "title",
            "product",
            "component",
            "severity"
        ]
    ]
    .head()
    .to_string(index=False)
)