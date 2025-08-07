#!/bin/bash

echo "🎯 Starting SnapStack Admin Dashboard"
echo "======================================"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd apps/backend
pip3 install flask flask-cors --quiet 2>/dev/null || pip install flask flask-cors --quiet 2>/dev/null
cd ../..

# Install web app dependencies
echo "📦 Installing React dependencies..."
cd apps/web
npm install --silent
cd ../..

# Start services
echo ""
echo "🚀 Starting services..."
echo ""

# Start backend
echo "✅ Starting Flask backend on http://localhost:5000"
cd apps/backend && python3 app.py &
BACKEND_PID=$!
cd ../..

# Wait for backend to start
sleep 2

# Start frontend
echo "✅ Starting React admin on http://localhost:5173"
cd apps/web && npm run dev &
FRONTEND_PID=$!
cd ../..

echo ""
echo "======================================"
echo "✨ Admin Dashboard is running!"
echo ""
echo "🎯 Admin Dashboard: http://localhost:5173/admin"
echo "📊 Dashboard: http://localhost:5173/admin"
echo "🔬 Parser Studio: http://localhost:5173/admin/parser"
echo "🔧 Backend API: http://localhost:5000/api/admin"
echo ""
echo "Press Ctrl+C to stop all services"
echo "======================================"

# Wait and handle shutdown
trap "echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait