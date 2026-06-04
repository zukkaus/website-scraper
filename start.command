#!/bin/bash

# ── WVCAC Local Dev Server ─────────────────────────────────────────
cd "$(dirname "$0")"

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║   WVCAC Website — Starting server    ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

# Kill any existing process on port 8080
lsof -ti :8080 | xargs kill -9 2>/dev/null
sleep 1

# Start server in background
python3 -m http.server 8080 &
SERVER_PID=$!

echo "  ✓ Server running at http://localhost:8080"
echo "  ✓ Press Ctrl+C in this window to stop"
echo ""

# Wait a moment then open browser
sleep 1
open http://localhost:8080/index.html

# Keep window open so server stays alive
wait $SERVER_PID
