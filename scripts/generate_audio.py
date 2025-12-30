#!/usr/bin/env python3
"""
HelloHistory - ElevenLabs Audio Generator

Automates audio generation from voice-track text files using the ElevenLabs API.

Setup:
    1. Get API key from https://elevenlabs.io/app/settings/api-keys
    2. Set environment variable:
       export ELEVENLABS_API_KEY="your-key-here"
    3. Install SDK:
       pip install elevenlabs pyyaml

Usage:
    # Generate a single chapter
    python3 scripts/generate_audio.py 01_welcome

    # Generate all chapters
    python3 scripts/generate_audio.py --all

    # List available voices
    python3 scripts/generate_audio.py --list-voices

    # Preview without generating (dry run)
    python3 scripts/generate_audio.py 01_welcome --dry-run

    # Use a specific config file
    python3 scripts/generate_audio.py --config my_config.yaml --all
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    
    try:
        import yaml
    except ImportError:
        missing.append("pyyaml")
    
    try:
        from elevenlabs import ElevenLabs
    except ImportError:
        missing.append("elevenlabs")
    
    if missing:
        print("Missing dependencies. Install with:")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)


def load_config(config_path: Path) -> dict:
    """Load configuration from YAML file."""
    import yaml
    
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        print("Creating default config...")
        create_default_config(config_path)
        print(f"Edit {config_path} with your voice_id, then try again.")
        sys.exit(1)
    
    with open(config_path) as f:
        return yaml.safe_load(f)


def create_default_config(config_path: Path):
    """Create a default configuration file."""
    default_config = '''# HelloHistory Audio Generation Config
# 
# Get your voice_id from ElevenLabs:
#   1. Go to https://elevenlabs.io/app/voice-lab
#   2. Create or select a voice
#   3. Click the ID button to copy the voice ID

# ElevenLabs settings
voice_id: "YOUR_VOICE_ID_HERE"  # Required: paste your voice ID
model_id: "eleven_monolingual_v1"  # or "eleven_multilingual_v2"

# Voice settings (0.0 to 1.0)
stability: 0.5
similarity_boost: 0.75
style: 0.45
use_speaker_boost: true

# Output settings
output_format: "mp3_44100_128"  # mp3_44100_128, mp3_44100_192, pcm_16000, etc.

# Chapter definitions
# Each chapter needs an id and either a source file or inline text
chapters:
  - id: "00_intro"
    text: "Welcome to Del Monte. Pick up the receiver to begin your journey through this remarkable mid-century home."
  
  - id: "01_welcome"
    source: "voice-tracks/01_welcome.txt"
  
  - id: "02_marys_story"
    source: "voice-tracks/02_marys_story.txt"
  
  - id: "03_building"
    source: "voice-tracks/03_building_del_monte.txt"
  
  - id: "04_design"
    source: "voice-tracks/04_design_philosophy.txt"
  
  - id: "05_other_work"
    source: "voice-tracks/05_other_work.txt"
  
  - id: "06_closing"
    source: "voice-tracks/06_closing.txt"
  
  # Note: 07_song.mp3 is music, not generated speech
'''
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        f.write(default_config)


def list_voices(client) -> None:
    """List all available voices."""
    print("\nAvailable Voices:")
    print("=" * 60)
    
    response = client.voices.get_all()
    
    for voice in response.voices:
        labels = voice.labels or {}
        accent = labels.get('accent', 'unknown')
        gender = labels.get('gender', 'unknown')
        
        print(f"\n  Name: {voice.name}")
        print(f"  ID:   {voice.voice_id}")
        print(f"  Type: {gender}, {accent}")
        if voice.description:
            print(f"  Desc: {voice.description[:60]}...")
    
    print("\n" + "=" * 60)
    print("Copy the voice_id to your audio_config.yaml")


def get_chapter_text(chapter: dict, scripts_dir: Path) -> str:
    """Get the text content for a chapter."""
    if "text" in chapter:
        return chapter["text"]
    
    if "source" in chapter:
        source_path = scripts_dir / chapter["source"]
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        return source_path.read_text()
    
    raise ValueError(f"Chapter {chapter['id']} has no 'text' or 'source'")


def generate_chapter(
    client,
    chapter_id: str,
    text: str,
    config: dict,
    output_dir: Path,
    dry_run: bool = False
) -> Path:
    """Generate audio for a single chapter."""
    output_path = output_dir / f"{chapter_id}.mp3"
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Generating: {chapter_id}")
    print(f"  Text length: {len(text)} characters")
    print(f"  Output: {output_path}")
    
    if dry_run:
        print(f"  Preview: {text[:100]}...")
        return output_path
    
    # Generate audio
    audio = client.text_to_speech.convert(
        voice_id=config["voice_id"],
        model_id=config.get("model_id", "eleven_monolingual_v1"),
        text=text,
        voice_settings={
            "stability": config.get("stability", 0.5),
            "similarity_boost": config.get("similarity_boost", 0.75),
            "style": config.get("style", 0.45),
            "use_speaker_boost": config.get("use_speaker_boost", True),
        },
        output_format=config.get("output_format", "mp3_44100_128"),
    )
    
    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    
    # Get file size
    size_kb = output_path.stat().st_size / 1024
    print(f"  ✓ Generated: {size_kb:.1f} KB")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate audio from voice-track text files using ElevenLabs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 01_welcome           Generate chapter 01
  %(prog)s --all                Generate all chapters
  %(prog)s --list-voices        List available voices
  %(prog)s 01_welcome --dry-run Preview without generating
        """
    )
    
    parser.add_argument(
        "chapter",
        nargs="?",
        help="Chapter ID to generate (e.g., 01_welcome)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all chapters"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available ElevenLabs voices"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without generating audio"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "scripts" / "audio_config.yaml",
        help="Path to config file (default: scripts/audio_config.yaml)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "src" / "audio",
        help="Output directory (default: src/audio)"
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    check_dependencies()
    
    # Check API key
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY environment variable not set")
        print("\nTo set it:")
        print('  export ELEVENLABS_API_KEY="your-key-here"')
        print("\nGet your API key from:")
        print("  https://elevenlabs.io/app/settings/api-keys")
        sys.exit(1)
    
    # Import ElevenLabs (after dependency check)
    from elevenlabs import ElevenLabs
    client = ElevenLabs(api_key=api_key)
    
    # Handle --list-voices
    if args.list_voices:
        list_voices(client)
        return
    
    # Require --all or a chapter name
    if not args.all and not args.chapter:
        parser.print_help()
        print("\nError: Specify a chapter ID or use --all")
        sys.exit(1)
    
    # Load config
    config = load_config(args.config)
    
    # Check voice_id is set
    if config.get("voice_id") == "YOUR_VOICE_ID_HERE":
        print("Error: voice_id not configured")
        print(f"\nEdit {args.config} and set your voice_id")
        print("Use --list-voices to see available voices")
        sys.exit(1)
    
    scripts_dir = PROJECT_ROOT / "scripts"
    chapters_to_generate = []
    
    if args.all:
        chapters_to_generate = config.get("chapters", [])
    else:
        # Find the specified chapter
        for chapter in config.get("chapters", []):
            if chapter["id"] == args.chapter:
                chapters_to_generate = [chapter]
                break
        
        if not chapters_to_generate:
            print(f"Error: Chapter '{args.chapter}' not found in config")
            print("\nAvailable chapters:")
            for ch in config.get("chapters", []):
                print(f"  - {ch['id']}")
            sys.exit(1)
    
    # Generate audio
    print(f"\n{'=' * 60}")
    print(f"HelloHistory Audio Generator")
    print(f"{'=' * 60}")
    print(f"Voice ID: {config['voice_id'][:20]}...")
    print(f"Output:   {args.output_dir}")
    print(f"Chapters: {len(chapters_to_generate)}")
    
    generated = []
    errors = []
    
    for chapter in chapters_to_generate:
        try:
            text = get_chapter_text(chapter, scripts_dir)
            output = generate_chapter(
                client,
                chapter["id"],
                text,
                config,
                args.output_dir,
                args.dry_run
            )
            generated.append(output)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            errors.append((chapter["id"], str(e)))
    
    # Summary
    print(f"\n{'=' * 60}")
    print(f"Summary")
    print(f"{'=' * 60}")
    print(f"Generated: {len(generated)}")
    print(f"Errors:    {len(errors)}")
    
    if errors:
        print("\nErrors:")
        for chapter_id, error in errors:
            print(f"  - {chapter_id}: {error}")
    
    if generated and not args.dry_run:
        print("\nTest with:")
        print("  make test")


if __name__ == "__main__":
    main()
