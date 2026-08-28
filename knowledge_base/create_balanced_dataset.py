import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

HISTORICAL_DIR = (
    BASE_DIR
    / "data"
    / "historical"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "balanced_test_bugs.csv"
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
# CONFIGURATION
# =========================================================

APACHE_LIMIT = 2000

ECLIPSE_LIMIT = 2000

MOZILLA_LIMIT = 99


# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# LOAD DATASETS
# =========================================================

print("Loading standardized datasets...")

apache = pd.read_csv(APACHE_FILE)

eclipse = pd.read_csv(ECLIPSE_FILE)

mozilla = pd.read_csv(MOZILLA_FILE)


print("\nAvailable records:")

print(f"Apache  : {len(apache):,}")

print(f"Eclipse : {len(eclipse):,}")

print(f"Mozilla : {len(mozilla):,}")


# =========================================================
# SAMPLE DATA
# =========================================================

apache_sample = apache.sample(
    n=min(APACHE_LIMIT, len(apache)),
    random_state=42
)

eclipse_sample = eclipse.sample(
    n=min(ECLIPSE_LIMIT, len(eclipse)),
    random_state=42
)

mozilla_sample = mozilla.sample(
    n=min(MOZILLA_LIMIT, len(mozilla)),
    random_state=42
)


# =========================================================
# COMBINE
# =========================================================

balanced = pd.concat(
    [
        apache_sample,
        eclipse_sample,
        mozilla_sample
    ],
    ignore_index=True
)


# =========================================================
# SHUFFLE
# =========================================================

balanced = balanced.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# =========================================================
# SAVE
# =========================================================

balanced.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================================================
# RESULTS
# =========================================================

print("\n========================================")
print("BALANCED TEST DATASET CREATED")
print("========================================")

print(
    f"\nTotal records: "
    f"{len(balanced):,}"
)

print("\nRecords by source:")

print(
    balanced["source"]
    .value_counts()
)

print("\nOutput file:")

print(OUTPUT_FILE)