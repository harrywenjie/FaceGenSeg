@echo off

:: Create a virtual environment if it doesn't exist
if not exist "venv" (
  python -m venv venv
)

:: Activate the virtual environment and install requirements
call venv\Scripts\activate.bat
pip install --use-pep517 -r requirements.txt

python webAPI.py