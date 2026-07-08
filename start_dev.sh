#!/bin/bash
echo "Starting Backend..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
echo "Backend started with PID $BACKEND_PID"

echo "Starting Frontend..."
cd ../frontend
# Run on Chrome. Added wayland flags just in case, though XWayland usually works too.
/home/sp/flutter/bin/flutter run -d chrome

# Cleanup backend when frontend is closed
kill $BACKEND_PID
