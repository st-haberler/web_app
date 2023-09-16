import os
import tempfile
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_upload(client):
    # Use a test CSV file here
    data = {
        'file': (open('test.csv', 'rb'), 'test.csv')
    }

    rv = client.post('/upload', content_type='multipart/form-data', data=data)

    assert b'File is being processed.' in rv.data
