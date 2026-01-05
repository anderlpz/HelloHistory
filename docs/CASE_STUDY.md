# HelloHistory Case Study

## How I Built a Hardware Product with No Hardware Experience

I wanted to turn a vintage rotary phone into an interactive storytelling device. When guests at our rental property pick up the handset, they'd hear the story of Mary Lund Davis—the architect who designed the house in 1954.

The problem: I'd never worked with a Raspberry Pi. I didn't know GPIO from HDMI. I hadn't touched a soldering iron since high school. And I had no idea how the internals of a rotary phone worked.

Two weeks later, I had a working product.

This is how that happened.

---

## The Idea

The Del Monte house was designed by Mary Lund Davis, the first licensed female architect in Washington State after WWII. Guests often ask about the home's history, and I wanted a way to tell Mary's story that felt special—something that matched the mid-century character of the house.

A vintage rotary phone felt right. Pick it up, hear a story. No screens, no apps, no instructions needed.

But I had no idea how to actually build it.

---

## Starting From Zero

I started by asking Amplifier what I'd need. Not "how do I build this"—just "what would this require?"

The response was a project plan: Raspberry Pi for the brain, GPIO pins to detect when the handset lifts, USB audio adapter for sound output. A shopping list with specific components and links. An explanation of why Pi over Arduino (I needed audio playback, not just signals).

I didn't have to research "Raspberry Pi vs Arduino for audio projects" or wade through forum posts. I described what I wanted, and got a concrete plan.

**First lesson:** Having an AI that understood the full problem—not just code—meant I could skip weeks of research.

---

## The Knowledge Problem

Mary Lund Davis isn't famous. There's no Wikipedia page. The best source is a 200-page academic thesis from the University of Washington.

I gave Amplifier the thesis and asked it to extract everything relevant: her education, her career, the story of building this specific house, her later work. It pulled out the key facts, organized them into a biography document, and identified the most compelling stories for the narration.

Then it wrote the scripts. Seven chapters, about 12 minutes total, in a warm narrator voice. We iterated on tone and pacing until it felt right.

**What this meant:** I went from "there's a thesis somewhere" to "here are recording-ready scripts" without manually reading 200 pages or struggling to write narration myself.

---

## First Contact with Hardware

The Pi arrived. I'd never flashed an SD card with an operating system before.

Amplifier walked me through it: download Raspberry Pi Imager, select the OS, configure WiFi and SSH during imaging so the Pi would be accessible headless (no monitor). Even small details—like naming the Pi `delmonte.local` so I could find it on the network.

When I couldn't connect after booting, we debugged together. Was my laptop on the wrong WiFi network? (Yes.) Was the Pi's hostname resolving? (Not at first.) We tried different approaches until `ping delmonte.local` succeeded.

Then I was in via SSH, looking at a Linux command line on a tiny computer I'd never touched.

---

## Building the Development Workflow

Before touching hardware, Amplifier set up a development workflow:

```
make deploy    → Push code to Pi
make logs      → See what's happening
make restart   → Restart the service
make ssh       → Connect to Pi
```

It also created a "bench player"—a version of the audio player that runs on my Mac, so I could test the playlist logic without the Pi. When I made changes, I'd test locally first, then `make deploy` to push to the actual device.

**Why this mattered:** I wasn't just getting code. I was getting the infrastructure to iterate quickly. Every hardware project needs this, but I wouldn't have known to build it myself.

---

## The Audio Puzzle

The audio files needed to go somewhere. I had scripts, but needed actual recordings.

Amplifier created a workflow for ElevenLabs (text-to-speech): a Python script that takes the chapter text and generates MP3s with the right voice settings. It handled the API integration, file naming, and output organization.

Later, when I re-recorded everything as a single file and needed to split it by chapter, Amplifier wrote the splitting logic based on timestamps I provided.

**The pattern:** Every time I hit a sub-problem, we solved it together—not by me googling "how to split mp3 by timestamp python" but by describing what I needed and getting working code.

---

## The Wiring Challenge

Here's where it got interesting.

