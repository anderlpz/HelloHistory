# The Phone That Tells Stories

There's something about old phones.

They have weight. Presence. When you pick up a rotary handset, you're holding an object that was designed to be held—curved to fit against your ear, heavy enough to feel like it matters. Nobody ever absent-mindedly picked up a rotary phone.

I wanted to use that. I had a vintage phone and a story worth telling.

---

The house I was working on was designed in 1954 by Mary Lund Davis—the first licensed female architect in Washington State after World War II. She built it as her own home and office, a modernist experiment in the suburbs of Tacoma. Guests who stay there often ask about its history, and I'd been looking for a way to share Mary's story that felt right for the space.

A touchscreen kiosk wasn't it. Neither was a QR code linking to a website.

But what if you could pick up a phone and hear her story? No instructions, no interface. Just the gesture everyone already knows: lift the handset, put it to your ear, listen.

The idea was simple. Building it was another matter.

---

I should be honest about where I started: I had never worked with a Raspberry Pi. I didn't know what GPIO meant. The last time I'd touched anything resembling electronics was a high school science fair project that didn't work. I had no idea how the inside of a rotary phone was wired, or whether what I wanted was even possible.

What I did have was Amplifier—an AI tool I'd been using for software projects. And a hunch that the gap between "person who can't do hardware" and "person who built a hardware thing" might be smaller than it used to be.

---

The first conversation was just exploration. I described what I wanted: a phone that plays audio when you pick it up and stops when you hang up. What would that require?

The answer came back structured but not overwhelming: a Raspberry Pi as the brain, GPIO pins to detect the hook switch, a USB audio adapter for sound. A shopping list with links. An explanation of why Pi over Arduino—I needed audio playback, not just electronic signals.

I didn't have to spend a weekend researching "best microcontroller for audio projects" or parsing conflicting forum advice. I described the destination, and got a map.

This became the pattern. Not "how do I do X" but "I want Y to happen"—and then working backward together to figure out X.

---

The first real challenge wasn't technical. It was content.

Mary Lund Davis isn't famous. There's no Wikipedia article, no documentary. The best source is a 200-page academic thesis buried in the University of Washington library system.

I fed Amplifier the thesis and asked it to find the good stuff: her education, her career, the specific story of building this house, her later work designing affordable homes in the 1960s. It pulled out the threads, organized them into a knowledge base, and identified the moments that would make good narration.

Then it wrote the scripts. Seven chapters, about twelve minutes total, in a warm storyteller voice. We went back and forth on tone—less formal here, more detail there, let this moment breathe. The kind of editing you'd do with a human collaborator.

By the end, I had recording-ready scripts without having manually read 200 pages or stared at a blank document trying to write narration.

---

The Pi arrived in a box smaller than I expected.

There's a particular anxiety that comes with hardware. Software is forgiving—you can undo, revert, try again. Hardware feels permanent. You plug the wrong thing into the wrong place, and maybe something burns.

I started with the basics: flashing an operating system onto an SD card. Amplifier walked me through it, including details I wouldn't have thought to ask about—like configuring WiFi and SSH during the imaging process so the Pi would be accessible without a monitor.

First boot. Nothing visible—this was "headless," just a tiny computer drawing power somewhere in my house. I tried to connect from my laptop.

Connection refused.

The next twenty minutes were debugging. Was my laptop on the wrong WiFi network? Was the Pi's hostname resolving? We tried different approaches, checked different things. Eventually: `ping delmonte.local` succeeded, and I was in.

I was looking at a Linux command line on a computer I'd never touched, running an operating system I'd never configured, and somehow it was working.

---

Before any hardware integration, Amplifier did something I wouldn't have thought to ask for: it built a development workflow.

A Makefile appeared with commands like `make deploy` to push code to the Pi, `make logs` to see what was happening, `make restart` to restart the service. A "bench player" that runs on my laptop so I could test the audio logic without the actual hardware.

This is the kind of thing experienced developers do automatically—set up their environment before writing application code. I didn't know to ask for it. The AI understood that the meta-work matters as much as the work.

---

The moment I'll remember is the wiring.

I opened the phone and found seven wires connected to the hook switch—the mechanism that detects whether the handset is lifted. No labels. No documentation. Just colored wires: gray, yellow, orange, two whites, a brown, and another gray.

