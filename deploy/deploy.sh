#!/bin/bash
#
# HelloHistory Deploy Script
# Syncs code to Raspberry Pi and restarts the service
#
# Usage:
#   ./deploy/deploy.sh              # Deploy to delmonte.local
#   ./deploy/deploy.sh 192.168.1.50 # Deploy to specific IP
#

set -e

PI_HOST="${1:-delmonte.local}"
PI_USER="pi"
REMOTE_PATH="/home/pi/delmonte"

echo "═══════════════════════════════════════════════════════════"
echo "  HelloHistory Deploy"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "  Target: ${PI_USER}@${PI_HOST}:${REMOTE_PATH}"
echo ""

# Step 1: Verify connection
echo "▶ Checking connection..."
if ! ssh -o ConnectTimeout=5 -o BatchMode=yes "${PI_USER}@${PI_HOST}" 'echo "connected"' > /dev/null 2>&1; then
    echo "✗ Cannot connect to ${PI_HOST}"
    echo ""
    echo "  Troubleshooting:"
    echo "  1. Is the Pi powered on and connected to WiFi?"
    echo "  2. Try: ping ${PI_HOST}"
    echo "  3. Try: ssh ${PI_USER}@${PI_HOST}"
    echo "  4. Check your SSH keys: ssh-copy-id ${PI_USER}@${PI_HOST}"
    exit 1
fi
echo "✓ Connected to ${PI_HOST}"

# Step 2: Ensure remote directory exists
echo ""
echo "▶ Preparing remote directory..."
ssh "${PI_USER}@${PI_HOST}" "mkdir -p ${REMOTE_PATH}/src ${REMOTE_PATH}/logs"
echo "✓ Remote directory ready"

# Step 3: Sync files
echo ""
echo "▶ Syncing files..."
rsync -avz --delete \
    --exclude='.git' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='*.egg-info' \
    --exclude='.amplifier' \
    ./src/ "${PI_USER}@${PI_HOST}:${REMOTE_PATH}/src/"

# Also sync deploy files (for service management)
rsync -avz \
    ./deploy/*.service \
    "${PI_USER}@${PI_HOST}:${REMOTE_PATH}/deploy/" 2>/dev/null || true

echo "✓ Files synced"

# Step 4: Check if service exists and restart
echo ""
echo "▶ Checking service status..."
if ssh "${PI_USER}@${PI_HOST}" "systemctl is-enabled hellohistory 2>/dev/null"; then
    echo "  Service installed, restarting..."
    ssh "${PI_USER}@${PI_HOST}" "sudo systemctl restart hellohistory"
    sleep 2
    if ssh "${PI_USER}@${PI_HOST}" "systemctl is-active hellohistory" | grep -q "active"; then
        echo "✓ Service restarted successfully"
    else
        echo "⚠ Service may have failed to start. Check logs:"
        echo "  ssh ${PI_USER}@${PI_HOST} 'journalctl -u hellohistory -n 20'"
    fi
else
    echo "  Service not installed yet."
    echo "  To install, run: make setup-service"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Deploy complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "  Useful commands:"
echo "    make logs      # View service logs"
echo "    make ssh       # SSH into Pi"
echo "    make status    # Check service status"
echo ""
