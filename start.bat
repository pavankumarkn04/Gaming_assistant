@echo off
echo ============================================
echo   PAV1 AI Gaming Assistant - Starting
echo ============================================

cd /d "%~dp0backend"
call venv\Scripts\activate.bat

echo.
echo Starting PAV1 AI server on http://localhost:8000
echo Open your browser at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop.
echo.

python main.py
