import pytest
from application import application
import json
import time


@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.content_type

def test_click_route(client):
    """Test the click endpoint."""
    response = client.post('/click')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'Increment queued'

def test_get_counter_route(client):
    """Test the counter retrieval endpoint."""
    response = client.get('/counter')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    #  checked with the numbers locally but later on changed it to 0 as previous tests clicks everytime so number had to be increases constantly.
    assert data['counter'] != 0

def test_unsupported_method(client):
    """Test application response to an unsupported HTTP method."""
    response = client.put('/click')
    assert response.status_code == 405 


def test_multiple_clicks(client):
    """Test multiple clicks to see if counter increments correctly."""
    response = client.get('/counter')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    old_value = data['counter']
    
    for _ in range(5):
        response = client.post('/click')
        assert response.status_code == 200
    time.sleep(5)
    counter_response = client.get('/counter')
    counter_data = json.loads(counter_response.data.decode('utf-8'))
    assert counter_data['counter'] >= old_value + 5
