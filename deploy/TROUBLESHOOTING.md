# HelloHistory Deployment Troubleshooting Guide

This guide documents common issues encountered during Raspberry Pi setup and deployment, with root cause analysis and solutions.

## Table of Contents

- [Fresh Pi Setup Issues](#fresh-pi-setup-issues)
- [Deployment Issues](#deployment-issues)
- [Audio Playback Issues](#audio-playback-issues)
- [Network Connectivity Issues](#network-connectivity-issues)
- [Quick Reference Commands](#quick-reference-commands)

---

## Fresh Pi Setup Issues

### Issue 1: SSH Key Authentication Fails with BatchMode

**Symptoms:**
```bash
make deploy
# Output: ✗ Cannot connect to delmonte.local
```

SSH works manually but `make deploy` fails with "Permission denied (publickey,password)".

**Root Cause:**

The deploy script uses `ssh -o BatchMode=yes` which disables password prompts and requires key-based authentication. If you have multiple SSH keys, SSH may try the wrong key first.

**Diagnosis:**

```bash
# Test manual SSH (works):
ssh pi@delmonte.local 'echo "connected"'

# Test batch mode SSH (fails):
ssh -o BatchMode=yes pi@delmonte.local 'echo "connected"'
```

If manual works but batch mode fails, it's a key selection issue.

**Solution:**

Create an SSH config entry specifying the correct key:

```bash
cat >> ~/.ssh/config << 'EOF'

Host delmonte.local
  HostName delmonte.local
  User pi
  IdentityFile ~/.ssh/YOUR_KEY_NAME
EOF
```

Replace `YOUR_KEY_NAME` with your actual key file (e.g., `id_ed25519_pidrive`).

**Prevention:**

- Use `ssh-copy-id` after fresh imaging to install keys
- Configure SSH config during initial setup
- Test with `ssh -o BatchMode=yes` before deployment

---

### Issue 2: mpg123 Not Installed

**Symptoms:**

```
Jan 22 01:27:22 delmonte python3[570]: Error: [Errno 2] No such file or directory: 'mpg123'
```

Phone detects handset lift but no audio plays. Logs show tracks "playing" but finishing instantly.

**Root Cause:**

`mpg123` (the MP3 player) was not included in the dependency installation list in `setup-pi.sh`. The Python code tries to spawn `mpg123` processes but the command doesn't exist.

**Diagnosis:**

```bash
# Check if mpg123 is installed:
ssh pi@delmonte.local 'which mpg123'
# Returns nothing if not installed

# Check service logs:
make logs
# Shows: Error: [Errno 2] No such file or directory: 'mpg123'
```

**Solution:**

```bash
# Install mpg123 manually:
ssh pi@delmonte.local 'sudo apt install -y mpg123'

# Restart service:
make restart
```

**Prevention:**

✅ **FIXED** - The `setup-pi.sh` script has been updated to include `mpg123` in the dependency installation:

```bash
sudo apt install -y \
    python3-pip \
    python3-pygame \
    python3-rpi.gpio \
    alsa-utils \
    mpg123 \
    git
```

This issue should not occur on future re-imaging.

---

### Issue 3: ALSA Audio Configured for Wrong Card

**Symptoms:**

```bash
speaker-test
# Output: Playback open error: -524,Unknown error 524
```

`mpg123` processes start but no sound plays. Audio test commands fail.

**Root Cause:**

The ALSA default audio card was set to card 1 (HDMI audio) instead of card 0 (USB Audio Device). The setup script auto-detected the card number but may have gotten it wrong, or the card numbers changed after SD card reflashing.

**Diagnosis:**

```bash
# List audio devices:
ssh pi@delmonte.local 'aplay -l'
# Output shows:
# card 0: Device [USB Audio Device] ← This is what we want
# card 1: vc4hdmi [vc4-hdmi]        ← This is HDMI

# Check current ALSA config:
ssh pi@delmonte.local 'cat /etc/asound.conf'
# Output shows:
# defaults.pcm.card 1  ← WRONG! Should be 0
# defaults.ctl.card 1
```

**Solution:**

```bash
# Fix ALSA config to use card 0:
ssh pi@delmonte.local 'echo "defaults.pcm.card 0" | sudo tee /etc/asound.conf'
ssh pi@delmonte.local 'echo "defaults.ctl.card 0" | sudo tee -a /etc/asound.conf'

# Test audio:
ssh pi@delmonte.local 'speaker-test -D plughw:0,0 -c 1 -t sine -f 440 -l 1'

# Restart service:
make restart
```

**Prevention:**

- Always verify USB audio is card 0 after imaging
- Run `make setup` with USB audio adapter plugged in
- Test audio before deploying code:
  ```bash
  ssh pi@delmonte.local 'speaker-test -t sine -f 440 -l 1'
  ```

**Note:** The setup script attempts to auto-detect the card number. If issues persist, this may need to be hardcoded to card 0 for USB Audio devices.

---

## Deployment Issues

### Issue 4: SSH Host Key Changed After Re-imaging

**Symptoms:**

```
ssh-copy-id pi@delmonte.local
# Output: WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
# ERROR: Host key verification failed.
```

**Root Cause:**

When you reflash the SD card, the Pi generates new SSH host keys. Your Mac still remembers the old keys and treats this as a potential security threat.

**Solution:**

```bash
# Remove old host key:
ssh-keygen -R delmonte.local

# Try ssh-copy-id again:
ssh-copy-id pi@delmonte.local
```

This is **normal and expected** after re-imaging. It's a security feature, not a bug.

**Prevention:**

- Document this as an expected step in re-imaging process
- Always run `ssh-keygen -R` after flashing a fresh SD card

---

### Issue 5: Network Configuration Manual Editing Breaks WiFi

**Symptoms:**

Pi boots successfully but never appears on the network. Can't ping `delmonte.local` or connect via SSH.

**Root Cause:**

Manually editing `/boot/network-config` with complex passwords containing special characters (`$`, `*`, `!`) can break the netplan YAML syntax or password handling. The Pi boots but WiFi never connects.

**Solution:**

**DO NOT manually edit network-config files.** Use Raspberry Pi Imager to configure WiFi:

1. Use Raspberry Pi Imager's built-in settings (⚙️ gear icon)
2. Let the imager handle special characters and password encoding
3. Configure primary WiFi network during imaging
4. Add additional networks after deployment using `make wifi-add`

**Prevention:**

✅ **DOCUMENTED** - Created `deploy/POST_IMAGING_SETUP.md` with step-by-step Raspberry Pi Imager configuration instructions. Always use this guide instead of manual file editing.

---

## Audio Playback Issues

### Jack/PulseAudio Warnings (Non-Critical)

**Symptoms:**

```
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1
Cannot connect to server socket err = No such file or directory
jack server is not running or cannot be started
```

**Root Cause:**

`mpg123` tries to connect to Jack or PulseAudio servers but falls back to ALSA when they're not available.

**Impact:**

⚠️ **These warnings are harmless.** Audio plays correctly via ALSA. These are just informational messages that can be ignored.

**Solution:**

No action needed. Audio works correctly despite the warnings.

---

## Network Connectivity Issues

### Pi Not Appearing on Network After Boot

**Symptoms:**

- Pi powers on, green LED blinks (SD card activity)
- Can't ping `delmonte.local`
- Not showing up in router's device list
- Tailscale shows device offline

**Diagnosis Checklist:**

1. **Wait longer** - First boot takes 2-3 minutes for filesystem expansion and network setup
2. **Check WiFi credentials** - Verify password was entered correctly in Pi Imager
3. **Check WiFi network** - Confirm the configured SSID is in range and broadcasting
4. **Check hostname** - Try `ping raspberrypi.local` (default hostname if yours didn't apply)
5. **Check router** - Look for new "raspberrypi" or "delmonte" devices at http://192.168.86.1

**Common Causes:**

- WiFi password typo during imaging
- Special characters in WiFi password not handled correctly
- WiFi network out of range
- 5GHz network selected but Pi only supports 2.4GHz (older Pi models)

**Solution:**

If WiFi won't connect after 5+ minutes:

1. **Re-flash with Raspberry Pi Imager** using the exact steps in `deploy/POST_IMAGING_SETUP.md`
2. Double-check WiFi credentials during setup
3. Use a simpler WiFi network (2.4GHz, WPA2, standard characters) for initial setup
4. Add complex networks later using `make wifi-add`

---

## Quick Reference Commands

### Diagnostic Commands

```bash
# Check if Pi is reachable:
ping -c 3 delmonte.local

# Check SSH connectivity:
ssh pi@delmonte.local 'echo "connected"'

# Check service status:
make status

# View recent logs:
make logs

# List audio devices:
ssh pi@delmonte.local 'aplay -l'

# Check ALSA config:
ssh pi@delmonte.local 'cat /etc/asound.conf'

# Test audio playback:
ssh pi@delmonte.local 'speaker-test -t sine -f 440 -l 1'

# Check if mpg123 is installed:
ssh pi@delmonte.local 'which mpg123'

# Check WiFi networks:
ssh pi@delmonte.local 'nmcli connection show'

# Check Tailscale status:
/Applications/Tailscale.app/Contents/MacOS/Tailscale status | grep delmonte
```

### Quick Fixes

```bash
# Fix SSH host key warning:
ssh-keygen -R delmonte.local

# Copy SSH keys:
ssh-copy-id pi@delmonte.local

# Install missing mpg123:
ssh pi@delmonte.local 'sudo apt install -y mpg123'

# Fix ALSA audio card:
ssh pi@delmonte.local 'echo "defaults.pcm.card 0" | sudo tee /etc/asound.conf'
ssh pi@delmonte.local 'echo "defaults.ctl.card 0" | sudo tee -a /etc/asound.conf'

# Restart service:
make restart

# Restart Pi:
ssh pi@delmonte.local 'sudo reboot'
```

### Deployment Sequence (After Fresh Imaging)

```bash
# 1. Remove old SSH host key:
ssh-keygen -R delmonte.local

# 2. Copy SSH keys:
ssh-copy-id pi@delmonte.local

# 3. Test connection:
ping -c 3 delmonte.local

# 4. Initial setup (installs dependencies, configures audio):
make setup

# 5. Deploy code:
make deploy

# 6. Install service:
make setup-service

# 7. Add second WiFi network (optional):
make wifi-add SSID="NetworkName" PASS="password" PRIORITY=20

# 8. Verify service:
make status
make logs

# 9. Test physically:
# Pick up phone handset and verify audio plays
```

---

## Summary of Fixes Applied

The following preventive fixes have been implemented:

✅ **mpg123 dependency** - Added to `setup-pi.sh` (commit 3216281)
✅ **Deployment guide** - Created `POST_IMAGING_SETUP.md` with step-by-step Raspberry Pi Imager instructions (commit 2c97ca9)
✅ **PII removed** - WiFi credentials removed from documentation (commit 25e22c4)
✅ **UX improvement** - Added 1.5 second delay after handset pickup (commit 2a5e334)

### Remaining Manual Steps

The following issues still require manual intervention:

⚠️ **ALSA card configuration** - May need manual fix if USB audio is detected as card 1 instead of card 0
⚠️ **SSH config** - Requires manual creation of SSH config entry if you have multiple keys
⚠️ **WiFi troubleshooting** - Complex passwords or network issues may require re-imaging

---

## When to Re-Image vs. Repair

**Re-image (reflash SD card) when:**
- WiFi won't connect after 5+ minutes
- You manually edited network-config and broke something
- Multiple issues compound and system state is uncertain
- Faster than debugging (takes 10 minutes total)

**Repair (fix in place) when:**
- Single known issue (mpg123 missing, ALSA misconfigured)
- SSH/deployment issues (doesn't require reflash)
- Audio issues after code changes
- Service crashes or won't start

**Rule of thumb:** If you're not sure, re-image. It's faster and more reliable than debugging ambiguous network/boot issues.

---

## Getting Help

If you encounter new issues:

1. **Check logs first**: `make logs`
2. **Check service status**: `make status`
3. **Test basic connectivity**: `ping delmonte.local`
4. **Review this guide** for similar symptoms
5. **Check recent commits** for related changes: `git log --oneline -10`

**Document new issues** by adding them to this guide with:
- Symptoms (what you observed)
- Root cause (why it happened)
- Solution (how you fixed it)
- Prevention (how to avoid it)

This living document improves with each deployment cycle.
