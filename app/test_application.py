import pytest
from application import application
import json

value = 0

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
