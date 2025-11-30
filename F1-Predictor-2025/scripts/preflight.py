import os
import sys
import pandas as pd

DATA_DIR = "data/2025"
REQUIRED = [
    "2025_drivers.csv",
    "2025_constructors.csv",
    "2025_results_so_far.csv",
    "2025_qualifying_today.csv"
]

missing = [f for f in REQUIRED if not os.path.exists(os.path.join(DATA_DIR, f))]
if missing:
    print("Missing CSV files:")
    for m in missing:
        print("-", m)
    sys.exit(1)

try:
    pd.read_csv(os.path.join(DATA_DIR, "2025_drivers.csv"))
    pd.read_csv(os.path.join(DATA_DIR, "2025_constructors.csv"))
    pd.read_csv(os.path.join(DATA_DIR, "2025_results_so_far.csv"))
    q = pd.read_csv(os.path.join(DATA_DIR, "2025_qualifying_today.csv"))
except Exception as e:
    print("CSV read error:", e)
    sys.exit(1)

if 'grid_position' not in q.columns and 'position' in q.columns:
    q.rename(columns={'position':'grid_position'}, inplace=True)
    q.to_csv(os.path.join(DATA_DIR, "2025_qualifying_today.csv"), index=False)

print("Preflight checks passed.")
