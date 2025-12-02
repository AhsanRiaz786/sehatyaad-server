#!/bin/bash

# SehatYaad Backend Start Script

cd "$(dirname "$0")"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run ./setup.sh first."
    exit 1
fi

echo "🚀 Starting SehatYaad Backend..."
python app.py
