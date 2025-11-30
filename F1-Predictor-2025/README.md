# F1 2025 Race Winner Predictor

## Quickstart

```
pip install -r requirements.txt
python scripts/preflight.py
python scripts/generate_entrylist.py
python src/train.py
python src/predict.py
```

Get probability for specific driver:

```
python src/predict.py --driver "Lando Norris"
```
