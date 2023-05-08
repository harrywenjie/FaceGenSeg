@echo off

if not exist "venv" (
  echo Virtual environment not found. Please run setup.bat first and then run this script.
  pause
  exit /b 1
)

call venv\Scripts\activate.bat
if errorlevel 1 (
  echo Error activating the virtual environment.Please run setup.bat first and try again.
  pause
  exit /b 1
)

start cmd /k "python webAPI.py"
start cmd /k "python webGUI.py"

echo Both webAPI.py and webGUI.py are running. Close this window to stop them.
pause

:: Kill the processes when the command prompt is closed
taskkill /IM python.exe /F
