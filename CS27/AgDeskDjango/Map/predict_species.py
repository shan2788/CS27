import joblib
import numpy as np

model = joblib.load("rf_model.pkl")
encoder = joblib.load("label_encoder.pkl")

feature_order = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']

def predict_crop(input_features: dict) -> str:
    try:
        values = np.array([input_features[k] for k in feature_order]).reshape(1, -1)
        pred = model.predict(values)
        crop = encoder.inverse_transform(pred)[0]
        return crop
    except Exception as e:
        return f"Prediction error: {str(e)}"
