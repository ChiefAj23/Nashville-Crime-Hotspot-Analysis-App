#!/bin/bash
# Start FastAPI Backend Server

echo "🚀 Starting Nashville Safe Tourist Guide Backend Server..."
echo ""

cd backend

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
pip install -r requirements.txt --quiet

# Start server
echo ""
echo "✅ Starting server on http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py

