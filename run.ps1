# ===============================================================
# Windows PowerShell Startup Script for English Learning Platform
# ===============================================================

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Starting English Learning Platform (PowerShell)" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# Check for virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "[INFO] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "[INFO] Verifying packages..." -ForegroundColor Yellow
pip install -r requirements.txt

# Initialize database if needed
if (-not (Test-Path "instance\english_learning.db")) {
    Write-Host "[INFO] Initializing and seeding educational content..." -ForegroundColor Yellow
    python -c "from app import create_app; from database.db import init_db, get_db; from database.seed_data import seed_all_data; app = create_app(); app.app_context().push(); init_db(app); seed_all_data(get_db()); print('Database ready.')"
}

Write-Host "`n===================================================" -ForegroundColor Green
Write-Host "Platform is live at: http://localhost:5000" -ForegroundColor Green
Write-Host "Press CTRL+C in this terminal to shut down." -ForegroundColor Green
Write-Host "===================================================`n" -ForegroundColor Green

python app.py
