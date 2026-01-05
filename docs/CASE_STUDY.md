# HelloHistory

The phone is a 1960s ITT rotary. When you pick up the handset, you hear a story about the architect who designed this house. When you hang up, it stops. That's the whole interaction.

Building it required things I didn't know: Raspberry Pi configuration, GPIO wiring, Linux services, audio routing through 60-year-old speaker hardware. I figured it out with an AI that could do more than give advice.

This is a case study of that process—what I built, what I didn't know, and how the gap closed.

---

## The idea

The house was designed in 1954 by Mary Lund Davis, the first licensed female architect in Washington State after WWII. Guests often ask about its history. I wanted a way to tell her story that matched the character of the space.

A touchscreen kiosk wasn't it. Neither was a QR code. But a rotary phone—pick it up and listen—felt right. The gesture is self-explanatory. No instructions needed.

As a designer, I also wanted to express something of myself in the work: modifying an old piece of technology with something at the edge of innovation, crafting an artifact that gives guests a small moment of magic. The phone felt like the right vessel for that.

I had the concept. I did not have the skills to execute it.

## Starting point

I'd never worked with a Raspberry Pi. I didn't know what GPIO meant. I had no idea how the inside of a rotary phone was wired.

I started by describing what I wanted to Amplifier: a phone that plays audio when you pick it up and stops when you hang up. What would that require?

The answer was concrete: a Raspberry Pi for the brain, GPIO pins to detect the hook switch, a USB audio adapter for sound output. A shopping list with links. An explanation of why Pi over Arduino. I didn't have to research any of this myself. I described the destination and got a map.

## Content

Mary Lund Davis is well known and regarded for her contributions to Pacific Northwest modernism. Being part of this history—helping tell her story in the house she designed—was a privilege.

The primary source was [*Mary Lund Davis: A Portrait in Three Histories*](https://digital.lib.washington.edu/researchworks/items/75e69ac3-bc19-41fa-9c6e-ae27d7ab16d6), a thesis by Nevis Granum, Mary's grandson. We were fortunate to find it. It's a remarkable document—part architectural history, part family memoir—that enables us to really understand her thinking and expression. That's core to what makes history human. We also drew from other sources: articles, archives, records of her later work.

The thesis was a beautiful read on its own. The challenge was condensing all of this into something suited for the experience—a few minutes of narration through a phone handset. With Amplifier, I worked through the material: what mattered most, what would resonate, how to structure it. We built a knowledge base, then shaped the narration scripts—seven chapters, about twelve minutes total. We iterated on tone until it felt right.

## First contact with hardware

The Pi arrived. Amplifier walked me through flashing the OS, including details I wouldn't have thought to ask about—like configuring WiFi and SSH during imaging so the device would be accessible without a monitor.

First boot. I tried to connect. Connection refused.

We debugged together. Was my laptop on the wrong network? Was the hostname resolving? We tried different things until it worked. Then I was looking at a Linux command line on a computer I'd never touched.

Before any hardware integration, Amplifier set up a development workflow: `make deploy` to push code, `make logs` to see output, `make restart` to restart the service. It also built a version that runs on my Mac for testing without the Pi. I didn't ask for this infrastructure. The AI understood it was necessary.

## The wiring

This is the part I'll remember.

I opened the phone and found seven wires connected to the hook switch. No labels. No documentation. Gray, yellow, orange, two whites, a brown, and another gray.

I described what I saw. Amplifier explained how hook switches typically work, then wrote a test script to monitor GPIO pins. It deployed the script to my Pi while I stood there holding wires.

"Touch the gray and yellow together." Nothing.

"Try gray and orange." Nothing.

We kept going. Eventually I found it—the yellow wire triggered when the handset lifted.

I was physically holding wires while the AI wrote code, deployed it, and interpreted results. The feedback loop was seconds. We were debugging hardware together in real-time. That's different from getting advice.

## The speaker

I'd planned to use an external speaker. But the phone had its original earpiece, and I wondered if it could work.

Amplifier explained the considerations—impedance, power levels—but said it was worth trying. I wired it with lever nuts, no soldering.

It worked. The 1960s earpiece played the audio. The sound is a little tinny, a little vintage. Exactly right for an old phone telling an old story.

## The bugs

Things broke. Audio disappeared after reboots because volume settings weren't persisting. Linux kept choosing the wrong sound card. A Python dependency was missing on the Pi but not on my test setup.

Each bug was found and fixed in minutes. Not because the problems were simple, but because the AI could look at logs, run commands, and test fixes directly on the device. When you're debugging with something that can see what you see and act on what it learns, problems shrink.

## Production

The last step was making it automatic. When the phone powers on, the service should start without intervention.

Amplifier created a systemd service, an installation script, and a Makefile command to set it up. One command: `make setup-service`.

Now the phone boots, starts the listener, and waits. Pick up the handset, Mary's story begins. Hang up, it stops. Standalone.

---

## What made this work

A few things stand out.

**Cross-domain help.** This project required research, writing, audio production, Python, Linux administration, and hardware debugging. Having one tool that could help with all of it—and remember the context—made it tractable. I wasn't switching between specialized tools and re-explaining the project each time.

**Direct execution.** The AI didn't just tell me what to do. It wrote code, deployed it, read the output, and adjusted. When I was holding wires and couldn't type, it ran tests on my Pi and told me what happened. That tight loop is the difference between a 15-minute debugging session and an afternoon of frustration.

**Building the scaffolding.** I didn't just get application code. I got Makefiles, deploy scripts, service configurations. The infrastructure that makes a project maintainable. I wouldn't have known to build it myself.

## The result

A vintage rotary phone that plays 12 minutes of narration about Mary Lund Davis, uses the original earpiece speaker, starts automatically on power-on, and can be updated remotely over WiFi.

Built by someone who, two weeks earlier, had never configured a Raspberry Pi.

---

## The property

The phone lives at the Del Monte house, a mid-century modern rental in Fircrest, Washington. [midcenturypnw](https://linktr.ee/midcenturypnw)

## About Amplifier

Amplifier is an open-source AI agent framework from the Research Team at Microsoft. Unlike chat-based AI tools, it can take actions—write files, run commands, deploy code, debug in real-time. That's what made this project possible for someone without hardware experience.

[github.com/microsoft/amplifier](https://github.com/microsoft/amplifier)

---

*Source code: [github.com/anderlpz/HelloHistory](https://github.com/anderlpz/HelloHistory)*

*Disclosure: I'm a member of the Amplifier team at Microsoft.*
