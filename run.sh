#!/bin/bash

# Quick Aid - Smart First Aid & Emergency Care System
# Unified Startup Script

echo "================================================"
echo "Quick Aid - Smart First Aid & Emergency Care"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --break-system-packages flask flask-cors 2>/dev/null || pip3 install flask flask-cors

# Check npm
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed"
    exit 1
fi

# Install npm dependencies and build
echo "Building React frontend..."
npm install
npm run build

echo ""
echo "================================================"
echo "Starting Quick Aid Application..."
echo "================================================"
echo ""

# Start the unified Flask app
PORT=3000 python3 app.py
