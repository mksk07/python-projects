import pandas as pd
import os

DATA_DIR = "data/2025"

dr = pd.read_csv(f"{DATA_DIR}/2025_drivers.csv")
co = pd.read_csv(f"{DATA_DIR}/2025_constructors.csv")
rs = pd.read_csv(f"{DATA_DIR}/2025_results_so_far.csv")
q = pd.read_csv(f"{DATA_DIR}/2025_qualifying_today.csv")

if 'grid_position' not in q.columns and 'position' in q.columns:
    q.rename(columns={'position':'grid_position'}, inplace=True)

driver_points = rs.groupby("driverId")['points'].sum().reset_index()
driver_points.rename(columns={'points':'rolling_points'}, inplace=True)
driver_points['driver_rank'] = driver_points['rolling_points'].rank(ascending=False, method='dense')

co['constructor_rank'] = co['constructor_points'].rank(ascending=False, method='dense')

merged = q.merge(driver_points, on='driverId', how='left')
merged = merged.merge(dr, on='driverId', how='left')
merged = merged.merge(co[['team','constructor_rank']], on='team', how='left')

merged['rolling_points'] = merged['rolling_points'].fillna(0)
merged['driver_rank'] = merged['driver_rank'].fillna(merged['rolling_points'].rank(ascending=False))
merged['constructor_rank'] = merged['constructor_rank'].fillna(10)

final = merged[['driverId','grid_position','rolling_points','constructor_rank','driver_rank']]
final.to_csv(f"{DATA_DIR}/2025_race_entrylist.csv", index=False)

print("Generated 2025_race_entrylist.csv")
