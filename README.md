# Nabaztag Radio 🐰📻

Notes, access details, and helper scripts for my Nabaztag rabbit, revived with
the open-source [**pynab**](https://github.com/nabaztag2018/pynab) project on a
Raspberry Pi. It's a Spotify Connect speaker whose ears wiggle to the music.

📖 **Project site:** https://mathemagie.github.io/nabaztag_radio/ — an illustrated
walkthrough of how it all works.

## What's in this repo

| File | Runs on | What it does |
|------|---------|--------------|
| `test_audio.py` | Pi | Play a test tone/sweep through the sound HAT |
| `play_mp3.sh` | Mac | Convert an MP3 and play it on the Pi |
| `wiggle_ears.py` | Pi | Wiggle the ears via the nabd protocol |
| `on_song_change.sh` | Pi | spotifyd hook that triggers the ear wiggle |

The scripts are deployed to the Pi's home dir (`~`); this repo is the
source-of-truth backup. See each section below for details.

## The device

| | |
|---|---|
| **Hostname** | `nabaztag` (`nabaztag.home`) |
| **IP address** | `192.168.1.66` (Wi-Fi, on `Livebox-9E45`) |
| **Hardware** | Raspberry Pi Zero W Rev 1.1 |
| **OS** | Raspbian GNU/Linux 10 (Buster), kernel 5.10.17+ |
| **Software** | pynab (`nabd` daemon + web config) |

### Services

| Port | Service | URL |
|------|---------|-----|
| 22   | SSH     | `ssh nabaztag` |
| 80   | Web config (Configuration du Nabaztag) | http://192.168.1.66/ |
| 8080 | pynab app / proxy | http://192.168.1.66:8080/ |

The web interface (port 80) has tabs for **Accueil, Services, RFID, Information
système, Mise à jour, Aide** and includes reboot/shutdown buttons under
*Information système → Maintenance*.

## SSH access

Passwordless key login is configured. Two aliases point at the same Pi:

```bash
ssh nabaztag     # or: ssh pi
```

### How it was set up

1. Located the Pi on the LAN by its Raspberry Pi MAC prefix (`b8:27:eb`):

   ```bash
   nmap -sn 192.168.1.0/24 >/dev/null; arp -a -n | grep b8:27:eb
   ```

2. Installed the SSH public key on the Pi:

   ```bash
   ssh-copy-id -i ~/.ssh/id_ed25519.pub pi@192.168.1.66
   ```

3. Added a host alias in `~/.ssh/config`:

   ```
   Host nabaztag
       HostName 192.168.1.66
       User pi
       IdentityFile ~/.ssh/id_ed25519
   ```

**User:** `pi` (key-based login).

## Useful commands

```bash
# Check the pynab daemon
ssh nabaztag 'systemctl status nabd'

# Follow logs
ssh nabaztag 'journalctl -u nabd -f'

# Reboot / shutdown
ssh nabaztag 'sudo reboot'
ssh nabaztag 'sudo shutdown -h now'
```

## Audio

The rabbit has a **tagtagtag WM8960 sound HAT** (ALSA card 0). `aplay` plays
WAV; there's no MP3 decoder on the Pi (Buster's `mpg123` is uninstallable —
see below), so MP3s are converted to WAV first.

- **`test_audio.py`** (on the Pi at `~/test_audio.py`) — stdlib-only tone
  generator. `python3 ~/test_audio.py --sweep`
- **`play_mp3.sh`** (run from the Mac) — converts an MP3 with `afconvert`,
  copies it over, and plays it: `./play_mp3.sh ~/Downloads/song.mp3`

Mixer levels (Speaker/Headphone/PCM) are raised, unmuted, and saved with
`alsactl store`.

## Spotify Connect (spotifyd)

The Pi is a Spotify Connect speaker named **Nabaztag**, so music plays through
its HAT.

- **Daemon:** `spotifyd` **v0.3.3 armv6-slim** — the newest build that runs on
  the Pi Zero W (armv6, glibc 2.28). Newer spotifyd needs glibc ≥2.29; raspotify
  needs libc6 ≥2.31 / systemd ≥247 — all too new for Buster.
- **Binary:** `/usr/local/bin/spotifyd` · **Config:** `/etc/spotifyd.conf`
  (outputs to `plughw:CARD=tagtagtagsound`) · **Service:** `spotifyd.service`
  (enabled, auto-starts).
- **Auth:** zeroconf/discovery (no stored password — Spotify killed password
  auth for old librespot). Activate it **once** from a first-party Spotify app
  on the same Wi-Fi: Connect menu → **Nabaztag**. After that it also appears in
  LEGO Radio's device list (`d`).

```bash
ssh nabaztag 'systemctl status spotifyd'
ssh nabaztag 'journalctl -u spotifyd -f'
```

Companion terminal player: [`radio_spotify_lego`](../radio_spotify_lego)
(deployed to `~/radio_spotify_lego` on the Pi; launch with its `run-on-pi.sh`).

## Ear wiggle on track change

The ears twitch a little every time the music changes while playing through the
Nabaztag (spotifyd).

- **`wiggle_ears.py`** (Pi: `~/wiggle_ears.py`) — nudges the ears via the nabd
  protocol (`127.0.0.1:10543`, `{"type":"ears","left":X,"right":Y}`).
- **`on_song_change.sh`** (Pi: `~/on_song_change.sh`) — spotifyd hook; fires the
  wiggle only on `change`/`start`/`play` events (not stop/pause).
- Wired via `on_song_change_hook = "/home/pi/on_song_change.sh"` in
  `/etc/spotifyd.conf`.

Test it manually: `ssh pi '~/wiggle_ears.py'`

## Notes & TODO

- Raspbian **Buster is end-of-life** — no more security updates. Consider
  hardening SSH (`PasswordAuthentication no`) since `pi`/`raspberry` boxes are
  actively scanned for.
- Consider rotating the `pi` account password.
- The IP `192.168.1.66` is DHCP-assigned; set a static lease on the Livebox if
  it starts changing.

## Links

- pynab project: https://github.com/nabaztag2018/pynab
- pynab docs: https://github.com/nabaztag2018/pynab/wiki
