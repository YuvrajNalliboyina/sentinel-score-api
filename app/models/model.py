import xgboost as xgb
import numpy as np
import pandas as pd
import shap
import json
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "xgboost_best.json"
FEATURES_PATH = Path(__file__).parent.parent / "feature_columns.json"

# Load model once
model = xgb.XGBClassifier()
model.load_model(str(MODEL_PATH))

# Load feature names from JSON
with open(str(FEATURES_PATH)) as f:
    FEATURE_COLUMNS = json.load(f)

# Load SHAP explainer once
explainer = shap.TreeExplainer(model)

def _prepare_features(features: dict) -> pd.DataFrame:
    row = {col: 0 for col in FEATURE_COLUMNS}
    row.update(features)
    return pd.DataFrame([row])[FEATURE_COLUMNS]

def predict(features: dict) -> dict:
    df = _prepare_features(features)
    
    fraud_probability = model.predict_proba(df)[0][1]
    fraud_probability = round(float(fraud_probability), 4)
    
    if fraud_probability >= 0.7:
        decision = "REJECT"
    elif fraud_probability >= 0.4:
        decision = "FLAG"
    else:
        decision = "APPROVE"
    
    return {
        "fraud_score": fraud_probability,
        "decision": decision
    }

def explain(features: dict) -> dict:
    df = _prepare_features(features)
    
    fraud_probability = model.predict_proba(df)[0][1]
    fraud_probability = round(float(fraud_probability), 4)
    
    if fraud_probability >= 0.7:
        decision = "REJECT"
    elif fraud_probability >= 0.4:
        decision = "FLAG"
    else:
        decision = "APPROVE"
    
    shap_values = explainer.shap_values(df)
    shap_series = pd.Series(shap_values[0], index=FEATURE_COLUMNS)
    
    top_features = shap_series.abs().nlargest(3)
    
    top_reasons = []
    for feature, _ in top_features.items():
        value = df[feature].values[0]
        shap_val = shap_series[feature]
        direction = "increased" if shap_val > 0 else "decreased"
        top_reasons.append(f"{feature} = {round(float(value), 2)} ({direction} fraud risk)")
    
    return {
        "fraud_score": fraud_probability,
        "decision": decision,
        "top_reasons": top_reasons
    }