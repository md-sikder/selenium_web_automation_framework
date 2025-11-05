@echo off
setlocal ENABLEDELAYEDEXPANSION

title Selenium UI Tests Runner
echo === Selenium UI Tests Runner (Windows) ===

:: 1) Check Python
where python >NUL 2>&1
if errorlevel 1 (
  echo [ERROR] Python is not installed or not on PATH.
  echo Download: https://www.python.org/downloads/
  pause
  exit /b 1
)

:: 2) Create venv if missing
if not exist ".venv" (
  echo Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
  )
)

:: 3) Activate venv
call .venv\Scripts\activate
if errorlevel 1 (
  echo [ERROR] Failed to activate virtual environment.
  pause
  exit /b 1
)

:: 4) Upgrade pip and install deps
echo Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] pip install failed. Check your internet and requirements.txt
  pause
  exit /b 1
)

:: 5) Ask user: headed or headless?
echo.
echo Choose run mode:
echo   1 ^) GUI (headed)  [default]
echo   2 ^) Headless
set /p RUNMODE=Enter choice (1/2) and press Enter:
if "%RUNMODE%"=="2" (
  set HEADLESS=true
) else (
  set HEADLESS=false
)

:: 6) Ensure report dirs
if not exist reports mkdir reports
if not exist logs mkdir logs
if not exist screenshots mkdir screenshots

:: 7) Run pytest
echo.
echo Running tests (HEADLESS=%HEADLESS%) ...
set PYTEST_CMD=pytest -n auto --env=test --html=reports\report.html --self-contained-html
if "%HEADLESS%"=="true" (
  set PYTEST_CMD=%PYTEST_CMD% --headless
)
%PYTEST_CMD%
set EXITCODE=%ERRORLEVEL%

echo.
echo Generated report: reports\report.html
if exist reports\report.html (
  start "" reports\report.html
)

echo.
if %EXITCODE% NEQ 0 (
  echo [DONE] Tests finished with failures. Exit code: %EXITCODE%
) else (
  echo [DONE] All tests passed. Exit code: %EXITCODE%
)
pause
exit /b %EXITCODE%
