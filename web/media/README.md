# web/media

Assets for the project site. Drop files here and they wire up automatically.

| File | Used for | Notes |
|------|----------|-------|
| `rabbit.jpg` | Photo section on the site | ✅ present — Nabaztag by Rama, [CC BY-SA 2.0 FR](https://creativecommons.org/licenses/by-sa/2.0/fr/deed.en), via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Nabaztag-IMG_7036.jpg) |
| `wiggle.mp4` | Hero loop on the site | ⬜ add later — see below |

## Adding the ear-wiggle video

Record a short clip of the ears wiggling, then export a small **muted** MP4:

- **Format:** MP4 (H.264 + AAC), **≤ ~20 s**, keep it **under 50 MB** (GitHub warns at 50 MB, hard-blocks at 100 MB).
- **Silent:** the hero autoplays it muted + looping, so audio isn't needed.
- Convert on the Mac, e.g.:

  ```bash
  # trim + shrink to 720p, strip audio
  ffmpeg -i input.mov -t 15 -an -vf "scale=-2:720" -movflags +faststart web/media/wiggle.mp4
  ```

Drop it in as `web/media/wiggle.mp4`, commit, and push — the site replaces the
animated CSS bunny with your clip on the next deploy. If it's missing, the bunny
simply stays. For a video too big for the repo, put it on YouTube instead and
ask to embed it.
