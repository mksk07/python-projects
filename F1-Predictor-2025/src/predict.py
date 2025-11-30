import pandas as pd
import joblib
import subprocess
import os
import argparse

ENTRY = 'data/2025/2025_race_entrylist.csv'
MODEL = 'model.pkl'
DRIVERS = 'data/2025/2025_drivers.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--driver', type=str)
args = parser.parse_args()

if not os.path.exists(MODEL):
    subprocess.check_call(['python','src/train.py'])

entry = pd.read_csv(ENTRY)
dr = pd.read_csv(DRIVERS)
model = joblib.load(MODEL)
features = ["grid_position","rolling_points","constructor_rank","driver_rank"]

entry['win_prob'] = model.predict_proba(entry[features])[:,1]
out = entry.merge(dr[['driverId','driver']], on='driverId', how='left')

if args.driver:
    d = args.driver.lower()
    row = out[out['driver'].str.lower().str.contains(d)]
    print(row[['driver','grid_position','win_prob']])
else:
    print(out[['driver','grid_position','win_prob']].sort_values('win_prob', ascending=False))
