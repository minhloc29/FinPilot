#!/bin/bash
# Initialize database and start frontend

echo "🎨 AI Finance Agent - Frontend Setup"
echo "====================================="

cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start development server
echo "✅ Starting React development server..."
echo "Frontend will be available at http://localhost:3000"
echo ""
npm run dev
