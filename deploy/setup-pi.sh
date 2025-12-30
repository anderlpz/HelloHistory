#!/bin/bash
#
# HelloHistory - First-Time Pi Setup
# Run this once after flashing a fresh Raspberry Pi OS
#
# Usage (from your Mac):
#   make setup
#
# Or manually:
#   scp deploy/setup-pi.sh pi@delmonte.local:~/
#   ssh pi@delmonte.local 'chmod +x setup-pi.sh && ./setup-pi.sh'
#

set -e

echo "═══════════════════════════════════════════════════════════"
echo "  HelloHistory - Raspberry Pi Setup"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Step 1: Update system
echo "▶ Updating system packages..."
sudo apt update && sudo apt upgrade -y
echo "✓ System updated"

# Step 2: Install dependencies
echo ""
echo "▶ Installing dependencies..."
sudo apt install -y \
    python3-pip \
    python3-pygame \
    python3-rpi.gpio \
    alsa-utils \
    git
echo "✓ Dependencies installed"

# Step 3: Create project directory
echo ""
echo "▶ Creating project directory..."
mkdir -p ~/delmonte/src ~/delmonte/logs
echo "✓ Directory created: ~/delmonte"

# Step 4: Configure audio
echo ""
echo "▶ Configuring USB audio..."

# Check if USB audio device is connected
if aplay -l | grep -q "USB Audio"; then
    echo "  USB audio device detected"
    
    # Get the card number
    CARD_NUM=$(aplay -l | grep "USB Audio" | head -1 | sed 's/card \([0-9]\).*/\1/')
    
    # Create ALSA config
    sudo tee /etc/asound.conf > /dev/null << EOF
defaults.pcm.card ${CARD_NUM}
defaults.ctl.card ${CARD_NUM}
EOF
    echo "✓ USB audio set as default (card ${CARD_NUM})"
else
    echo "⚠ USB audio device not detected"
    echo "  Connect the USB audio adapter and run this script again"
fi

# Step 5: Test audio (optional)
echo ""
read -p "▶ Test audio output? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  Playing test tone (Ctrl+C to stop)..."
    speaker-test -t sine -f 440 -c 1 -l 1 || true
    echo "✓ Audio test complete"
fi

# Step 6: Install systemd service
echo ""
echo "▶ Installing systemd service..."
if [ -f ~/delmonte/deploy/hellohistory.service ]; then
    sudo cp ~/delmonte/deploy/hellohistory.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable hellohistory
    echo "✓ Service installed and enabled"
    echo "  (Will start automatically on boot)"
else
    echo "⚠ Service file not found"
    echo "  Run 'make deploy' first, then 'make setup-service'"
fi

# Step 7: Summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Setup Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "  Next steps:"
echo "  1. From your Mac, deploy the code:"
echo "     make deploy"
echo ""
echo "  2. Start the service:"
echo "     make start"
echo ""
echo "  3. View logs:"
echo "     make logs"
echo ""
echo "  Pi will auto-start HelloHistory on boot."
echo ""
