@echo off
echo ========================================
echo   FraudX Agent - Local Deployment
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo [2/4] Checking dependencies...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Dependencies not installed. Installing now...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed.
)
echo.

echo [3/4] Starting Backend API...
echo Backend will run on http://localhost:8001
echo API Docs: http://localhost:8001/docs
echo.
start "FraudX Backend" cmd /k "cd Backend && python main.py"
timeout /t 3 >nul
echo.

echo [4/4] Starting Frontend UI...
echo Frontend will open in your browser at http://localhost:8501
echo.
start "FraudX Frontend" cmd /k "cd Frontend && streamlit run streamlit_app.py"
echo.

echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Services running:
echo   - Backend API: http://localhost:8001
echo   - API Docs: http://localhost:8001/docs
echo   - Frontend UI: http://localhost:8501
echo.
echo Press any key to view this window's logs...
pause >nul

@REM Made with Bob
