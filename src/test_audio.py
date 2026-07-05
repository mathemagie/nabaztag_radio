#!/usr/bin/env python3
"""Test audio output on the Nabaztag (tagtagtag WM8960 sound HAT).

Generates a short sine-wave tone and plays it through ALSA with `aplay`.
Uses only the Python standard library -- no sounddevice/pyaudio needed.

Usage:
    ./test_audio.py                 # 440 Hz for 2 s at 30% volume
    ./test_audio.py --freq 880      # change frequency (Hz)
    ./test_audio.py --duration 3    # change duration (seconds)
    ./test_audio.py --volume 0.6    # 0.0 - 1.0
    ./test_audio.py --device hw:0   # ALSA device (default: card 0)
    ./test_audio.py --sweep         # rising sweep 220 -> 880 Hz instead of a tone
"""

import argparse
import math
import struct
import subprocess
import sys
import tempfile
import wave

SAMPLE_RATE = 44100
CHANNELS = 2  # WM8960 is stereo
SAMPLE_WIDTH = 2  # 16-bit


def build_samples(freq, duration, volume, sweep):
    """Yield 16-bit signed sample values for both channels."""
    n = int(SAMPLE_RATE * duration)
    amplitude = int(32767 * max(0.0, min(1.0, volume)))
    fade = int(SAMPLE_RATE * 0.02)  # 20 ms fade in/out to avoid clicks

    for i in range(n):
        if sweep:
            # linear frequency sweep from freq to freq*4
            f = freq + (freq * 3) * (i / n)
        else:
            f = freq
        value = amplitude * math.sin(2 * math.pi * f * (i / SAMPLE_RATE))

        # apply short fade envelope
        if i < fade:
            value *= i / fade
        elif i > n - fade:
            value *= (n - i) / fade

        yield int(value)


def write_wav(path, freq, duration, volume, sweep):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for s in build_samples(freq, duration, volume, sweep):
            frames += struct.pack("<h", s) * CHANNELS  # same value on L and R
        wf.writeframes(bytes(frames))


def main():
    parser = argparse.ArgumentParser(description="Test Nabaztag audio output.")
    parser.add_argument("--freq", type=float, default=440.0, help="tone frequency in Hz")
    parser.add_argument("--duration", type=float, default=2.0, help="duration in seconds")
    parser.add_argument("--volume", type=float, default=0.3, help="volume 0.0-1.0")
    parser.add_argument("--device", default="hw:0", help="ALSA device (default hw:0)")
    parser.add_argument("--sweep", action="store_true", help="play a rising sweep")
    args = parser.parse_args()

    kind = "sweep" if args.sweep else f"{args.freq:.0f} Hz tone"
    print(f"Generating {kind}, {args.duration}s @ {int(args.volume * 100)}% ...")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        write_wav(tmp.name, args.freq, args.duration, args.volume, args.sweep)
        print(f"Playing on ALSA device '{args.device}' ...")
        try:
            subprocess.run(["aplay", "-D", args.device, tmp.name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"aplay failed (exit {e.returncode}). Try --device default or hw:0",
                  file=sys.stderr)
            return 1
        except FileNotFoundError:
            print("aplay not found -- is alsa-utils installed?", file=sys.stderr)
            return 1

    print("Done. If you heard the tone, audio output works.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
