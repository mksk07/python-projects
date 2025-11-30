import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

ENTRY = 'data/2025/2025_race_entrylist.csv'
MODEL = 'model.pkl'

if not os.path.exists(ENTRY):
    print('Run generate_entrylist.py first')
    raise SystemExit

entry = pd.read_csv(ENTRY)
features = ["grid_position","rolling_points","constructor_rank","driver_rank"]

entry['winner'] = np.where(entry['grid_position']==1,1,0)
X = entry[features]
y = entry['winner']

model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
model.fit(X, y)
joblib.dump(model, MODEL)

print("Model trained and saved as model.pkl")
