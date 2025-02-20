import pytest

def test_homepage(test_client):
    """Test if the root URL returns a welcome message."""
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the User Management API!"}

def test_add_user(test_client):
    """Test adding a new user."""
    response = test_client.post('/users', json={"username": "testuser", "password": "testpass"},headers={"Authorization": "Basic admin:admin123"})
    assert response.status_code == 201
    assert response.json == {"message": "User added successfully!"}

def test_get_users(test_client):
    """Test retrieving all users."""
    test_client.post('/users', json={"username": "testuser2", "password": "testpass"},headers={"Authorization": "Basic admin:admin123"})
    response = test_client.get('/users', headers={"Authorization": "Basic admin:admin123"})
    assert response.status_code == 200
    assert len(response.json) > 0  # Ensure at least one user exists

def test_get_user_by_id(test_client):
    """Test retrieving a specific user by ID."""
    response = test_client.get('/users/1', headers={"Authorization": "Basic admin:admin123"})
    assert response.status_code == 200
    assert "username" in response.json  # Ensure response has username field

def test_update_user(test_client):
    """Test updating an existing user."""
    test_client.post('/users', json={"username": "updateuser", "password": "oldpass"},headers={"Authorization": "Basic admin:admin123"})
    response = test_client.put('/users/1', json={"username": "updateduser"},headers={"Authorization": "Basic admin:admin123"})
    assert response.status_code == 200
    assert response.json == {"message": "User updated successfully!"}

def test_delete_user(test_client):
    """Test deleting a user."""
    test_client.post('/users', json={"username": "deleteuser", "password": "delpass"},headers={"Authorization": "Basic admin:admin123"})
    response = test_client.delete('/users/1', headers={"Authorization": "Basic admin:admin123"})
    assert response.status_code == 200
    assert response.json == {"message": "User deleted successfully!"}
