#!/bin/bash

# Awesome Notes Setup Script
# This script helps set up the development environment

set -e

echo "🚀 Awesome Notes Setup Script"
echo "=============================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Visit: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✓ Docker is installed"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

echo "✓ Docker Compose is available"

# Determine docker-compose command
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found. Please run this script from the awesome-notes directory."
    exit 1
fi

echo "✓ In correct directory"
echo ""

# Ask user if they want to use Docker or manual setup
echo "Choose setup method:"
echo "1) Docker (Recommended - Everything in containers)"
echo "2) Manual (Local Python and Node.js)"
read -p "Enter choice [1-2]: " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "🐳 Starting Docker setup..."
    echo ""
    
    # Build and start containers
    echo "Building containers (this may take a few minutes)..."
    $DOCKER_COMPOSE build
    
    echo ""
    echo "Starting services..."
    $DOCKER_COMPOSE up -d
    
    # Wait for services to be ready
    echo ""
    echo "Waiting for services to be ready..."
    sleep 10
    
    # Initialize database
    echo ""
    echo "Initializing database with sample data..."
    $DOCKER_COMPOSE exec backend python init_db.py
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "🌐 Application URLs:"
    echo "   Frontend: http://localhost:4200"
    echo "   Backend:  http://localhost:5000"
    echo ""
    echo "👤 Test Credentials:"
    echo "   Admin: admin@example.com / admin123"
    echo "   User:  user@example.com / user123"
    echo ""
    echo "📝 Useful commands:"
    echo "   View logs:        $DOCKER_COMPOSE logs -f"
    echo "   Stop services:    $DOCKER_COMPOSE down"
    echo "   Restart services: $DOCKER_COMPOSE restart"
    echo ""
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "🔧 Manual setup selected..."
    echo ""
    
    # Check for Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
        exit 1
    fi
    echo "✓ Python is installed"
    
    # Check for Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
        exit 1
    fi
    echo "✓ Node.js is installed"
    
    # Check for PostgreSQL
    if ! command -v psql &> /dev/null; then
        echo "⚠️  PostgreSQL client not found. Make sure PostgreSQL is installed and running."
    fi
    
    echo ""
    echo "Setting up backend..."
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo "✓ Created virtual environment"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    echo "✓ Installed Python dependencies"
    
    # Copy environment file
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo "✓ Created .env file"
        echo "⚠️  Please edit backend/.env with your database connection string"
    fi
    
    cd ..
    
    echo ""
    echo "Setting up frontend..."
    cd frontend
    
    # Install dependencies
    npm install
    echo "✓ Installed Node.js dependencies"
    
    cd ..
    
    echo ""
    echo "✅ Manual setup complete!"
    echo ""
    echo "📝 Next steps:"
    echo "1. Edit backend/.env with your PostgreSQL connection"
    echo "2. Initialize the database:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   python init_db.py"
    echo ""
    echo "3. Start the backend:"
    echo "   python run.py"
    echo ""
    echo "4. In a new terminal, start the frontend:"
    echo "   cd frontend"
    echo "   ng serve"
    echo ""
else
    echo "Invalid choice. Exiting."
    exit 1
fi