I described what I saw. Amplifier explained how hook switches typically work electrically, then wrote a test script to monitor GPIO pins for changes. It deployed the script to my Pi while I stood there holding wires.

"Touch the gray and yellow together."

Nothing.

"Try gray and orange."

Still nothing.

We kept going. Different combinations. Different theories. At some point, I just started lifting and lowering the handset while watching the output—and there it was. A signal change. The yellow wire.

This was something I hadn't experienced before with AI tools. I was physically manipulating hardware while the AI wrote code, deployed it to my device, watched the results with me, and suggested next steps. The feedback loop was seconds, not minutes. We were debugging together in real-time.

That's different from getting advice. Advice is "you should try checking the continuity between these wires." Partnership is standing next to someone while they hand you the multimeter.

---

The speaker was a happy accident.

I'd planned to use a small external speaker—something cheap from Amazon. But the phone had its original earpiece, and I wondered if it could work.

Two white wires ran to it. Amplifier explained the electrical considerations—impedance, power levels—but said it was worth trying. I used lever nuts to make the connection (no soldering, per recommendation for someone who'd never done this before).

It worked. The original 1960s speaker played the audio.

The sound quality isn't audiophile-grade. It's a little tinny, a little vintage. Which turned out to be exactly right—you're holding an old phone, and it sounds like an old phone. The imperfection became part of the experience.

---

Things broke along the way. Of course they did.

The audio disappeared after a reboot—volume settings weren't persisting. The Pi kept choosing the wrong sound card. A Python dependency was missing on the production device but not on my test setup.

Each bug was found and fixed in minutes. Not because the problems were trivial, but because the AI could actually look at logs, run commands, test fixes, and iterate. When you're debugging with something that can see what you see and do what you would do, problems shrink.

---

The last step was making it automatic. When the phone powers on, it should just work. No SSH required, no manual startup.

A systemd service file. An installation script. A Makefile command to set everything up: `make setup-service`.

Now the phone boots, connects to WiFi, starts listening for the hook switch, and waits. Pick up the handset, and Mary's story begins. Hang up, and it stops. Completely standalone.

---

I keep thinking about what actually happened here.

Two weeks. Zero hardware experience to start. A working product at the end—not a prototype, not a proof of concept, but something I can plug in and walk away from.

The obvious conclusion is "AI is powerful now," which is true but not quite right. What's actually different is the shape of the help.

Most AI tools give you answers. You ask a question, you get a response, you figure out what to do with it. The flow is: *you* act, AI advises, *you* act again.

What happened here was different. The AI didn't just advise—it did things. It wrote code and deployed it. It read logs and diagnosed problems. It created files and configured services. When I was holding wires and couldn't type, it ran the test script on my Pi and told me what happened.

The flow was: *we* act, together, in the same loop.

That's not a small difference. It's the difference between having a consultant who sends you a report and a collaborator who shows up at your workbench.

---

There's a philosophical thread here I want to pull on.

The phone project required research, writing, audio production, Python, Linux system administration, electronics, and hardware debugging. In a normal workflow, each of those is a different tool, a different context, a different headspace. You'd task-switch constantly. You'd lose momentum explaining the same background to different systems.

Having one collaborator that could help with all of it—and remember the context—changed how I thought about the project. I wasn't breaking it into "the software part" and "the hardware part" and "the content part." It was just *the project*, and we worked on whatever needed working on.

That's closer to how creative work actually feels in your head. Not compartmentalized. Just... the thing you're making.

---

The phone lives in the house now.

When guests pick it up, they hear about Mary Lund Davis—her education at the University of Washington, her struggle to be taken seriously in a male-dominated field, the story of building this exact house with materials from her family's mill. About twelve minutes if they listen to everything.

Most people don't listen to everything. They pick up, hear a few chapters, hang up. Maybe they come back later. That's fine. The phone isn't demanding attention. It's just there, holding a story, waiting for someone to pick it up.

There's something satisfying about that. A piece of technology that doesn't notify, doesn't require updates, doesn't ask for your email. It just does one thing, well, when you want it to.

Maybe that's the real lesson. Not about AI, but about what's worth building: things with presence, things with weight, things that wait quietly until they're needed.

The AI helped me build it. But the phone itself is stubbornly, beautifully analog.

---

*[HelloHistory](https://github.com/anderlpz/HelloHistory) is open source. Built with [Amplifier](https://github.com/microsoft/amplifier).*
