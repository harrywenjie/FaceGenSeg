@echo off

:: Check if Python 3.10 is installed
where python3.10 >nul 2>&1
if errorlevel 1 (
  echo Python 3.10 is not installed. Please install it and try again.
  pause
  exit /b 1
)

:: Check if python3.10-venv is installed
python3.10 -c "import venv" >nul 2>&1
if errorlevel 1 (
  echo python3.10-venv is not installed. Please install it (e.g., using the Python installer) and try again.
  pause
  exit /b 1
)

:: Create a virtual environment if it doesn't exist
if not exist "venv" (
  python3.10 -m venv venv
)

:: Activate the virtual environment and install requirements
call venv\Scripts\activate.bat
pip install -r requirements.txt

if errorlevel 1 (
  echo Installation failed!
  pause
  exit /b 1
) else (
  echo Installation completed successfully!
  pause
)
