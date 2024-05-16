
import os
import pytest
import logging
import json
from src.main import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_production_plan_returns_correct_format(client):
    payload_path = os.path.join(os.path.dirname(__file__), '..', 'example_payloads', 'payload3.json')

    with open(payload_path, 'r') as file:
        payload = json.load(file)

    response = client.post('/productionplan', json=payload)
    logger.info(f"Response: {response.get_json()}")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all('name' in plant and 'p' in plant for plant in data)


def test_production_plan_golden(client):
    payload_path = os.path.join(os.path.dirname(__file__), '..', 'example_payloads', 'payload3.json')
    expected_response_path = os.path.join(os.path.dirname(__file__), '..', 'example_payloads', 'response3.json')

    with open(payload_path, 'r') as file:
        payload = json.load(file)

    with open(expected_response_path, 'r') as file:
        expected_response = json.load(file)

    response = client.post('/productionplan', json=payload)
    assert response.status_code == 200

    actual_response = response.get_json()

    print("Actual Response Data:", actual_response)

    assert actual_response == expected_response


if __name__ == '__main__':
    pass
