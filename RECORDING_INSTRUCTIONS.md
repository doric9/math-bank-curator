# How to Create Your YouTube Demo Video

## Quick Start (3 Steps)

### Step 1: Open the Presentation
```bash
# Open demo_video.html in your browser
open demo_video.html   # macOS
xdg-open demo_video.html   # Linux
start demo_video.html   # Windows
```

### Step 2: Record the Screen
Use any screen recording software:
- **macOS**: QuickTime Player (Cmd+Shift+5)
- **Windows**: Xbox Game Bar (Win+G) or OBS Studio
- **Linux**: SimpleScreenRecorder or OBS Studio
- **Online**: Loom, ScreenPal

### Step 3: Add Voiceover
Use the script in `VIDEO_SCRIPT.md` to record narration:
- **Software**: Audacity (free), GarageBand, Adobe Audition
- **Or**: Record directly while screen recording

---

## Detailed Instructions

### Option A: All-in-One Recording (Easiest)

**Best for**: Quick creation, less editing

1. **Prepare**:
   - Open `demo_video.html` in **fullscreen** (F11)
   - Have `VIDEO_SCRIPT.md` open on another monitor or device
   - Test your microphone

2. **Practice**:
   - Read through the script once
   - Time yourself (should be ~2:20)
   - The slides auto-advance, so match your pace

3. **Record**:
   - Start screen recording
   - Refresh the page to restart slides
   - Begin narrating immediately
   - Follow the script timing
   - Let it run through all 12 slides

4. **Finish**:
   - Stop recording when closing slide appears
   - Save as MP4 (1080p recommended)
   - Upload to YouTube!

### Option B: Separate Video + Audio (Professional)

**Best for**: High quality, flexibility

#### Part 1: Record Screen
```bash
# 1. Open presentation
open demo_video.html

# 2. Press F11 for fullscreen
# 3. Start screen recording (no audio)
# 4. Refresh page to restart
# 5. Let it run completely through (2:50)
# 6. Save as video_raw.mp4
```

#### Part 2: Record Narration
```bash
# 1. Open Audacity or similar
# 2. Hit Record
# 3. Read VIDEO_SCRIPT.md naturally
# 4. Save as narration.mp3
```

#### Part 3: Combine in Video Editor
```bash
# Use any editor (iMovie, DaVinci Resolve, etc.)
# 1. Import video_raw.mp4
# 2. Import narration.mp3
# 3. Sync audio to slides
# 4. Optional: Add background music at 10% volume
# 5. Export as final.mp4
```

---

## Recording Settings

### Video
- **Resolution**: 1920×1080 (1080p)
- **Frame Rate**: 30 fps
- **Format**: MP4 (H.264)
- **Bitrate**: 8-12 Mbps

### Audio
- **Sample Rate**: 44.1 kHz or 48 kHz
- **Bit Depth**: 16-bit
- **Format**: AAC or MP3
- **Bitrate**: 128-192 kbps

---

## Presentation Controls

### Keyboard Shortcuts
- **→ (Right Arrow)**: Next slide manually
- **← (Left Arrow)**: Previous slide
- **F11**: Toggle fullscreen
- **Esc**: Exit fullscreen
- **R**: Refresh to restart

### Auto-Play Behavior
- Slides automatically advance based on timing
- Total runtime: ~2:50 for full loop
- Timer shows elapsed time (bottom right)

---

## Tips for Great Results

### Voice Over
✅ **DO**:
- Speak clearly and with energy
- Emphasize key numbers (100%, 8x, 16 problems)
- Pause briefly between sections
- Sound enthusiastic about the demos
- Practice 2-3 times before final recording

❌ **DON'T**:
- Rush through slides
- Sound monotone or bored
- Include "um" or "uh" filler words
- Read too fast (aim for 150 words/min)

### Visual Recording
✅ **DO**:
- Use fullscreen mode (F11)
- Close other applications
- Use clean desktop background
- Record in quiet environment
- Check resolution (1080p minimum)

❌ **DON'T**:
- Show notifications or popups
- Include browser UI (use fullscreen!)
- Record in low resolution
- Have visual distractions

### Production Quality
✅ **DO**:
- Add subtle background music (optional)
- Normalize audio levels
- Export in high quality (1080p)
- Test on different devices
- Keep file size reasonable (<500MB)

❌ **DON'T**:
- Over-compress video (blurry text)
- Make background music too loud
- Rush the editing process
- Skip quality check

---

## YouTube Upload Checklist

### Title Options
- "Math Bank Curator - AI Agent Demo | Agents For Good"
- "Autonomous Math Problem Generator with Multi-Agent AI"
- "Math Bank Curator: Educational AI Demo"

