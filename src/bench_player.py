#!/usr/bin/env python3
"""
Del Monte HelloHistory - Bench Testing Player

Keyboard-controlled audio player for testing without the physical phone.
Simulates hook switch and rotary dial with keyboard input.

Controls:
    SPACE   - Toggle play/pause (simulates hook switch)
    0       - Restart from intro
    1-6     - Jump to chapter 1-6
    7       - Play the song
    Q       - Quit

Usage:
    python3 bench_player.py

Requirements:
    pip install pygame

Note: This script requires a terminal that can capture keyboard input.
      Run directly in a terminal, not through an IDE.
"""

import sys
import time
import select
import termios
import tty
from pathlib import Path
from enum import Enum, auto

# Check for pygame before importing
try:
    import pygame
except ImportError:
    print("Error: pygame not installed")
    print("Install with: pip install pygame")
    print("Or on Pi: sudo apt install python3-pygame")
    sys.exit(1)


class State(Enum):
    IDLE = auto()      # "On hook" - not playing
    PLAYING = auto()   # "Off hook" - playing audio


class BenchPlayer:
    """
    Keyboard-controlled audio player for bench testing.
    Simulates the phone behavior without GPIO.
    """
    
    def __init__(self, audio_dir: Path):
        self.audio_dir = audio_dir
        self.state = State.IDLE
        self.current_track = 0
        
        # Track list in playback order
        self.tracks = [
            ("00_intro.mp3", "Intro"),
            ("01_welcome.mp3", "Chapter 1: Welcome to Del Monte"),
            ("02_marys_story.mp3", "Chapter 2: Mary's Story"),
            ("03_building.mp3", "Chapter 3: Building Del Monte"),
            ("04_design.mp3", "Chapter 4: The Design Philosophy"),
            ("05_other_work.mp3", "Chapter 5: Her Other Work"),
            ("06_closing.mp3", "Chapter 6: Closing"),
            ("07_song.mp3", "Bonus: Song"),
        ]
        
        # Validate audio files exist
        missing = []
        for filename, name in self.tracks:
            if not (self.audio_dir / filename).exists():
                missing.append(filename)
        
        if missing:
            print(f"Warning: Missing audio files: {missing}")
            print(f"Looking in: {self.audio_dir.absolute()}")
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Store original terminal settings for restoration
        self.old_settings = None
    
    def print_status(self):
        """Print current player status."""
        state_str = "PLAYING" if self.state == State.PLAYING else "IDLE"
        track_name = self.tracks[self.current_track][1] if self.state == State.PLAYING else "(none)"
        
        # Clear line and print status
        print(f"\r[{state_str}] {track_name:<50}", end="", flush=True)
    
    def print_help(self):
        """Print control help."""
        print("\n" + "=" * 60)
        print("Del Monte HelloHistory - Bench Testing Player")
        print("=" * 60)
        print("\nControls:")
        print("  SPACE  - Pick up / Hang up (toggle playback)")
        print("  0      - Restart from intro")
        print("  1-6    - Jump to chapter")
        print("  7      - Play the song")
        print("  Q      - Quit")
        print("\nTrack listing:")
        for i, (filename, name) in enumerate(self.tracks):
            key = str(i) if i < 8 else "-"
            exists = "✓" if (self.audio_dir / filename).exists() else "✗"
            print(f"  [{key}] {exists} {name}")
        print("\n" + "-" * 60)
        print("Status: ", end="")
    
    def on_pick_up(self):
        """Simulate picking up the phone - start playback."""
        if self.state == State.IDLE:
            self.state = State.PLAYING
            self.current_track = 0
            self.play_current()
            print("\n📞 Phone picked up - starting playback")
            self.print_status()
    
    def on_hang_up(self):
        """Simulate hanging up - stop playback."""
        if self.state == State.PLAYING:
            pygame.mixer.music.stop()
            self.state = State.IDLE
            self.current_track = 0
            print("\n📞 Phone hung up - stopped")
            self.print_status()
    
    def toggle_hook(self):
        """Toggle between picked up and hung up."""
        if self.state == State.IDLE:
            self.on_pick_up()
        else:
            self.on_hang_up()
    
    def jump_to_chapter(self, number: int):
        """Jump to a specific chapter."""
        if self.state != State.PLAYING:
            print("\n⚠️  Pick up phone first (press SPACE)")
            return
        
        if 0 <= number <= 7:
            pygame.mixer.music.stop()
            self.current_track = number
            self.play_current()
            print(f"\n⏭️  Jumped to: {self.tracks[number][1]}")
            self.print_status()
        else:
            print(f"\n⚠️  Invalid chapter: {number}")
    
    def play_current(self):
        """Play the current track."""
        if self.current_track >= len(self.tracks):
            # End of playlist - loop back
            print("\n🔄 End of playlist - looping back to intro")
            self.current_track = 0
        
        filename, name = self.tracks[self.current_track]
        track_path = self.audio_dir / filename
        
        if track_path.exists():
            try:
                pygame.mixer.music.load(str(track_path))
                pygame.mixer.music.play()
            except pygame.error as e:
                print(f"\n❌ Error playing {filename}: {e}")
        else:
            print(f"\n❌ File not found: {track_path}")
            # Try to advance to next track
            self.current_track += 1
            if self.current_track < len(self.tracks):
                self.play_current()
    
    def check_track_ended(self):
        """Check if current track finished, advance to next."""
        if self.state == State.PLAYING and not pygame.mixer.music.get_busy():
            self.current_track += 1
            if self.current_track < len(self.tracks):
                print(f"\n▶️  Next: {self.tracks[self.current_track][1]}")
            self.play_current()
            self.print_status()
    
    def get_key(self):
        """Non-blocking keyboard read."""
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None
    
    def run(self):
        """Main loop."""
        self.print_help()
        self.print_status()
        
        # Set terminal to raw mode for single-key input
        self.old_settings = termios.tcgetattr(sys.stdin)
        
        try:
            tty.setcbreak(sys.stdin.fileno())
            
            while True:
                # Check for keyboard input
                key = self.get_key()
                
                if key:
                    key = key.lower()
                    
                    if key == 'q':
                        print("\n\n👋 Goodbye!")
                        break
                    elif key == ' ':
                        self.toggle_hook()
                    elif key in '01234567':
                        self.jump_to_chapter(int(key))
                
                # Check if track ended
                self.check_track_ended()
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted - goodbye!")
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            pygame.mixer.quit()


def main():
    # Determine audio directory
    # Try relative path first (for running from project root)
    audio_dir = Path("audio")
    
    if not audio_dir.exists():
        # Try src/audio (running from project root on dev machine)
        audio_dir = Path("src/audio")
    
    if not audio_dir.exists():
        # Try ~/delmonte/audio (typical Pi deployment)
        audio_dir = Path.home() / "delmonte" / "audio"
    
    if not audio_dir.exists():
        # Try same directory as script
        audio_dir = Path(__file__).parent / "audio"
    
    if not audio_dir.exists():
        print(f"Error: Cannot find audio directory")
        print("Tried: audio/, src/audio/, ~/delmonte/audio/")
        print("\nMake sure audio files are in one of these locations.")
        sys.exit(1)
    
    print(f"Using audio directory: {audio_dir.absolute()}")
    
    player = BenchPlayer(audio_dir)
    player.run()


if __name__ == "__main__":
    main()
