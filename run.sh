#!/usr/bin/env bash
# ===============================================================
# Linux / macOS Bash Startup Script for English Learning Platform
# ===============================================================

set -e

cd "$(dirname "$0")"

echo "==================================================="
echo "Starting English Learning Platform"
echo "==================================================="

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv || python -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Install requirements
pip install -r requirements.txt

# Initialize database
if [ ! -f "instance/english_learning.db" ]; then
    echo "[INFO] Initializing and seeding educational database..."
    python3 -c "from app import create_app; from database.db import init_db, get_db; from database.seed_data import seed_all_data; app = create_app(); app.app_context().push(); init_db(app); seed_all_data(get_db()); print('Database initialized.')"
fi

echo ""
echo "==================================================="
echo "Application running at: http://localhost:5000"
echo "Press Ctrl+C to stop the server."
echo "==================================================="
python3 app.py
