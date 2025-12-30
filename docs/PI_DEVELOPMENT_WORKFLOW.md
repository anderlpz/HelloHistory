# Pi Development Workflow Design

**Goal:** Define a "develop locally, deploy to Pi" workflow that:
1. Solves HelloHistory's immediate needs
2. Creates reusable Amplifier components for the community

---

## The Problem

Developing for Raspberry Pi (or any embedded/remote device) presents challenges:

1. **No local hardware** - Can't run GPIO code on Mac/Windows
2. **Slow iteration** - SSH + edit + test cycle is tedious
3. **Headless operation** - Pi often runs without monitor/keyboard
4. **Service management** - Need to install, start, restart services
5. **Environment differences** - Mac vs Pi (ARM Linux) differences

## The Solution: Layered Approach

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer's Mac                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Source Code │  │ Local Test  │  │ Amplifier + Tools   │ │
│  │ (git repo)  │  │ (simulator) │  │ (deploy commands)   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────┬───────────────────────────────────┘
                          │ SSH / rsync
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Raspberry Pi                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Deployed    │  │ systemd     │  │ Hardware            │ │
│  │ Code        │  │ Service     │  │ (GPIO, audio, etc)  │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Proposed Amplifier Components

### 1. Recipe: `pi-deploy`

A declarative recipe for deploying projects to Raspberry Pi.

```yaml
name: "pi-deploy"
description: "Deploy a project to Raspberry Pi over SSH"
version: "1.0.0"

context:
  pi_host: ""              # e.g., "delmonte.local" or IP
  pi_user: "pi"            # SSH username
  local_path: "."          # Local project path
  remote_path: ""          # e.g., "~/delmonte"
  service_name: ""         # Optional systemd service
  exclude_patterns:        # Files to skip
    - ".git"
    - "venv"
    - "__pycache__"
    - "*.pyc"
    - ".DS_Store"

steps:
  - id: "verify-connection"
    type: "bash"
    command: "ssh -o ConnectTimeout=5 {{pi_user}}@{{pi_host}} 'echo connected'"
    
  - id: "sync-files"
    type: "bash"
    command: |
      rsync -avz --delete \
        --exclude='.git' --exclude='venv' --exclude='__pycache__' \
        {{local_path}}/ {{pi_user}}@{{pi_host}}:{{remote_path}}/
    output: "sync_result"
    
  - id: "install-deps"
    type: "bash"
    condition: "{{install_deps}} == 'true'"
    command: |
      ssh {{pi_user}}@{{pi_host}} 'cd {{remote_path}} && pip install -r requirements.txt'
      
  - id: "restart-service"
    type: "bash"
    condition: "{{service_name}} != ''"
    command: |
      ssh {{pi_user}}@{{pi_host}} 'sudo systemctl restart {{service_name}}'
```

**Use case:** `amplifier run "deploy to pi delmonte.local"`

---

### 2. Tool: `tool-pi-remote`

An MCP tool for Amplifier agents to interact with Raspberry Pi.

**Capabilities:**
- `pi_exec` - Run command on Pi via SSH
- `pi_sync` - Sync files to Pi (rsync)
- `pi_service` - Manage systemd services (start/stop/restart/status/logs)
- `pi_health` - Check Pi health (disk, memory, temp, connectivity)
- `pi_logs` - Tail/fetch logs from Pi

**Example tool schema:**
```python
@tool
async def pi_exec(
    host: str,           # Pi hostname or IP
    command: str,        # Command to run
    user: str = "pi",    # SSH user
    timeout: int = 30,   # Timeout in seconds
) -> str:
    """Execute a command on Raspberry Pi via SSH."""
    ...

@tool
async def pi_sync(
    host: str,
    local_path: str,
    remote_path: str,
    user: str = "pi",
    exclude: list[str] = None,
    delete: bool = False,
) -> str:
    """Sync local directory to Raspberry Pi using rsync."""
    ...

@tool  
async def pi_service(
    host: str,
    service: str,
    action: Literal["start", "stop", "restart", "status", "logs"],
    user: str = "pi",
) -> str:
    """Manage a systemd service on Raspberry Pi."""
    ...
```

---

### 3. Behavior: `embedded-dev`

A behavior bundle that provides embedded development capabilities.

```yaml
# behaviors/embedded-dev.yaml
bundle:
  name: embedded-dev-behavior
  version: 1.0.0
  description: Embedded device development workflow (Raspberry Pi, etc.)

tools:
  - module: tool-pi-remote
    source: git+https://github.com/microsoft/amplifier-foundation@main#subdirectory=modules/tool-pi-remote

agents:
  include:
    - foundation:pi-deployment-specialist

context:
  include:
    - foundation:context/embedded-dev-instructions.md
```

---

### 4. Agent: `pi-deployment-specialist`

A specialized agent for Raspberry Pi deployment and troubleshooting.

