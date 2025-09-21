#!/bin/bash

# Setup script for CV Enhancer project

echo "Setting up CV Enhancer project..."

# Change to web-app directory
cd "$(dirname "$0")"

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Make Python script executable
chmod +x scripts/extract_text.py

echo "Setup complete!"
echo ""
echo "To start the development server:"
echo "  cd web-app && npm run dev"
echo ""
echo "The application will be available at http://localhost:3000"
