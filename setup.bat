@echo off
echo ============================================
echo   STAN AI Gaming Assistant - Setup
echo ============================================

cd /d "%~dp0backend"

echo.
echo [1/4] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo [3/4] Setting up .env file...
if not exist .env (
    copy .env.example .env
    echo Created .env file — EDIT IT with your API keys before running!
) else (
    echo .env already exists, skipping.
)

echo.
echo [4/4] Setup complete!
echo.
echo ============================================
echo   NEXT STEPS:
echo   1. Edit backend\.env with your API keys
echo   2. Run: start.bat
echo ============================================
pause