I needed to detect when the handset lifts. That meant finding the "hook switch"—the mechanism that knows whether the phone is on-hook or off-hook. I opened the phone and found... seven wires. No labels. No documentation.

I described what I saw: "Gray, yellow, orange, two whites, a brown, and another gray."

Amplifier explained what hook switches typically look like electrically, then wrote a test script that monitors GPIO pins for changes. It deployed the script to my Pi, and I started testing.

"Touch the gray and yellow wires together."

Nothing.

"Try gray and orange."

Nothing.

"What happens when you just lift and lower the handset while watching the output?"

I found it—the yellow wire, completing a circuit when the handset lifted.

**This was the moment I understood the difference.** I was physically holding wires while the AI wrote code, deployed it to my device, and interpreted the results. The feedback loop was seconds, not minutes. We were debugging hardware together in real-time.

---

## The Speaker Surprise

The plan was to use a small external speaker. But when I looked at the phone's original earpiece, I wondered: could I use that instead?

Two white wires ran to the earpiece. I asked if I could connect them to the audio output.

Amplifier explained the electrical considerations—impedance matching, power levels—but said it should work for testing. I wired it up with lever nuts (no soldering, per recommendation for a first hardware project).

It worked. The original 1960s earpiece speaker played the audio. The sound quality wasn't perfect, but it was authentic—exactly right for a vintage phone telling a vintage story.

---

## The Bugs

Things didn't always work the first time.

**Audio disappeared after reboot.** The volume settings weren't persisting. Amplifier checked `amixer`, found the issue, and added volume configuration to the startup script.

**Wrong audio device.** Linux saw multiple sound cards and was using the wrong one. Amplifier SSH'd in, ran `aplay -l` to list devices, and updated the config to target the USB adapter specifically.

**Service wouldn't start.** A Python dependency was missing. Amplifier checked the logs, identified the missing package, and updated the setup script.

Each bug was found and fixed in minutes. Not because the problems were simple—but because the AI could actually look at logs, run commands, and test fixes directly on the device.

---

## Going to Production

The final step: making it work automatically. When the phone powers on, the service should start. No manual intervention.

Amplifier created a systemd service file, wrote an installation script, and added a Makefile command to set it up. One command: `make setup-service`.

Now the phone boots, connects to WiFi, starts the listener service, and waits for someone to pick up the handset. Completely standalone.

---

## The Result

A vintage rotary phone that:
- Plays 8 chapters of narration about Mary Lund Davis (~12 minutes)
- Uses the original earpiece speaker
- Detects handset lift/hangup via GPIO
- Starts automatically on power-on
- Can be updated remotely over WiFi

Built by someone who, two weeks earlier, had never configured a Raspberry Pi.

---

## What Made This Possible

Looking back, several things stand out:

**Cross-domain help.** This project required research, writing, audio production, Python, Linux administration, electronics, and hardware debugging. Switching between specialized tools for each domain would have been exhausting. Having one AI that could help with all of it—and remember the context—made it tractable.

**Direct execution.** The AI didn't just tell me what commands to run. It ran them, saw the output, and adjusted. When debugging the hook switch, it wrote test scripts, deployed them to my Pi, and iterated with me in real-time. That tight loop is the difference between a 15-minute debugging session and an afternoon of frustration.

**Building the scaffolding.** I didn't just get application code. I got Makefiles, deploy scripts, service configurations, and documentation. The meta-work that makes a project maintainable.

**Not being blocked.** Every time I hit something I didn't know—ALSA audio configuration, systemd service files, GPIO pull-up resistors—we figured it out together. I never had to stop and spend an hour researching before continuing.

---

## The Takeaway

I built a hardware product with no hardware experience. Not because the AI did it for me, but because it did it with me.

There's a difference between an AI that says "you should use a pull-up resistor on the GPIO pin" and one that writes the code, deploys it, sees it's not working, and says "let's try a different pin."

The first is advice. The second is partnership.

---

## Project Links

- [HelloHistory on GitHub](https://github.com/anderlpz/HelloHistory)
- [Amplifier](https://github.com/microsoft/amplifier)
