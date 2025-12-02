#!/bin/bash

# SehatYaad Backend Setup Script

echo "🚀 SehatYaad Backend Setup"
echo "=========================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Please edit backend/.env and add your GEMINI_API_KEY"
    echo ""
    read -p "Press Enter to continue after adding your API key..."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the backend server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Or simply run:"
echo "  cd backend && ./start.sh"
