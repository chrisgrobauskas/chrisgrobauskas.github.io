# Contributing to Awesome Notes

Thank you for your interest in contributing to Awesome Notes! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project follows a code of conduct that all contributors are expected to adhere to:
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect differing viewpoints

## Getting Started

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/chrisgrobauskas.github.io.git
   cd chrisgrobauskas.github.io/awesome-notes
   ```

2. **Set up remote**
   ```bash
   git remote add upstream https://github.com/chrisgrobauskas/chrisgrobauskas.github.io.git
   ```

3. **Start development environment**
   ```bash
   docker-compose up --build
   ```

### Development Tools

**Backend:**
- Python 3.9+
- Flask
- PostgreSQL
- pytest for testing
- black for formatting
- flake8 for linting

**Frontend:**
- Node.js 18+
- Angular 17
- TypeScript
- Jasmine/Karma for testing

## Development Workflow

### Creating a New Feature

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd frontend
   npm test
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Describe your changes
   - Link related issues

### Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(backend): Add note tagging functionality
fix(frontend): Fix markdown preview not updating
docs(readme): Update installation instructions
test(backend): Add tests for user authentication
```

## Code Style Guidelines

### Python (Backend)

**Follow PEP 8 with these specifics:**
- Line length: 100 characters
- Use black for formatting
- Use flake8 for linting

**Example:**
```python
def create_note(user_id: int, title: str, content: str) -> Note:
    """Create a new note for a user.
    
    Args:
        user_id: The ID of the user creating the note
        title: The note title
        content: The note content in markdown
        
    Returns:
        The created Note object
    """
    note = Note(user_id=user_id, title=title, content=content)
    db.session.add(note)
    db.session.commit()
    return note
```

**Formatting:**
```bash
# Format code
black app tests

# Check linting
flake8 app tests
```

### TypeScript (Frontend)

**Follow Angular style guide:**
- Use TypeScript strict mode
- 2 spaces for indentation
- Semicolons required
- Single quotes for strings

**Example:**
```typescript
export class NotesService {
  constructor(private http: HttpClient) {}

  getNotes(): Observable<Note[]> {
    return this.http.get<Note[]>(`${this.apiUrl}/notes`);
  }
}
```

**Linting:**
```bash
# Check linting
ng lint
```

### Database Models

- Use descriptive model names
- Add indexes for frequently queried fields
- Include timestamps (created_at, updated_at)
- Add proper relationships and constraints

### API Design

- Use RESTful conventions
- Version APIs when breaking changes occur
- Return appropriate HTTP status codes
- Include error messages in responses

## Testing Guidelines

### Backend Testing

**Test Structure:**
```python
def test_create_note(client, auth_user):
    """Test creating a new note."""
    # Arrange
    client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    # Act
    response = client.post('/api/notes', json={
        'title': 'Test Note',
        'content': 'Test content'
    })
    
    # Assert
    assert response.status_code == 201
    assert response.json['note']['title'] == 'Test Note'
```

**Running Tests:**
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_notes.py

# Run specific test
pytest tests/test_notes.py::test_create_note
```

### Frontend Testing

**Component Test Example:**
```typescript
describe('LoginComponent', () => {
  it('should login successfully', () => {
    // Arrange
    component.credentials = {
      email: 'test@example.com',
      password: 'password'
    };
    
    // Act
    component.onSubmit();
    
    // Assert
    expect(authService.login).toHaveBeenCalled();
  });
});
```

**Running Tests:**
```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## Submitting Changes

### Pull Request Process

1. **Update your branch with latest upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Ensure all tests pass**
   ```bash
   # Backend
   cd backend && pytest
   
   # Frontend
   cd frontend && npm test
   ```

3. **Create descriptive PR**
   - Clear title and description
   - Reference related issues
   - Include screenshots for UI changes
   - List breaking changes if any

4. **Respond to feedback**
   - Address reviewer comments
   - Make requested changes
   - Keep discussion constructive

### PR Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow convention
- [ ] Branch is up to date with main

## Areas for Contribution

### Easy Issues (Good First Issues)
- Documentation improvements
- UI/UX enhancements
- Adding tests
- Bug fixes

### Medium Issues
- New features
- Performance improvements
- Refactoring

### Advanced Issues
- Architecture changes
- Security enhancements
- DevOps improvements

## Development Tips

### Backend Development

**Hot Reloading:**
```bash
# Flask automatically reloads on code changes
export FLASK_ENV=development
python run.py
```

**Database Console:**
```bash
flask shell
>>> from app import db
>>> from app.models import User, Note
>>> users = User.query.all()
```

### Frontend Development

**Hot Reloading:**
```bash
# Angular CLI watches for changes
ng serve
```

**Component Generation:**
```bash
ng generate component components/my-component
ng generate service services/my-service
```

### Debugging

**Backend:**
```python
import pdb; pdb.set_trace()  # Add breakpoint
```

**Frontend:**
```typescript
console.log('Debug info:', variable);
debugger;  // Browser debugpoint
```

## Questions?

- Open an issue for questions
- Join discussions in pull requests
- Review existing documentation

## License

By contributing, you agree that your contributions will be licensed under the project's license.

Thank you for contributing to Awesome Notes! 🎉
