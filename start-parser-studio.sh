#!/bin/bash

echo "🚀 Starting SnapStack Parser Studio"
echo "=================================="
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd apps/backend
pip3 install flask flask-cors --quiet 2>/dev/null || pip install flask flask-cors --quiet 2>/dev/null
cd ../..

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node dependencies..."
    npm install
fi

# Install web app dependencies
echo "📦 Installing web app dependencies..."
cd apps/web
npm install --silent
cd ../..

# Start services
echo ""
echo "🎯 Starting services..."
echo ""

# Start backend
echo "✅ Starting Flask backend on http://localhost:5000"
cd apps/backend && python3 app.py &
BACKEND_PID=$!
cd ../..

# Wait for backend to start
sleep 2

# Start frontend
echo "✅ Starting React frontend on http://localhost:5173"
cd apps/web && npm run dev &
FRONTEND_PID=$!
cd ../..

echo ""
echo "=================================="
echo "✨ Parser Studio is running!"
echo ""
echo "📝 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=================================="

# Wait and handle shutdown
trap "echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait