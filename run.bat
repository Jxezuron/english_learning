@echo off
REM ===============================================================
REM Windows Batch Startup Script for English Learning Platform
REM ===============================================================

echo ===================================================
echo Starting English Learning Platform (Windows)
echo ===================================================

REM Check for virtual environment
if not exist "venv" (
    echo [INFO] Virtual environment not found. Creating venv...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment. Ensure Python 3 is installed.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing required dependencies...
pip install -r requirements.txt

REM Initialize and seed the database if not already present
if not exist "instance\english_learning.db" (
    echo [INFO] Initializing SQLite database and educational seed data...
    python -c "from app import create_app; from database.db import init_db, get_db; from database.seed_data import seed_all_data; app = create_app(); app.app_context().push(); init_db(app); seed_all_data(get_db()); print('Database ready.')"
)

REM Start development server
echo.
echo ===================================================
echo Platform running at: http://localhost:5000
echo Open your browser to begin learning!
echo Press CTRL+C to stop the server.
echo ===================================================
python app.py
pause
