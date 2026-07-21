#!/bin/bash

# SHIELD Project - Unified Start Script
# This script starts both the FastAPI backend and Flutter frontend, 
# ensuring clean shutdown of background processes upon exit.

# Default values
DEVICE=""

# Parse arguments
while getopts d: flag
do
    case "${flag}" in
        d) DEVICE=${OPTARG};;
    esac
done

# If no device was provided via flags, prompt the user
if [ -z "$DEVICE" ]; then
    echo "Please select the target device to run the Flutter frontend:"
    echo "1) Chrome (Web) (Default)"
    echo "2) Linux"
    echo "3) Windows"
    read -p "Enter choice [1-3]: " choice
    case "$choice" in
        2) DEVICE="linux" ;;
        3) DEVICE="windows" ;;
        *) DEVICE="chrome" ;;
    esac
fi

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
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
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

# Get the primary local IP address to allow external devices to connect
LOCAL_IP=$(hostname -I | awk '{print $1}')
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="127.0.0.1"
fi
BACKEND_URL="ws://${LOCAL_IP}:8000"

# Run the flutter app
echo "Running: $FLUTTER_CMD run -d $DEVICE --dart-define=BACKEND_URL=$BACKEND_URL"
$FLUTTER_CMD run -d $DEVICE --dart-define=BACKEND_URL=$BACKEND_URL

# If flutter run fails, try interactive fallback
if [ $? -ne 0 ]; then
    echo -e "\n⚠️ Could not launch on '$DEVICE'. Trying interactive device selection..."
    $FLUTTER_CMD run --dart-define=BACKEND_URL=$BACKEND_URL
fi
