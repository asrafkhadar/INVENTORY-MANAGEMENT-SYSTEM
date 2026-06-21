# Run Project Script
# This script sets up and runs the Inventory Management System

Write-Host 'Starting Inventory Management System...' -ForegroundColor Green

# Navigate to project directory
Set-Location 'c:\Users\asraf\Desktop\IMS\IMS'

# Check if virtual environment exists
if (!(Test-Path .\.venv)) {
    Write-Host 'Creating virtual environment...' -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host 'Activating virtual environment...' -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Install/update dependencies
Write-Host 'Installing dependencies...' -ForegroundColor Yellow
pip install -r backend\requirements.txt

# Navigate to backend
Set-Location backend

# Run migrations
Write-Host 'Running database migrations...' -ForegroundColor Yellow
python manage.py migrate

# Create admin user if not exists
Write-Host 'Setting up admin user...' -ForegroundColor Yellow
python setup_admin.py

# Populate data
Write-Host 'Populating sample data...' -ForegroundColor Yellow
python populate_large_dataset.py

# Fix sales data
Write-Host 'Fixing sales analytics...' -ForegroundColor Yellow
python fix_sales_data.py

# Run tests
Write-Host 'Running tests...' -ForegroundColor Yellow
python manage.py test

# Start server
Write-Host 'Starting Django server...' -ForegroundColor Green
Write-Host 'Access at: http://localhost:8000/login.html' -ForegroundColor Cyan
Write-Host '   Username: admin' -ForegroundColor Cyan
Write-Host '   Password: admin' -ForegroundColor Cyan
Write-Host '' -ForegroundColor Cyan
Write-Host 'Server is starting in background...' -ForegroundColor Yellow

Start-Process -FilePath "python" -ArgumentList "manage.py", "runserver" -NoNewWindow

Write-Host 'Server started! Check http://localhost:8000' -ForegroundColor Green