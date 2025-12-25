from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Note
from datetime import datetime

bp = Blueprint('notes', __name__, url_prefix='/api/notes')


@bp.route('', methods=['GET'])
@login_required
def list_notes():
    """Get all notes for the current user."""
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    return jsonify({
        'notes': [note.to_dict() for note in notes]
    }), 200


@bp.route('/<int:note_id>', methods=['GET'])
@login_required
def get_note(note_id):
    """Get a specific note."""
    note = Note.query.get(note_id)
    
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Check if user owns the note
    if note.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({'note': note.to_dict()}), 200


@bp.route('', methods=['POST'])
@login_required
def create_note():
    """Create a new note."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    title = data.get('title')
    content = data.get('content', '')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    note = Note(
        title=title,
        content=content,
        user_id=current_user.id
    )
    
    db.session.add(note)
    db.session.commit()
    
    return jsonify({
        'message': 'Note created successfully',
        'note': note.to_dict()
    }), 201


@bp.route('/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    """Update an existing note."""
    note = Note.query.get(note_id)
    
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Check if user owns the note
    if note.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Note updated successfully',
        'note': note.to_dict()
    }), 200


@bp.route('/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    """Delete a note."""
    note = Note.query.get(note_id)
    
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Check if user owns the note
    if note.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(note)
    db.session.commit()
    
    return jsonify({'message': 'Note deleted successfully'}), 200


@bp.route('/search', methods=['GET'])
@login_required
def search_notes():
    """Search notes by title, content, or date range."""
    query = request.args.get('q', '')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    
    # Start with user's notes
    notes_query = Note.query.filter_by(user_id=current_user.id)
    
    # Search by title or content
    if query:
        search_filter = db.or_(
            Note.title.ilike(f'%{query}%'),
            Note.content.ilike(f'%{query}%')
        )
        notes_query = notes_query.filter(search_filter)
    
    # Filter by date range
    if from_date:
        try:
            from_datetime = datetime.fromisoformat(from_date)
            notes_query = notes_query.filter(Note.created_at >= from_datetime)
        except ValueError:
            return jsonify({'error': 'Invalid from date format'}), 400
    
    if to_date:
        try:
            to_datetime = datetime.fromisoformat(to_date)
            notes_query = notes_query.filter(Note.created_at <= to_datetime)
        except ValueError:
            return jsonify({'error': 'Invalid to date format'}), 400
    
    notes = notes_query.order_by(Note.updated_at.desc()).all()
    
    return jsonify({
        'notes': [note.to_dict() for note in notes],
        'count': len(notes)
    }), 200
