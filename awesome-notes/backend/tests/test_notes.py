import pytest
from app.models import Note


def test_create_note(client, auth_user):
    """Test creating a note."""
    # Login first
    client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    response = client.post('/api/notes', json={
        'title': 'Test Note',
        'content': '# This is a test note\n\nWith markdown content.'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Note created successfully'
    assert data['note']['title'] == 'Test Note'
    assert '# This is a test note' in data['note']['content']


def test_list_notes(client, auth_user, app):
    """Test listing notes."""
    # Login first
    client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    # Create a note
    with app.app_context():
        from app import db
        note = Note(title='Test Note', content='Content', user_id=auth_user.id)
        db.session.add(note)
        db.session.commit()
    
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['notes']) >= 1


def test_search_notes(client, auth_user, app):
    """Test searching notes."""
    # Login first
    client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    # Create notes
    with app.app_context():
        from app import db
        note1 = Note(title='Python Tutorial', content='Learn Python', user_id=auth_user.id)
        note2 = Note(title='JavaScript Guide', content='Learn JS', user_id=auth_user.id)
        db.session.add(note1)
        db.session.add(note2)
        db.session.commit()
    
    # Search for Python
    response = client.get('/api/notes/search?q=Python')
    assert response.status_code == 200
    data = response.get_json()
    assert data['count'] >= 1
    assert any('Python' in note['title'] for note in data['notes'])
