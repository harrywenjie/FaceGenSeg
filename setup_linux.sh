#!/bin/bash

# Check if Python 3.10 is installed
if ! command -v python3.10 &> /dev/null; then
  echo "Python 3.10 is not installed. Please install it and try again."
  exit 1
fi

# Check if python3.10-venv is installed
if ! python3.10 -c 'import venv' &> /dev/null; then
  echo "python3.10-venv is not installed. Please install it (e.g., sudo apt-get install python3.10-venv) and try again."
  exit 1
fi

if [ ! -d "venv" ]; then
  python3.10 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
