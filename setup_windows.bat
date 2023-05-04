@echo off

IF NOT EXIST venv (
  python -m venv venv
)

venv\Scripts\activate
pip install -r requirements.txt
