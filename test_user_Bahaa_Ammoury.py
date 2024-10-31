import pytest
import json
from app import app, create_db_table, insert_user, get_user_by_id, update_user, delete_user

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Create database table before tests
    with app.app_context():
        create_db_table()

    yield client

# Test case for getting all users
def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)  # Check if the response is a list

# Test case for inserting a user
def test_insert_user(client):
    user = {
        "name": "Alice",
        "email": "alice@example.com",
        "phone": "123456789",
        "address": "123 Wonderland",
        "country": "Wonderland"
    }
    response = client.post('/api/users/add', data=json.dumps(user), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == user['name']
    assert data['email'] == user['email']

# Test case for getting user by id
def test_get_user_by_id(client):
    response = client.get('/api/users/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'user_id' in data  # Check if the user exists

# Test case for updating a user
def test_update_user(client):
    updated_user = {
        "user_id": 1,
        "name": "Alice Updated",
        "email": "alice.updated@example.com",
        "phone": "987654321",
        "address": "321 Wonderland",
        "country": "Wonderland"
    }
    response = client.put('/api/users/update', data=json.dumps(updated_user), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == updated_user['name']
    assert data['email'] == updated_user['email']

# Test case for deleting a user
def test_delete_user(client):
    response = client.delete('/api/users/delete/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'User deleted successfully'
