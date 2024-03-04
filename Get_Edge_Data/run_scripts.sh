#!/bin/bash

echo "HELLO"
python scripts/getPlayerData.py
python scripts/getEdgeData.py
python scripts/sendData.py
