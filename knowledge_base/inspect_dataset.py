import pandas as pd
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Sample dataset location
DATASET_PATH = (
    BASE_DIR
    / "data"
    / "historical"
    / "sample_historical_bugs.csv"
)


print("Loading historical bug dataset...")

df = pd.read_csv(DATASET_PATH)


print("\nDataset loaded successfully!")

print("\nNumber of bug reports:")
print(len(df))

print("\nColumns:")
print(list(df.columns))

print("\nFirst 5 bug reports:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nBug sources:")
print(df["source"].value_counts())