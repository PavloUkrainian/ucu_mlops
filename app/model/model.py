import pickle
from flask import current_app

def load_model():
    model_path = current_app.config['MODEL_PATH']
    current_app.logger.info(f"Attempting to load model from: {model_path}")
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        current_app.logger.error(f"Error loading model: {e}")
        return None

def make_prediction(model, features):
    try:
        prediction = model.predict(features)
        return prediction.tolist()
    except Exception as e:
        current_app.logger.error(f"Error during prediction: {e}")
        return None
