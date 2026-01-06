#!/bin/bash
# Setup WiFi networks on Raspberry Pi
# Usage: ./setup-wifi.sh [SSID] [PASSWORD] [PRIORITY]
#
# Examples:
#   ./setup-wifi.sh "HomeNetwork" "password123" 10
#   ./setup-wifi.sh "RentalNetwork" "password456" 20
#
# Higher priority = preferred when multiple networks available

SSID="$1"
PASSWORD="$2"
PRIORITY="${3:-10}"

if [ -z "$SSID" ] || [ -z "$PASSWORD" ]; then
    echo "Usage: $0 SSID PASSWORD [PRIORITY]"
    echo ""
    echo "Current saved networks:"
    nmcli connection show | grep wifi
    exit 1
fi

echo "Adding WiFi network: $SSID (priority: $PRIORITY)"

# Check if network already exists
if nmcli connection show "$SSID" &>/dev/null; then
    echo "Network '$SSID' already exists, updating..."
    nmcli connection modify "$SSID" wifi-sec.psk "$PASSWORD"
    nmcli connection modify "$SSID" connection.autoconnect-priority "$PRIORITY"
else
    echo "Adding new network..."
    nmcli device wifi connect "$SSID" password "$PASSWORD"
    nmcli connection modify "$SSID" connection.autoconnect-priority "$PRIORITY"
fi

echo ""
echo "Saved WiFi networks:"
nmcli connection show | grep wifi

echo ""
echo "Done. Pi will auto-connect to whichever network is in range."
