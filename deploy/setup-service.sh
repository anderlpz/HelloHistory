#!/bin/bash
# Setup phone player service to start on boot

set -e

echo "==============================================================="
echo "  Setting up Phone Player Service"
echo "==============================================================="

# Create service file
echo "Creating systemd service..."
sudo tee /etc/systemd/system/phone-player.service > /dev/null << 'SERVICEEOF'
[Unit]
Description=Del Monte Phone Player
After=sound.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/delmonte
ExecStart=/usr/bin/python3 /home/pi/delmonte/src/phone_player.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF

echo "OK Service file created"

# Reload and enable
echo "Enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable phone-player
echo "OK Service enabled"

# Start the service
echo "Starting service..."
sudo systemctl start phone-player
echo "OK Service started"

# Show status
echo ""
echo "==============================================================="
echo "  Service Status"
echo "==============================================================="
sudo systemctl status phone-player --no-pager || true

echo ""
echo "OK Setup complete! The phone player will now start on boot."
echo ""
echo "  Useful commands:"
echo "    sudo systemctl status phone-player   # Check status"
echo "    sudo systemctl restart phone-player  # Restart"
echo "    sudo systemctl stop phone-player     # Stop"
echo "    journalctl -u phone-player -f        # View logs"
echo ""
