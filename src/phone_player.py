#!/usr/bin/env python3
"""
Del Monte Phone Player - Production Version
Starts automatically on boot, plays audio when handset is lifted.
"""
import gpiod
import time
import subprocess
import logging
from gpiod.line import Direction, Bias

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler("/home/pi/delmonte/logs/phone.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("phone")

AUDIO_DIR = "/home/pi/delmonte/src/audio"
VOLUME_PERCENT = 60  # Set volume level (0-100)
TRACKS = [
    "00_intro.mp3",
    "01_welcome.mp3",
    "02_marys_story.mp3",
    "03_building.mp3",
    "04_design.mp3",
    "05_other_work.mp3",
    "06_closing.mp3",
    "07_song.mp3",
]

class PhonePlayer:
    def __init__(self):
        self.chip = gpiod.Chip("/dev/gpiochip0")
        self.request = self.chip.request_lines(
            consumer="phone_player",
            config={17: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP)}
        )
        self.process = None
        self.current_track = 0
        self.set_volume(VOLUME_PERCENT)
        log.info("Phone player initialized")
    
    def set_volume(self, percent):
        """Set system volume to specified percentage"""
        try:
            subprocess.run(["amixer", "set", "Speaker", f"{percent}%"], 
                         capture_output=True, check=True)
            log.info(f"Volume set to {percent}%")
        except Exception as e:
            log.warning(f"Could not set volume: {e}")
    
    def is_lifted(self):
        return self.request.get_value(17) == gpiod.line.Value.ACTIVE
    
    def play_track(self, index):
        self.stop_audio()
        self.current_track = index
        path = f"{AUDIO_DIR}/{TRACKS[index]}"
        log.info(f"Playing: {TRACKS[index]}")
        self.process = subprocess.Popen(["mpg123", "-q", path])
    
    def stop_audio(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=0.5)
            except:
                self.process.kill()
            self.process = None
    
    def check_track_ended(self):
        if self.process and self.process.poll() is not None:
            self.current_track += 1
            if self.current_track < len(TRACKS):
                self.play_track(self.current_track)
            else:
                log.info("Playlist complete")
                self.current_track = 0
                self.process = None
    
    def run(self):
        log.info("Phone player running - waiting for handset")
        was_lifted = False
        
        while True:
            try:
                lifted = self.is_lifted()
                
                if lifted and not was_lifted:
                    log.info("Handset LIFTED")
                    self.play_track(0)
                elif not lifted and was_lifted:
                    log.info("Handset HUNG UP")
                    self.stop_audio()
                    self.current_track = 0
                
                if lifted:
                    self.check_track_ended()
                
                was_lifted = lifted
                time.sleep(0.1)
                
            except Exception as e:
                log.error(f"Error: {e}")
                time.sleep(1)
    
    def cleanup(self):
        self.stop_audio()
        self.request.release()
        log.info("Phone player stopped")

if __name__ == "__main__":
    player = PhonePlayer()
    try:
        player.run()
    except KeyboardInterrupt:
        log.info("Shutting down...")
    finally:
        player.cleanup()
