#!/bin/bash

# AQA Home Task Setup Script
echo "🚀 Setting up AQA Home Task Test Frameworks"
echo "=============================================="

# Function to setup a framework
setup_framework() {
    local framework_name=$1
    local framework_path=$2
    
    echo ""
    echo "📁 Setting up $framework_name..."
    echo "--------------------------------"
    
    cd "$framework_path"
    
    # Create virtual environment
    echo "Creating virtual environment..."
    python -m venv venv
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    # Create necessary directories
    echo "Creating directories..."
    mkdir -p reports screenshots allure-results
    
    echo "✅ $framework_name setup complete!"
    
    cd ..
}

# Setup API Framework
setup_framework "API Framework" "api_framework"

# Setup Selenium Framework
setup_framework "Selenium Framework" "selenium_framework"

echo ""
echo "🎉 All frameworks setup complete!"
echo ""
echo "📋 To run tests:"
echo "   API Framework:"
echo "   cd api_framework && source venv/bin/activate && python run_tests.py"
echo ""
echo "   Selenium Framework:"
echo "   cd selenium_framework && source venv/bin/activate && python run_tests.py"
echo ""
echo "📖 For more options, see the README files in each framework directory."
