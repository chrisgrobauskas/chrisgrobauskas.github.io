# Awesome Notes

A secure, full-stack note-taking application with markdown support.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [API Documentation](#api-documentation)
- [Testing](#testing)

## Overview

Awesome Notes is a modern, secure note-taking application that allows users to create, edit, and search notes with markdown support. The application features user authentication, role-based access control, and a responsive web interface.

### Features

- **User Authentication**: Secure login with bcrypt password hashing
- **Role-Based Access**: Admin and user roles with appropriate permissions
- **Markdown Support**: Rich text editing with live preview
- **Search Functionality**: Search notes by title, content, and dates
- **Responsive UI**: Angular-based single-page application
- **Cloud-Ready**: Deployable to AWS Lambda and CloudFront

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: Flask-Login with bcrypt
- **Testing**: pytest
- **Linting**: black, flake8
- **Deployment**: AWS Lambda (via Zappa)

### Frontend
- **Framework**: Angular
- **Deployment**: AWS CloudFront + S3

### DevOps
- **Containerization**: Docker, docker-compose
- **CI/CD**: GitHub Actions
- **Cloud Platform**: AWS

## Project Structure

```
awesome-notes/
├── backend/                 # Flask backend application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── utils/          # Helper functions
│   ├── migrations/         # Alembic migrations
│   ├── tests/              # pytest tests
│   ├── requirements.txt    # Python dependencies
│   ├── config.py           # Configuration
│   ├── Dockerfile          # Backend Docker image
│   └── zappa_settings.json # AWS Lambda config
├── frontend/               # Angular frontend application
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/ # Angular components
│   │   │   ├── services/   # API services
│   │   │   ├── guards/     # Route guards
│   │   │   └── models/     # TypeScript models
│   │   ├── assets/         # Static assets
│   │   └── environments/   # Environment configs
│   ├── Dockerfile          # Frontend Docker image
│   └── package.json        # Node dependencies
├── docker-compose.yml      # Local development orchestration
└── README.md              # This file
```

## Local Development

### Prerequisites

- Docker and docker-compose
- Python 3.9+ (for local development without Docker)
- Node.js 16+ and npm (for local development without Docker)
- PostgreSQL (for local development without Docker)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/chrisgrobauskas/chrisgrobauskas.github.io.git
   cd chrisgrobauskas.github.io/awesome-notes
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - PostgreSQL database on port 5432
   - Flask backend on port 5000
   - Angular frontend on port 4200

3. **Access the application**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:5000
   - API Docs: http://localhost:5000/api/docs

4. **Stop services**
   ```bash
   docker-compose down
   ```

### Manual Setup (Without Docker)

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   flask db upgrade
   ```

6. **Run the development server**
   ```bash
   flask run
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment**
   ```bash
   cp src/environments/environment.example.ts src/environments/environment.ts
   # Edit environment.ts with your configuration
   ```

4. **Run the development server**
   ```bash
   ng serve
   ```

## Production Deployment

### Backend (AWS Lambda)

1. **Configure Zappa**
   ```bash
   cd backend
   cp zappa_settings.example.json zappa_settings.json
   # Edit zappa_settings.json with your AWS configuration
   ```

2. **Deploy**
   ```bash
   zappa deploy production
   ```

3. **Update**
   ```bash
   zappa update production
   ```

### Frontend (AWS S3 + CloudFront)

1. **Build production bundle**
   ```bash
   cd frontend
   npm run build -- --configuration production
   ```

2. **Deploy to S3**
   ```bash
   aws s3 sync dist/awesome-notes s3://your-bucket-name --delete
   ```

3. **Invalidate CloudFront cache**
   ```bash
   aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
   ```

### CI/CD with GitHub Actions

The project includes GitHub Actions workflows for automated testing and deployment:

- **Backend CI**: Runs tests and linting on every push
- **Frontend CI**: Runs tests and linting on every push
- **Backend CD**: Deploys to AWS Lambda on merge to main
- **Frontend CD**: Deploys to S3/CloudFront on merge to main

## API Documentation

### Authentication

#### Register
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "username": "johndoe"
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Logout
```
POST /api/auth/logout
```

### Notes

#### List Notes
```
GET /api/notes
```

#### Get Note
```
GET /api/notes/:id
```

#### Create Note
```
POST /api/notes
Content-Type: application/json

{
  "title": "My Note",
  "content": "# Markdown content\n\nThis is a note."
}
```

#### Update Note
```
PUT /api/notes/:id
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

#### Delete Note
```
DELETE /api/notes/:id
```

#### Search Notes
```
GET /api/notes/search?q=search+term&from=2024-01-01&to=2024-12-31
```

### Users (Admin Only)

#### List Users
```
GET /api/users
```

#### Get User
```
GET /api/users/:id
```

#### Update User
```
PUT /api/users/:id
Content-Type: application/json

{
  "email": "newemail@example.com",
  "role": "admin"
}
```

#### Delete User
```
DELETE /api/users/:id
```

## Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage  # With coverage
```

### Linting

#### Backend
```bash
cd backend
black .
flake8 app tests
```

#### Frontend
```bash
cd frontend
ng lint
```

## Environment Variables

### Backend (.env)

```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/awesome_notes
JWT_SECRET_KEY=your-jwt-secret
```

### Frontend (environment.ts)

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5000/api'
};
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.
