#!/bin/bash

echo "HELLO"
python scripts/getPlayerData.py
echo "Starting get Edge Data"
python scripts/getEdgeData.py
python scripts/sendData.py
