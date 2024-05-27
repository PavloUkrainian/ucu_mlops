# Flask ML Project

This project is a Flask-based web application that provides an endpoint for making predictions using a baseline machine learning model.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Docker (for containerization)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PavloUkrainian/ucu_mlops.git
   cd ucu_mlops
   
2. **Create and activate a virtual environment:**
   ```bash
    python -m venv venv
    source venv/bin/activate

3. **Install the dependencies:**
   ```bash
    pip install -r requirements.txt
   
4. **Ensure the `baseline_model.pkl` file is in the `app/models/` directory.**

## Running the Application

1. **Set the Flask app environment variable:**

   ```bash
    export FLASK_APP=run.py
   
2. **Run the Flask application:**
   ```bash
    flask run

The application should be running at http://127.0.0.1:5000.


## Running Tests

1. **Ensure you have the virtual environment activated:**

   ```bash
   source venv/bin/activate 
   ```

2. **Run the tests using pytest:**

   ```bash
   pytest
   ```

   This will discover and run all the tests in the `tests/` directory.

## Building and Running with Docker

1. **Build the Docker image:**

   ```bash
   docker build -t prediction-service .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -p 5000:5000 prediction-service
   ```

   The application should now be running at `http://127.0.0.1:5000`.

## Download and Start the Docker Image from DockerHub

1. **Open your terminal.**

2. **Pull the Docker image from Docker Hub:**

   ```bash
   docker pull pavelua/predict-service:latest
   ```

   This command pulls the `latest` version of the `predict-service` image from the Docker Hub repository `pavelua`.

3. **Run the Docker container:**

   ```bash
   docker run -d -p 80:8080 pavelua/predict-service:latest
   ```

   This command runs the container in detached mode (`-d`), mapping port 80 on your host to port 8080 in the container.

4. **Verify that the container is running:**

   ```bash
   docker ps
   ```

   This command lists all running containers. You should see `pavelua/predict-service` in the list.

## Project Configuration

Configuration for the project is handled in `config.py`:

```python
import os

class Config:
    MODEL_PATH = 'app/models/baseline_model.pkl'
```

## API Endpoints

### Predict Endpoint

- **URL:** `/predict`
- **Method:** `POST`
- **Description:** Make a prediction using the provided features.
- **Request Body:**

  ```json
  {
    "features": [42, 41, 42, 39, 42, 41, 42]
  }
  ```

- **Responses:**
  - `200 OK` with the prediction result.
  - `400 Bad Request` if the features are not provided.
  - `500 Internal Server Error` if there is an error with the prediction.
