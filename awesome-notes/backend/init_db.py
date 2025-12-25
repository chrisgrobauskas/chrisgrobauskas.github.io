#!/usr/bin/env python3
"""Initialize the database with sample data for development."""

import os
import sys

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Note


def init_db():
    """Initialize database with sample data."""
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user already exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print('✓ Created admin user (admin@example.com / admin123)')
        else:
            print('✓ Admin user already exists')
        
        # Check if regular user exists
        user = User.query.filter_by(email='user@example.com').first()
        if not user:
            # Create regular user
            user = User(
                username='user',
                email='user@example.com',
                role='user'
            )
            user.set_password('user123')
            db.session.add(user)
            print('✓ Created regular user (user@example.com / user123)')
        else:
            print('✓ Regular user already exists')
        
        db.session.commit()
        
        # Create sample notes for admin
        if Note.query.filter_by(user_id=admin.id).count() == 0:
            sample_notes = [
                {
                    'title': 'Welcome to Awesome Notes!',
                    'content': '''# Welcome to Awesome Notes

This is a sample note to help you get started.

## Features

- **Markdown Support**: Write notes in markdown format
- **Live Preview**: See your formatted content as you type
- **Search**: Quickly find notes by title or content
- **Secure**: Your notes are encrypted and secure

## Getting Started

1. Create a new note using the "New Note" button
2. Write your content using markdown syntax
3. Click "Save" to save your note
4. Use the search bar to find your notes

Enjoy taking notes!'''
                },
                {
                    'title': 'Markdown Cheat Sheet',
                    'content': '''# Markdown Cheat Sheet

## Headers
# H1
## H2
### H3

## Emphasis
*italic* or _italic_
**bold** or __bold__
***bold and italic***

## Lists
- Unordered list item
- Another item
  - Nested item

1. Ordered list item
2. Another item

## Links and Images
[Link text](https://example.com)
![Alt text](https://example.com/image.jpg)

## Code
Inline `code` with backticks

```python
def hello():
    print("Hello, World!")
```

## Blockquotes
> This is a blockquote
> It can span multiple lines

## Tables
| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |'''
                }
            ]
            
            for note_data in sample_notes:
                note = Note(
                    title=note_data['title'],
                    content=note_data['content'],
                    user_id=admin.id
                )
                db.session.add(note)
            
            db.session.commit()
            print(f'✓ Created {len(sample_notes)} sample notes for admin')
        else:
            print('✓ Sample notes already exist')
        
        print('\n✅ Database initialization complete!')
        print('\nTest Credentials:')
        print('  Admin: admin@example.com / admin123')
        print('  User:  user@example.com / user123')


if __name__ == '__main__':
    init_db()
