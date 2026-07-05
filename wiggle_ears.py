#!/usr/bin/env python3
"""Wiggle the Nabaztag's ears via the nabd protocol.

nabd listens on 127.0.0.1:10543 and accepts JSON commands. The `ears` command
sets absolute ear positions (integers, 0 = up; the ears rotate through ~17
positions). We nudge them out and back a couple times for a little "dance",
then return to rest (0).

Designed to be spawned quickly (e.g. from spotifyd's on-song-change hook), so
it fails silently if nabd is busy or unavailable.
"""

import json
import socket
import time

HOST, PORT = "127.0.0.1", 10543
# (left, right) positions — small moves around the rest position, ending at 0.
WIGGLE = [(3, 3), (0, 0), (2, 4), (0, 0)]
STEP_DELAY = 0.45  # seconds between moves (the motors need time to travel)


def main():
    try:
        s = socket.create_connection((HOST, PORT), timeout=5)
    except OSError:
        return  # nabd not reachable — nothing to do
    s.settimeout(1)
    try:
        s.recv(4096)  # consume the initial {"type":"state",...} greeting
    except OSError:
        pass
    try:
        for left, right in WIGGLE:
            s.sendall(
                (json.dumps({"type": "ears", "left": left, "right": right}) + "\r\n").encode()
            )
            time.sleep(STEP_DELAY)
    except OSError:
        pass
    finally:
        s.close()


if __name__ == "__main__":
    main()
