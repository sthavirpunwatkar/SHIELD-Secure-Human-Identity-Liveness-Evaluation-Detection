#!/bin/bash

# SHIELD Project - Unified Start Script
# This script starts both the FastAPI backend and Flutter frontend, 
# ensuring clean shutdown of background processes upon exit.

# Default values
DEVICE="linux" # fallback to linux, can be overridden with ./start_dev.sh -d chrome

# Parse arguments
while getopts d: flag
do
    case "${flag}" in
        d) DEVICE=${OPTARG};;
    esac
done

echo "========================================="
echo " 🛡️  Starting SHIELD Development Session "
echo "========================================="

# Process cleanup on exit (handles Ctrl+C gracefully)
cleanup() {
    echo -e "\n🛑 Shutting down SHIELD project..."
    if [ ! -z "$BACKEND_PID" ]; then
        echo "Killing Backend (PID: $BACKEND_PID)..."
        kill -9 $BACKEND_PID 2>/dev/null || true
    fi
    echo "Cleanup complete. Goodbye!"
    exit 0
}
trap cleanup EXIT INT TERM

# --- 1. Start Backend ---
echo -e "\n[1/2] Starting Backend (FastAPI)..."
cd backend || { echo "❌ Backend directory not found!"; exit 1; }

# Find and activate virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "Using backend/venv environment..."
    source venv/bin/activate
elif [ -f "../.venv/bin/activate" ]; then
    echo "Using .venv environment from project root..."
    source ../.venv/bin/activate
else
    echo "⚠️ Warning: No virtual environment found. Running python directly."
fi

# Run backend
python main.py &
BACKEND_PID=$!
echo "Backend running with PID: $BACKEND_PID"

# Give backend a moment to start up and bind to port
sleep 2

# --- 2. Start Frontend ---
echo -e "\n[2/2] Starting Frontend (Flutter on $DEVICE)..."
cd ../frontend || { echo "❌ Frontend directory not found!"; exit 1; }

# Locate flutter executable
if command -v flutter &> /dev/null; then
    FLUTTER_CMD="flutter"
elif [ -f "/home/sp/flutter/bin/flutter" ]; then
    FLUTTER_CMD="/home/sp/flutter/bin/flutter"
else
    echo "❌ Error: Flutter not found in PATH or standard location (/home/sp/flutter/bin/flutter)."
    exit 1
fi

# Run the flutter app
echo "Running: $FLUTTER_CMD run -d $DEVICE"
$FLUTTER_CMD run -d $DEVICE

# If flutter run fails, try interactive fallback
if [ $? -ne 0 ]; then
    echo -e "\n⚠️ Could not launch on '$DEVICE'. Trying interactive device selection..."
    $FLUTTER_CMD run
fi
