import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR
    / "data"
    / "historical"
    / "apache"
    / "raw"
    / "apache.csv"
)


# ---------------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------------

print("Loading Apache historical defect dataset...")

df = pd.read_csv(DATASET_PATH)


# ---------------------------------------------------------
# BASIC INFORMATION
# ---------------------------------------------------------

print("\nDataset loaded successfully!")

print("\nNumber of bug reports:")
print(len(df))

print("\nNumber of columns:")
print(len(df.columns))

print("\nColumns:")
for column in df.columns:
    print("-", column)


# ---------------------------------------------------------
# DATA TYPES
# ---------------------------------------------------------

print("\nData types:")
print(df.dtypes)


# ---------------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------------

print("\nMissing values:")
print(df.isnull().sum())


# ---------------------------------------------------------
# FIRST RECORDS
# ---------------------------------------------------------

print("\nFirst 3 records:")
print(df.head(3).to_string())


# ---------------------------------------------------------
# DATASET SHAPE
# ---------------------------------------------------------

print("\nDataset shape:")
print(df.shape)