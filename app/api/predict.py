from flask import Blueprint, request, jsonify, current_app
import numpy as np
from ..model.model import load_model, make_prediction

bp = Blueprint('predict', __name__)

@bp.route('/predict', methods=['POST'])
def predict():
    """
    Predict PS25 level
    ---
    tags:
      - Prediction
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - features
          properties:
            features:
              type: array
              items:
                type: number
              example: [1.0, 2.0, 3.0, 4.0]
    responses:
      200:
        description: Prediction result
        schema:
          type: object
          properties:
            ps25_level:
              type: number
      400:
        description: No features provided
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Model not loaded or Prediction error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    model = load_model()
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json(force=True)
        features = data.get('features')

        if features is None:
            return jsonify({'error': 'No features provided'}), 400

        features = np.array(features).reshape(1, -1)
        prediction = make_prediction(model, features)

        if prediction is None:
            return jsonify({'error': 'Prediction error'}), 500

        return jsonify({'ps25_level': prediction[0]})

    except Exception as e:
        current_app.logger.error(f"Error during prediction: {e}")
        return jsonify({'error': 'Prediction error'}), 500