### Description Template
```
Math Bank Curator - An autonomous math problem generation system using Google's Agent Development Kit (ADK) and multi-agent AI.

🎯 Problem: Teachers spend countless hours creating math problems
✨ Solution: Multi-agent AI system that generates, validates, and curates high-quality problems

🤖 Architecture:
- Scraper Agent: Extracts from web, PDFs, images
- Generator Agent: Creates novel variations
- Validator Agent: Constitutional AI validation
- Problem Bank: Quality-gated storage (≥70/100)

📊 Results:
✅ 100% success rate across all scenarios
✅ 8x more problems extracted with multimodal approach
✅ Perfect validation scores (100/100)

🛠️ Built with:
- Google Agent Development Kit (ADK)
- Gemini 3 Pro
- Python 3.13
- BeautifulSoup, PyPDF2, Pydantic

📚 GitHub: https://github.com/doric9/math-bank-curator

#AgentsForGood #AI #Education #MachineLearning #GoogleADK
```

### Tags
```
agents for good, google adk, multi-agent ai, math education, ai for education,
autonomous agents, gemini api, educational technology, problem generation,
constitutional ai, kaggle competition, machine learning, artificial intelligence
```

### Thumbnail Ideas
- Screenshot of architecture diagram
- "100%" validation score prominently
- "8x Boost" multimodal result
- Math Bank Curator logo with emoji

---

## Advanced: Add Background Music

### Free Music Sources
- **YouTube Audio Library**: Free, no attribution
- **Incompetech**: Kevin MacLeod tracks (attribution)
- **Free Music Archive**: Creative Commons

### Recommended Tracks
- Upbeat tech/corporate music
- Tempo: 100-120 BPM
- Volume: 10-15% of voice
- No lyrics

### Mixing
```
Timeline:
[Background Music: 10% volume throughout]
[Voice Over: 100% volume]
[Fade music out during demos for clarity]
```

---

## Troubleshooting

### Slides advancing too fast/slow?
Edit `demo_video.html` and adjust `data-duration` values (in milliseconds)

### Timer not showing?
Check if `.timer` CSS is visible in your browser

### Video quality poor?
- Increase screen recording resolution to 1080p
- Use higher bitrate (10-12 Mbps)
- Check GPU acceleration in recording software

### Audio out of sync?
- Record separately and sync in video editor
- Use clap/snap at start for sync point
- Most editors have auto-sync features

### File size too large?
- Export at 8 Mbps instead of 12 Mbps
- Use H.264 codec with "fast" preset
- YouTube accepts up to 128 GB (you'll be fine!)

---

## Alternative: Live Demo Video

Instead of the slide presentation, you can record a live CLI demo:

### Recording Plan
1. **Terminal Setup** (0:00-0:15)
   ```bash
   ls -la
   cat README.md | head -20
   ```

2. **Web Scraping** (0:15-0:45)
   ```bash
   python main.py scrape --url "https://artofproblemsolving.com/wiki/index.php?title=2025_AMC_8_Problems" --output demo_seeds.json
   ```

3. **Generate Problems** (0:45-1:30)
   ```bash
   python main.py generate --seeds demo_seeds.json --num-seeds 2 --variations 2 --show-samples
   ```

4. **View Results** (1:30-2:00)
   ```bash
   python main.py view --limit 3 --show-solutions
   ```

5. **Statistics** (2:00-2:20)
   ```bash
   python main.py stats
   cat src/problem_bank/problems.json | jq '.problems | length'
   ```

6. **Closing** (2:20-2:30)
   - Show GitHub repo in browser
   - Quick scroll through README

---

## Quick Commands Reference

### Screen Recording
```bash
# macOS - QuickTime
# 1. Open QuickTime Player
# 2. File → New Screen Recording
# 3. Click record, select area
# 4. Press Stop in menu bar when done

# Linux - SimpleScreenRecorder
sudo apt install simplescreenrecorder
simplescreenrecorder

# Cross-platform - OBS Studio
# Download from obsproject.com
# Free, professional quality
```

### Video Editing
```bash
# Basic trim (ffmpeg)
ffmpeg -i input.mp4 -ss 00:00:05 -to 00:02:50 -c copy output.mp4

# Add audio track
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 final.mp4

# Compress for upload
ffmpeg -i input.mp4 -vcodec h264 -acodec aac -b:v 8M final.mp4
```

---

## Final Checklist

Before uploading to YouTube:

- [ ] Video is under 3 minutes
- [ ] Resolution is 1080p or higher
- [ ] Audio is clear and at good volume
- [ ] All slides are visible and readable
- [ ] No visual glitches or errors
- [ ] Narration matches slides
- [ ] Timer shows correct timing
- [ ] File format is MP4
- [ ] Tested playback on different devices
- [ ] Ready for upload!

---

**Good luck with your demo video!** 🎥✨

The presentation is designed to be clear, professional, and under 3 minutes. Just follow the script, record smoothly, and you'll have a great submission for the Kaggle competition!
