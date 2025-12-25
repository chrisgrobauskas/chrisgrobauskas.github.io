import pytest
from app.models import User


def test_register(client):
    """Test user registration."""
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User registered successfully'
    assert data['user']['username'] == 'newuser'
    assert data['user']['email'] == 'newuser@example.com'


def test_register_duplicate_email(client, auth_user):
    """Test registration with duplicate email."""
    response = client.post('/api/auth/register', json={
        'username': 'anotheruser',
        'email': 'test@example.com',  # Duplicate email
        'password': 'password123'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'already registered' in data['error']


def test_login(client, auth_user):
    """Test user login."""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful'
    assert data['user']['email'] == 'test@example.com'


def test_login_invalid_credentials(client, auth_user):
    """Test login with invalid credentials."""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'Invalid' in data['error']


def test_logout(client, auth_user):
    """Test user logout."""
    # First login
    client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    # Then logout
    response = client.post('/api/auth/logout')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Logout successful'
