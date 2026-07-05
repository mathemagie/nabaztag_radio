# Nabaztag Radio 🐰📻

Notes and access details for my Nabaztag rabbit, revived with the open-source
[**pynab**](https://github.com/nabaztag2018/pynab) project on a Raspberry Pi.

## The device

| | |
|---|---|
| **Hostname** | `nabaztag` (`nabaztag.home`) |
| **IP address** | `192.168.1.66` (Wi-Fi, on `Livebox-9E45`) |
| **Hardware** | Raspberry Pi Zero W Rev 1.1 |
| **OS** | Raspbian GNU/Linux 10 (Buster), kernel 5.10.17+ |
| **MAC** | `b8:27:eb:b5:3f:df` (Raspberry Pi Foundation) |
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

Passwordless key login is configured. Connect with:

```bash
ssh nabaztag
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

**User:** `pi` · password login also still works as a fallback.

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
