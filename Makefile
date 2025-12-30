# HelloHistory Makefile
# Development and deployment commands for the rotary phone audio player
#
# Usage:
#   make test          # Run local test player (Mac)
#   make deploy        # Deploy to Raspberry Pi
#   make logs          # View Pi service logs
#   make ssh           # SSH into Pi
#

# Configuration
PI_HOST ?= delmonte.local
PI_USER ?= pi
REMOTE_PATH ?= /home/pi/delmonte

# ============================================================================
# Local Development
# ============================================================================

.PHONY: test
test: ## Run the bench test player locally (Mac)
	@echo "Starting bench player..."
	@echo "Controls: SPACE=play/pause, 0-7=chapters, Q=quit"
	@echo ""
	python3 src/bench_player.py

.PHONY: test-audio
test-audio: ## Quick test of audio playback
	@echo "Playing intro track..."
	afplay src/audio/00_intro.mp3

# ============================================================================
# Deployment
# ============================================================================

.PHONY: deploy
deploy: ## Deploy code to Raspberry Pi
	@chmod +x deploy/deploy.sh
	@./deploy/deploy.sh $(PI_HOST)

.PHONY: sync
sync: ## Sync files to Pi without restarting service
	rsync -avz --delete \
		--exclude='.git' --exclude='venv' --exclude='__pycache__' \
		--exclude='*.pyc' --exclude='.DS_Store' --exclude='.amplifier' \
		./src/ $(PI_USER)@$(PI_HOST):$(REMOTE_PATH)/src/

# ============================================================================
# Pi Setup (First Time)
# ============================================================================

.PHONY: setup
setup: ## Run first-time Pi setup (installs deps, configures audio)
	@echo "Copying setup script to Pi..."
	scp deploy/setup-pi.sh $(PI_USER)@$(PI_HOST):~/
	@echo "Running setup on Pi..."
	ssh $(PI_USER)@$(PI_HOST) 'chmod +x ~/setup-pi.sh && ~/setup-pi.sh'

.PHONY: setup-service
setup-service: ## Install/update the systemd service on Pi
	@echo "Installing systemd service..."
	scp deploy/hellohistory.service $(PI_USER)@$(PI_HOST):/tmp/
	ssh $(PI_USER)@$(PI_HOST) '\
		sudo cp /tmp/hellohistory.service /etc/systemd/system/ && \
		sudo systemctl daemon-reload && \
		sudo systemctl enable hellohistory && \
		echo "Service installed and enabled"'

# ============================================================================
# Service Management
# ============================================================================

.PHONY: start
start: ## Start the HelloHistory service on Pi
	ssh $(PI_USER)@$(PI_HOST) 'sudo systemctl start hellohistory'
	@echo "Service started"

.PHONY: stop
stop: ## Stop the HelloHistory service on Pi
	ssh $(PI_USER)@$(PI_HOST) 'sudo systemctl stop hellohistory'
	@echo "Service stopped"

.PHONY: restart
restart: ## Restart the HelloHistory service on Pi
	ssh $(PI_USER)@$(PI_HOST) 'sudo systemctl restart hellohistory'
	@echo "Service restarted"

.PHONY: status
status: ## Check service status on Pi
	@ssh $(PI_USER)@$(PI_HOST) 'systemctl status hellohistory' || true

.PHONY: logs
logs: ## Tail the service logs from Pi (Ctrl+C to stop)
	ssh $(PI_USER)@$(PI_HOST) 'journalctl -u hellohistory -f'

.PHONY: logs-recent
logs-recent: ## Show last 50 log lines
	ssh $(PI_USER)@$(PI_HOST) 'journalctl -u hellohistory -n 50'

# ============================================================================
# Pi Remote Access
# ============================================================================

.PHONY: ssh
ssh: ## SSH into the Raspberry Pi
	ssh $(PI_USER)@$(PI_HOST)

.PHONY: ping
ping: ## Check if Pi is reachable
	@ping -c 3 $(PI_HOST) && echo "✓ Pi is reachable" || echo "✗ Pi not found"

.PHONY: pi-info
pi-info: ## Show Pi system info (temp, disk, memory)
	@ssh $(PI_USER)@$(PI_HOST) '\
		echo "═══ System Info ═══" && \
		echo "Hostname: $$(hostname)" && \
		echo "Uptime: $$(uptime -p)" && \
		echo "" && \
		echo "═══ Temperature ═══" && \
		vcgencmd measure_temp && \
		echo "" && \
		echo "═══ Disk Usage ═══" && \
		df -h / && \
		echo "" && \
		echo "═══ Memory ═══" && \
		free -h'

# ============================================================================
# Audio Testing on Pi
# ============================================================================

.PHONY: pi-test-audio
pi-test-audio: ## Test audio output on Pi
	@echo "Playing test tone on Pi..."
	ssh $(PI_USER)@$(PI_HOST) 'speaker-test -t sine -f 440 -c 1 -l 1'

.PHONY: pi-volume
pi-volume: ## Open audio mixer on Pi
	ssh -t $(PI_USER)@$(PI_HOST) 'alsamixer'

# ============================================================================
# Help
# ============================================================================

.PHONY: help
help: ## Show this help message
	@echo "HelloHistory - Development Commands"
	@echo ""
	@echo "Usage: make [target] [PI_HOST=hostname]"
	@echo ""
	@echo "Examples:"
	@echo "  make test                    # Run local test player"
	@echo "  make deploy                  # Deploy to delmonte.local"
	@echo "  make deploy PI_HOST=10.0.0.5 # Deploy to specific IP"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
