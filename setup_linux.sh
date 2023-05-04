#!/bin/bash

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install python3.10-tk
