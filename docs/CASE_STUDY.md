# HelloHistory Case Study

## Building Hardware with an AI That Can Actually Do Things

**Project:** A vintage rotary phone that plays stories about architect Mary Lund Davis when guests lift the handset.

**Built with:** [Amplifier](https://github.com/microsoft/amplifier)

**Timeline:** ~2 weeks from concept to working product

**Starting point:** Zero Raspberry Pi experience

---

## The Question This Case Study Answers

> "Cool project, but what made Amplifier different? Couldn't you do this with ChatGPT/Claude/Copilot?"

Short answer: **No.** Here's why.

---

## What Made Amplifier Different

### 1. Agentic Execution, Not Conversational Advice

**The difference:** ChatGPT tells you what to do. Amplifier does it.

**Real example from this project:**

When debugging the hook switch, I had 7 mystery wires and no documentation. With ChatGPT, the workflow would be:

```
1. Ask ChatGPT for a test script
2. Copy the code from the chat
3. Open terminal, SSH to Pi
4. Create file, paste code
5. Run script, see output
6. Copy output back to ChatGPT
7. "Try the gray wire instead"
8. Repeat steps 2-7 for each wire pair
```

That's ~3 minutes per iteration. With 7 wires and multiple combinations, we're talking an hour of copy-paste.

**With Amplifier:**

```
Me: "None of the wires are triggering"
Amplifier: [writes hooktest.py, deploys via SSH, runs it]
Amplifier: "Touch the gray and yellow wires together"
Me: "It works!"
Amplifier: [updates phone_player.py with correct pins, deploys, restarts service]
```

The entire debugging session—from mystery wires to working hook detection—took 15 minutes. The AI wrote code, deployed it to my Pi, watched me test physically, and iterated in real-time.

**This is the fundamental difference:** Amplifier has hands, not just a mouth.

---

### 2. Cross-Domain Work Without Switching Tools

This project required:

| Domain | What We Did |
|--------|-------------|
| Research | Extracted Mary's biography from a 200-page academic thesis |
| Writing | Created 7 narration scripts in a warm storyteller voice |
| Audio Engineering | Built ElevenLabs automation, split recordings by timestamp |
| Python Development | GPIO detection, audio playback, state management |
| Linux Administration | systemd services, ALSA configuration, auto-start |
| DevOps | Makefile, deploy scripts, SSH automation |
| Hardware | Wire identification, soldering alternatives, speaker routing |
| Documentation | Project specs, guides, this case study |

**With typical AI tools:** You'd use ChatGPT for research, Copilot for code, separate terminals for deployment, and lose context every time you switch.

**With Amplifier:** One continuous conversation over 2 weeks. When I asked about ALSA configuration, the AI already knew I was using a USB audio adapter connected to the phone's original earpiece speaker, because it had helped me wire it days earlier.

---

### 3. Persistent Project Memory

The `.amplifier/AGENTS.md` file stores project context that persists across sessions.

**What this meant in practice:**

- **Day 3:** "The audio should play through the original earpiece"
- **Day 8:** (new session) "The speaker sounds quiet"
- Amplifier already knows: USB adapter → 3.5mm → lever nuts → original earpiece. Suggests `amixer` settings, not "what speaker are you using?"

Other tools start fresh. Every. Single. Session.

---

### 4. Real-Time Hardware Debugging

This was the most impressive part. Hardware debugging requires a tight loop:

```
Hypothesis → Test → Observe → Adjust
```

The AI needs to see what's happening in real-time. With Amplifier:

1. **Audio not working?** SSH in, check `aplay -l`, see card numbering, fix ALSA config, test—all in one exchange.

2. **Hook switch wiring unknown?** Write GPIO test script, deploy, watch me physically test wires, identify the correct pair, update production code.

3. **Volume too low after reboot?** Check if `amixer` settings persist, create startup script, add to systemd service.

**The AI was debugging hardware with me in real-time.** Not giving me a troubleshooting guide—actually running commands on my Pi while I held wires.

---

### 5. Complete Workflow Creation

Amplifier didn't just write `phone_player.py`. It created an entire development ecosystem:

```
Makefile           → 15+ commands (deploy, logs, ssh, restart...)
deploy/deploy.sh   → Smart rsync with connection checking  
deploy/setup-pi.sh → First-time Pi provisioning
setup-service.sh   → systemd service installation
bench_player.py    → Mac testing without hardware
```

When I said "I want to test changes quickly," the AI didn't just explain how—it built the infrastructure, tested it, and documented it.

---

## What Would This Look Like Without Amplifier?

### Option A: ChatGPT + Manual Everything

- Research biography → Copy text back and forth
- Write scripts → Copy to files manually
- Generate audio → Separate ElevenLabs workflow
- Write Python → Copy-paste into SSH terminal
- Debug GPIO → 3 minutes per iteration, dozens of iterations
- Configure systemd → Google each step, copy commands

**Estimated time:** 2-3 months of evenings
**Friction:** Constant context-switching, copy-paste errors, lost context between sessions

### Option B: Cursor/Copilot for Code + Other Tools

Better for the Python parts, but:
- Can't SSH to Pi
- Can't run deployment commands
- Can't debug hardware in real-time
- Can't write narration scripts in the same context
- Still need separate tools for non-code work

### Option C: Amplifier

Everything in one place. AI that executes, not just advises. Context that persists. Real-time hardware debugging.

**Actual time:** ~2 weeks
**Friction:** Minimal—tell it what you want, it does it

---

## Concrete Examples

### Example 1: The Hook Switch Debugging Session

**The problem:** 7 wires from the hook switch, no documentation, need to find which pair detects handset lift.

**What happened:**

```
Me: "The hook switch has 7 wires, I don't know which ones to use"

Amplifier: [creates hooktest.py that monitors all GPIO pins]
Amplifier: [deploys to Pi via SSH]
Amplifier: "Run this and tell me what you see when you lift the handset"

Me: "Nothing changes"

Amplifier: "The wires might not be connected to GPIO yet. 
           Can you describe the wire colors?"

Me: "Gray, yellow, orange, two whites, brown, and one more gray"

Amplifier: [creates continuity test script]
Amplifier: "Touch the gray and yellow together"

Me: "It shows 'ACTIVE (low)' now!"

Amplifier: [updates phone_player.py to use correct GPIO pin]
Amplifier: [deploys and restarts service]
Amplifier: "Try lifting the handset now"

Me: "It works!"
```

**Total time:** 15 minutes
**With copy-paste workflow:** 1+ hours

---

### Example 2: Audio Configuration Debugging

**The problem:** Audio works from command line but not from Python script.

**What happened:**

```
Amplifier: [SSHs to Pi, runs `aplay -l`]
Amplifier: "Card 1 is your USB adapter. Let me check the Python code..."
Amplifier: [reads phone_player.py, spots the issue]
Amplifier: "The script is using the default ALSA device. I'll update it to target card 1."
Amplifier: [edits code, deploys, restarts service]
Amplifier: "Try now"

Me: "Still nothing"

Amplifier: [checks `amixer` settings]
Amplifier: "Speaker volume is at 40%. Setting to 100%."
Amplifier: [runs amixer command, tests with aplay]
Amplifier: "You should hear a test tone"

Me: "Yes!"

Amplifier: [adds volume setting to startup script so it persists across reboots]
```

---

### Example 3: Building the Dev Workflow

**The problem:** Deploying changes is tedious.

**What I said:** "I want a simple way to push changes and restart the service"

**What Amplifier created:**

```makefile
# Makefile
deploy:              # Push code to Pi
	./deploy/deploy.sh
	
logs:                # View live logs
	ssh pi@$(PI_HOST) 'journalctl -u hellohistory -f'
	
restart:             # Restart service
	ssh pi@$(PI_HOST) 'sudo systemctl restart hellohistory'
	
ssh:                 # Connect to Pi
	ssh pi@$(PI_HOST)

status:              # Check service status
	ssh pi@$(PI_HOST) 'sudo systemctl status hellohistory'
```

Plus `deploy.sh` with connection checking, `setup-service.sh` for systemd installation, and documentation for the whole workflow.

I didn't ask for all of this. The AI understood "simple way to push changes" meant building proper developer tooling.

---

## The Technical Result

A standalone device that:
- Starts automatically on power-on
- Plays audio when handset is lifted
- Stops when handset is replaced  
- Uses the phone's original 1960s speaker
- Requires no network to operate
- Can be updated remotely when on WiFi

Built by someone with zero Raspberry Pi experience, in 2 weeks, with an AI that could actually help—not just advise.

---

## Why This Matters

The gap between "AI that gives advice" and "AI that takes action" is enormous.

Advice: "You should use gpiod to monitor the GPIO pin for falling edges"

Action: *Writes the code, deploys it, tests it, fixes the bug, deploys again*

Amplifier is the difference between having a consultant who sends you a PDF and a teammate who sits next to you and does the work with you.

---

## Try It Yourself

HelloHistory is open source. The real artifact isn't the phone—it's the workflow:

1. **Research phase** with AI that can read documents and extract knowledge
2. **Content creation** with AI that writes and iterates on scripts
3. **Development** with AI that writes, tests, and deploys code
4. **Hardware integration** with AI that debugs in real-time
5. **Production** with AI that creates proper infrastructure

This is what building with Amplifier feels like. Not "AI-assisted"—AI-partnered.

---

## Links

- [Amplifier](https://github.com/microsoft/amplifier) - The framework
- [HelloHistory](https://github.com/anderlpz/HelloHistory) - This project
