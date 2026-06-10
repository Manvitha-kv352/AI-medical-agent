#!/bin/bash

# Medical Research Agent - Setup Script
# This script automates the setup of both frontend and backend

set -e

echo "🏥 Medical Research Agent - Setup Script"
echo "========================================"
echo ""

# Check Node.js installation
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js v14+"
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check npm installation
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ npm version: $(npm --version)"
echo ""

# Setup Backend
echo "📦 Setting up Backend..."
cd backend

if [ ! -f ".env" ]; then
    echo "   Creating .env file from template..."
    cp .env.example .env
fi

echo "   Installing dependencies..."
npm install

echo "✅ Backend setup complete!"
echo ""

# Setup Frontend
echo "📦 Setting up Frontend..."
cd ../frontend

if [ ! -f ".env" ]; then
    echo "   Creating .env file from template..."
    cp .env.example .env
fi

echo "   Installing dependencies..."
npm install

echo "✅ Frontend setup complete!"
echo ""

cd ..

echo "========================================"
echo "✨ Setup Complete!"
echo "========================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Start the Backend (in Terminal 1):"
echo "   cd backend"
echo "   npm run dev"
echo ""
echo "2. Start the Frontend (in Terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open your browser to http://localhost:3000"
echo ""
echo "For more information, see QUICK_START.md"
echo ""
