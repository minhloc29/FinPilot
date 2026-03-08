#!/bin/bash
# Initialize database and start backend server

echo "🚀 AI Finance Agent - Backend Setup"
echo "===================================="

cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python -c "from app.db.init_db import init_db; init_db()"

# Start server
echo "✅ Starting FastAPI server..."
echo "Server will be available at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