**Knowledge areas:**
- Raspberry Pi setup and configuration
- Raspberry Pi OS (Lite and Desktop)
- systemd service creation and management
- GPIO programming (RPi.GPIO, gpiozero)
- Audio configuration (ALSA, PulseAudio)
- WiFi/network troubleshooting
- Common Pi issues and solutions
- Power management and safe shutdown
- SD card management and backup

**Mode triggers:**
- "deploy to pi" → deployment workflow
- "set up service" → systemd creation
- "troubleshoot" → diagnostic mode

---

## Immediate Implementation for HelloHistory

While the full Amplifier components are future work, we can implement a lightweight version now:

### Phase 1: Local Development (Now)

```
HelloHistory/
├── src/
│   ├── bench_player.py      # Cross-platform test player ✅
│   ├── phone_player.py      # Pi-specific with GPIO (to create)
│   └── audio/               # Audio files ✅
├── deploy/
│   ├── deploy.sh            # Simple rsync + restart script
│   ├── hellohistory.service # systemd unit file
│   └── setup-pi.sh          # First-time Pi setup script
├── docs/
│   ├── BENCH_TESTING_GUIDE.md ✅
│   └── PI_DEPLOYMENT.md     # Deployment instructions
└── Makefile                 # Convenience commands
```

### Phase 2: Deploy Scripts

**`deploy/deploy.sh`** - One-command deployment:
```bash
#!/bin/bash
# Usage: ./deploy/deploy.sh [pi-host]

PI_HOST="${1:-delmonte.local}"
REMOTE_PATH="~/delmonte"

rsync -avz --delete \
  --exclude='.git' --exclude='venv' --exclude='__pycache__' \
  . pi@${PI_HOST}:${REMOTE_PATH}/

ssh pi@${PI_HOST} "sudo systemctl restart hellohistory"
```

**`deploy/hellohistory.service`** - systemd unit:
```ini
[Unit]
Description=HelloHistory Phone Player
After=sound.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/delmonte
ExecStart=/usr/bin/python3 /home/pi/delmonte/src/phone_player.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Phase 3: Makefile for Convenience

```makefile
.PHONY: test deploy logs ssh setup

PI_HOST ?= delmonte.local

# Run local test player
test:
	python3 src/bench_player.py

# Deploy to Pi
deploy:
	./deploy/deploy.sh $(PI_HOST)

# View Pi logs
logs:
	ssh pi@$(PI_HOST) 'journalctl -u hellohistory -f'

# SSH into Pi
ssh:
	ssh pi@$(PI_HOST)

# First-time Pi setup
setup:
	scp deploy/setup-pi.sh pi@$(PI_HOST):~/ && \
	ssh pi@$(PI_HOST) 'chmod +x setup-pi.sh && ./setup-pi.sh'
```

---

## Development Workflow

### Daily Development Cycle

1. **Edit locally** on Mac in your favorite editor
2. **Test locally** with `make test` (runs bench_player.py)
3. **Deploy to Pi** with `make deploy`
4. **Check logs** with `make logs`
5. **Iterate**

### First-Time Pi Setup

1. Flash SD card with Raspberry Pi Imager (configure WiFi/SSH)
2. Boot Pi and verify connectivity: `ping delmonte.local`
3. Run first-time setup: `make setup`
4. Deploy code: `make deploy`
5. Test on actual hardware

---

## Future: Full Amplifier Integration

Once this pattern proves useful, contribute back to Amplifier:

1. **Extract `tool-pi-remote`** as standalone module
2. **Create `pi-deploy` recipe** in amplifier-bundle-recipes
3. **Add `pi-deployment-specialist` agent** to foundation
4. **Document the pattern** for others

### Contribution Checklist

- [ ] Local scripts working for HelloHistory
- [ ] Pattern validated on real hardware
- [ ] Extract tool-pi-remote module
- [ ] Write recipe YAML
- [ ] Create agent definition
- [ ] Write documentation
- [ ] Submit PR to amplifier-foundation

---

## Questions to Resolve

1. **SSH key management** - Assume keys are set up, or help configure?
2. **Multiple Pis** - Support deploying to fleet of devices?
3. **Secrets management** - How to handle WiFi passwords, API keys?
4. **Rollback** - Keep previous version for quick rollback?
5. **Health checks** - Verify deployment succeeded?

---

## Summary

| Component | Scope | Status |
|-----------|-------|--------|
| bench_player.py | HelloHistory | ✅ Done |
| deploy.sh | HelloHistory | 📝 To create |
| systemd service | HelloHistory | 📝 To create |
| Makefile | HelloHistory | 📝 To create |
| tool-pi-remote | Amplifier | 🔮 Future |
| pi-deploy recipe | Amplifier | 🔮 Future |
| pi-specialist agent | Amplifier | 🔮 Future |
