#!/bin/bash

# Check if Python 3.10 is installed
if ! command -v python3.10 &> /dev/null; then
  echo "Python 3.10 is not installed. Please install it and try again."
  read -n 1 -s -r -p "Press any key to quit"
  exit 1
fi

# Check if python3.10-venv is installed
if ! python3.10 -c 'import venv' &> /dev/null; then
  echo "python3.10-venv is not installed. Please install it (e.g., sudo apt-get install python3.10-venv) and try again."
  read -n 1 -s -r -p "Press any key to quit"
  exit 1
fi

if [ ! -d "venv" ]; then
  python3.10 -m venv venv
fi

source venv/bin/activate
pip install --use-pep517 -r requirements.txt

if [ $? -eq 0 ]; then
  echo "Installation completed successfully!"
  read -n 1 -s -r -p "Press any key to finish installation"
else
  echo "Installation failed!"
  read -n 1 -s -r -p "Press any key to quit"
  exit 1
fi
