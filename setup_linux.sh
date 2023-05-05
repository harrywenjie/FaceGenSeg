#!/bin/bash

cleanup() {
  echo "Cleaning up..."
  pkill -f "uvicorn" || true
  pkill -f "webGUI.py" || true
  exit 0
}

trap cleanup SIGINT SIGTERM

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

# Kill any existing uvicorn processes
pkill -f "uvicorn" || true
pkill -f "webGUI.py" || true

# Start the FastAPI webAPI and Flask webGUI
uvicorn webAPI:app --host 0.0.0.0 --port 8000 &> /dev/null &
python webGUI.py &> /dev/null &

echo "WebAPI running on port 8000"
echo "WebGUI running on port 5000"
echo "Press Ctrl+C to stop both services"

wait
