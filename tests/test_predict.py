import json

def test_predict(client):
    data = {
        "features": [42, 42, 42, 42, 42, 42, 42]
    }
    response = client.post("/predict", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert "ps25_level" in response.json
