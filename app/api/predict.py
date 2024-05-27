from flask import Blueprint, request, jsonify, current_app
import numpy as np
from ..model.model import load_model, make_prediction

bp = Blueprint('predict', __name__)

@bp.route('/predict', methods=['POST'])
def predict():
    """
       Predict PS25 Level
    ---
    tags:
      - Prediction
    summary: Predict the PS25 level based on provided features.
    description: >
      This endpoint predicts the PS25 level based on an array of numerical features.
      The features should be provided in the request body as an array of numbers.
    parameters:
      - name: body
        in: body
        required: true
        description: JSON object containing an array of numerical features for prediction.
        schema:
          type: object
          required:
            - features
          properties:
            features:
              type: array
              items:
                type: number
              description: >
                An array of numerical features used for the prediction. Each feature should be a number.
              example: [41, 42, 43, 42, 41, 43, 42]
    responses:
      200:
        description: Prediction result
        schema:
          type: object
          properties:
            ps25_level:
              type: number
              description: Predicted PS25 level.
              example: 75
      400:
        description: Bad Request - No features provided
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message indicating that no features were provided in the request.
              example: "No features provided"
      500:
        description: Internal Server Error - Model not loaded or Prediction error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message indicating an issue with the model loading or prediction process.
              example: "Model not loaded or Prediction error"
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
