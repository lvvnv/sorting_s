#!/bin/bash
# ci-validate.sh
# Script to validate CI setup locally

echo "Validating CI setup locally..."

# Check if we're in the right directory
if [ ! -d "sorting_system" ] || [ ! -d "frontend" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

echo "✓ Project directory structure verified"

# Test backend setup
echo "Testing backend setup..."
cd sorting_system

# Check Python availability
if ! command -v python &> /dev/null; then
    echo "Error: Python not found"
    exit 1
fi

echo "✓ Python available"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

echo "✓ requirements.txt found"

# Test Django setup
if ! python -c "import django" &> /dev/null; then
    echo "Warning: Django not installed. Please install dependencies."
else
    echo "✓ Django available"
fi

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found"
    exit 1
fi

echo "✓ manage.py found"

# Try to run Django check
if python manage.py check &> /dev/null; then
    echo "✓ Django configuration valid"
else
    echo "Warning: Django configuration check failed"
fi

echo "Backend validation completed."

# Test frontend setup
echo "Testing frontend setup..."
cd ../frontend

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found"
    exit 1
fi

echo "✓ package.json found"

# Check Node.js availability
if ! command -v node &> /dev/null; then
    echo "Warning: Node.js not found. Frontend tests will not run."
else
    echo "✓ Node.js available"
    
    # Check if node_modules exists
    if [ -d "node_modules" ]; then
        echo "✓ node_modules directory found"
    else
        echo "Info: node_modules not found. Run 'npm install' to install dependencies."
    fi
fi

echo "Frontend validation completed."

cd ..

echo "CI validation completed successfully!"
echo ""
echo "To run the full CI pipeline locally:"
echo "1. Backend tests: cd sorting_system && python manage.py test"
echo "2. Frontend tests: cd frontend && npm test"
echo ""
echo "For GitHub Actions, push your changes to trigger the CI pipeline."