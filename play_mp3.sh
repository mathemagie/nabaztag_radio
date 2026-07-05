#!/usr/bin/env bash
# Play an MP3 (or any audio file) on the Nabaztag Pi.
#
# The Pi runs an EOL Raspbian Buster with no MP3 decoder (mpg123 uninstallable),
# and `aplay` only handles WAV. So we convert to WAV here on the Mac with the
# built-in `afconvert`, copy it over, and play it through the WM8960 sound HAT.
#
# Usage:
#   ./play_mp3.sh /path/to/file.mp3
#   ./play_mp3.sh ~/Downloads/song.mp3
#
# Requires: afconvert (built into macOS), ssh alias `pi` configured.

set -euo pipefail

SRC="${1:-}"
if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
    echo "Usage: $0 <audio-file>" >&2
    echo "  e.g. $0 ~/Downloads/song.mp3" >&2
    exit 1
fi

HOST="pi"                       # ssh alias for the Nabaztag
DEVICE="hw:0"                   # ALSA device (tagtagtag WM8960 HAT)
REMOTE_WAV="/tmp/nabaztag_play.wav"
LOCAL_WAV="$(mktemp -t nabaztag).wav"

cleanup() { rm -f "$LOCAL_WAV"; }
trap cleanup EXIT

echo "→ Converting '$(basename "$SRC")' to WAV (44.1kHz/16-bit/stereo)..."
afconvert -f WAVE -d LEI16@44100 -c 2 "$SRC" "$LOCAL_WAV"

echo "→ Copying to $HOST:$REMOTE_WAV ..."
scp -q "$LOCAL_WAV" "$HOST:$REMOTE_WAV"

echo "→ Playing on the Nabaztag..."
ssh "$HOST" "aplay -D $DEVICE '$REMOTE_WAV'"

echo "✓ Done."
