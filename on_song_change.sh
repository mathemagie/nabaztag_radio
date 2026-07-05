#!/usr/bin/env bash
# spotifyd on-song-change hook: wiggle the Nabaztag's ears when the music changes.
#
# spotifyd runs this on every player event and sets PLAYER_EVENT. We only
# wiggle when a (new) track actually starts playing — not on stop/pause/preload.
# The wiggle runs in the background so it never blocks spotifyd's audio thread.

case "${PLAYER_EVENT:-}" in
  change|start|play|playing)
    /home/pi/wiggle_ears.py >/dev/null 2>&1 &
    ;;
esac
exit 0
