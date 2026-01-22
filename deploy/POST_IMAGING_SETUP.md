# Post-Imaging Setup Guide

## Step 1: Flash SD Card with Raspberry Pi Imager

Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

### Imager Settings (⚙️ gear icon)

**IMPORTANT:** Click the gear icon ⚙️ in the bottom right before flashing!

```
Operating System:
  ✓ Raspberry Pi OS Lite (64-bit)
    (or whichever OS you were using before)

General Settings:
  ✓ Set hostname: delmonte
  ✓ Enable SSH
    → Use password authentication
  ✓ Set username and password:
    → Username: pi
    → Password: [your Pi password]

Configure Wireless LAN:
  ✓ SSID: lpzfam
  ✓ Password: flcslb!986$*
  ✓ Wireless LAN country: US
  
  NOTE: We'll add the second network (VGBND Guest) after setup

Services:
  ✓ Enable SSH
  
Locale Settings:
  → Timezone: America/Los_Angeles (or your timezone)
  → Keyboard layout: us
```

### Flash Process

1. Insert SD card
2. Select your OS
3. Click ⚙️ gear icon and configure settings above
4. Click "Write"
5. Wait for completion
6. Eject SD card safely

---

## Step 2: Boot Pi and Wait for Network Connection

1. Insert SD card into Pi
2. Power on the Pi
3. **Wait 2-3 minutes** for first boot and WiFi connection
4. Green LED should blink (SD card activity)

### Verify Connection

```bash
# From your Mac, test connection:
ping -c 3 delmonte.local

# Should see responses like:
# 64 bytes from delmonte.local (192.168.86.x): icmp_seq=0 ttl=64 time=...
```

If `delmonte.local` doesn't resolve, check your router at http://192.168.86.1 for the Pi's IP address.

---

## Step 3: Set Up SSH Keys (Optional but Recommended)

```bash
# Copy your SSH key to the Pi (enter Pi password when prompted)
ssh-copy-id pi@delmonte.local

# Test passwordless login
ssh pi@delmonte.local
```

---

## Step 4: Run Initial Pi Setup

This installs dependencies and configures audio.

```bash
make setup
```

This will:
- Update system packages
- Install Python, pygame, GPIO libraries
- Configure USB audio output
- Create project directories

**Expected duration:** 5-10 minutes

---

## Step 5: Deploy Your Code

```bash
make deploy
```

This will:
- Sync all code to the Pi
- Create remote directories

**Expected duration:** 30 seconds

---

## Step 6: Install and Start the Service

```bash
make setup-service
```

This will:
- Install the systemd service
- Enable auto-start on boot
- Start the service

**Expected duration:** 10 seconds

---

## Step 7: Add Second WiFi Network (VGBND Guest)

For when you take the Pi to Del Monte house:

```bash
make wifi-add SSID="VGBND Guest" PASS="137VgbnDavis" PRIORITY=20
```

Priority 20 = higher than lpzfam (10), so it will prefer VGBND Guest when both are available.

---

## Step 8: Verify Everything Works

```bash
# Check service status
make status

# View logs (Ctrl+C to exit)
make logs

# Test that rotary phone is working
# Pick up handset, should hear audio playing
```

---

## Complete Command Summary

Once the Pi is online at `delmonte.local`, run these commands in order:

```bash
# 1. Initial setup (one time)
make setup

# 2. Deploy code
make deploy

# 3. Install service
make setup-service

# 4. Add Del Monte WiFi
make wifi-add SSID="VGBND Guest" PASS="137VgbnDavis" PRIORITY=20

# 5. Verify
make status
make logs
```

---

## Troubleshooting

### Pi won't connect to WiFi
- Verify WiFi credentials in Raspberry Pi Imager were correct
- Check router (http://192.168.86.1) for connected devices
- Try SSH with IP address instead: `ssh pi@192.168.86.x`

### Cannot SSH into Pi
- Verify SSH was enabled in Imager settings
- Check hostname: `ping delmonte.local`
- Try IP address: `ssh pi@192.168.86.x`

### Service won't start
```bash
# View detailed logs
make logs-recent

# Check service status
make status

# Restart service
make restart
```

### USB audio not working
```bash
# SSH into Pi and check audio devices
make ssh
aplay -l

# Should see "USB Audio" device listed
# If not, reconnect USB audio adapter and reboot
```

---

## Future Deployments

After initial setup, deploying updates is simple:

```bash
# Deploy new code and restart service
make deploy

# View logs to verify
make logs
```

No need to reflash or reconfigure!
