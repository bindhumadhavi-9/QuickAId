#!/bin/bash

# QuickAid - Full Stack Application Runner
# This script starts both the Python backend and React frontend

echo "Starting QuickAid Application..."

# Check if Python and pip are installed
if command -v python3 &> /dev/null; then
    echo "Python3 found!"
else
    echo "Error: Python3 is not installed"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --break-system-packages flask flask-cors 2>/dev/null || pip3 install flask flask-cors

# Start Python backend in background
echo "Starting Python Flask backend on port 3001..."
cd backend
PORT=3001 python3 app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 2

# Check if npm is installed
if command -v npm &> /dev/null; then
    echo "npm found!"
else
    echo "Error: npm is not installed"
    kill $BACKEND_PID
    exit 1
fi

# Install npm dependencies
echo "Installing npm dependencies..."
npm install

# Build the React app
echo "Building React application..."
npm run build

echo ""
echo "=========================================="
echo "QuickAid is ready!"
echo "=========================================="
echo ""
echo "Backend API running at: http://localhost:3001"
echo "Frontend built at: dist/index.html"
echo ""
echo "To run development server: npm run dev"
echo "To preview production build: npm run preview"
echo ""
echo "Press Ctrl+C to stop the backend server"
echo ""

# Wait for backend process
wait $BACKEND_PID
