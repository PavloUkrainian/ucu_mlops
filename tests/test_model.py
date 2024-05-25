from app.model.model import load_model, make_prediction
import numpy as np

def test_load_model(app):
    with app.app_context():
        model = load_model()
        assert model is not None

def test_make_prediction(app):
    with app.app_context():
        model = load_model()
        data = np.array([1.0, 2.0, 3.0, 4.0]).reshape(1, -1)
        prediction = make_prediction(model, data)
        assert isinstance(prediction, list)
