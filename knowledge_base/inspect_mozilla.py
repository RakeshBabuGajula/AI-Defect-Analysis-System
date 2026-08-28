import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR
    / "data"
    / "historical"
    / "mozilla"
    / "raw"
    / "sample_mozilla_core.csv"
)

if not DATASET_PATH.exists():
    DATASET_PATH = (
        BASE_DIR
        / "data"
        / "submissions"
        / "historical"
        / "mozilla"
        / "sample_mozilla_core.csv"
    )


# =========================================================
# LOAD DATASET
# =========================================================

print("Loading Mozilla historical defect dataset...")

df = pd.read_csv(DATASET_PATH)


# =========================================================
# BASIC INFORMATION
# =========================================================

print("\nDataset loaded successfully!")

print("\nNumber of bug reports:")
print(f"{len(df):,}")

print("\nNumber of columns:")
print(len(df.columns))


# =========================================================
# COLUMNS
# =========================================================

print("\nColumns:")

for column in df.columns:
    print("-", column)


# =========================================================
# DATA TYPES
# =========================================================

print("\nData types:")

print(df.dtypes)


# =========================================================
# MISSING VALUES
# =========================================================

print("\nMissing values:")

print(df.isnull().sum())


# =========================================================
# FIRST 3 RECORDS
# =========================================================

print("\nFirst 3 records:")

print(
    df.head(3).to_string()
)


# =========================================================
# DATASET SHAPE
# =========================================================

print("\nDataset shape:")

print(df.shape)