# Section 188 Housing Act Violation Audio Project

## Project Status: IN PROGRESS

### ✅ Completed Tasks

1. **Grain API Transcript Extraction**
   - Successfully extracted 12 of 15 violation transcripts
   - Retrieved exact speaker names, timestamps, and dialogue
   - Created master CSV: `section188_violation_transcripts.csv`

2. **Organized Folder Structure**
   - Created 15 violation folders (violation-01 through violation-15)
   - Each folder contains:
     - Individual CSV file with violation data
     - README.md with violation details
     - (In progress) Full recording MP3
     - (In progress) 60-second violation segment MP3

3. **Audio Download System**
   - Built Python script using Grain API
   - Downloads MP4 from Grain `/recordings/{id}/download` endpoint
   - Extracts MP3 audio using ffmpeg
   - Creates timestamped segments for each violation
   - Currently processing 9 unique recordings

### 📊 Violation Data Summary

**Successfully Extracted (12 violations):**
- 001: Roger Mushett (Westminster) - Sep 18, 2025
- 002: Roger Mushett (Westminster) - Sep 22, 2025
- 004: Salen (Westminster Housing) - Aug 29, 2025
- 005: Ben Mak - Aug 29, 2025
- 006: Westminster Housing Solutions - Oct 3, 2025
- 007: Ben Mak - Oct 3, 2025
- 008: Ben Mak - Sep 30, 2025
- 009: Ben Mak - Sep 26, 2025
- 010: Speaker 2 (St John/The Passage) - Oct 14, 2025
- 011: Speaker 1 (St John/The Passage) - Oct 14, 2025
- 012: Dr. Newton (GP) - Sep 16, 2025
- 014: Malik (Westminster Housing) - Aug 29, 2025

**Missing (3 violations need recording IDs):**
- 003: Marilyn Modeste - Nov 7, 2024
- 013: Jade Ferguson - Dec 24, 2024
- 015: Roger Mushett - Sep 26, 2025

### 🎯 Next Steps

1. **Complete Audio Downloads** (In Progress)
   - Script currently running
   - Will create full MP3 + segments for all 12 violations

2. **Find Missing Recording IDs**
   - Need proper Grain recording IDs for violations 003, 013, 015
   - Current placeholder IDs caused 400 errors

3. **Update HTML Page**
   - Replace Grain URL buttons with local MP3 audio players
   - Use path: `audio/section188-violations/violation-XX/violation-XXX-segment.mp3`
   - Add HTML5 audio controls for direct playback

4. **Verify All Audio Files**
   - Check each violation folder has:
     - full-recording.mp3
     - violation-XXX-segment.mp3
   - Test playback quality

### 📁 File Structure

```
audio/section188-violations/
├── violation-01/
│   ├── violation-001-data.csv
│   ├── README.md
│   ├── full-recording.mp3         (downloading)
│   └── violation-001-segment.mp3  (will be created)
├── violation-02/
│   ├── violation-002-data.csv
│   ├── README.md
│   ├── full-recording.mp3
│   └── violation-002-segment.mp3
...
├── section188_violation_transcripts.csv  (master CSV)
├── extract_grain_transcripts.py          (extraction script)
├── organize_violations.py                (organization script)
├── download_audio.py                     (download script - RUNNING)
├── AUDIO_DOWNLOAD_LIST.md               (reference doc)
└── PROJECT_SUMMARY.md                    (this file)
```

### 🔧 Technical Details

**Grain API Configuration:**
- Workspace Token: `grain_wat_4im1uhu2_FI0elZgNHTc7sRQbngyQJinE7dhyEbqOkv33xaxf`
- Base URL: `https://api.grain.com/_/workspace-api`
- Endpoints Used:
  - `/recordings` - List all recordings
  - `/recordings/{id}?transcript_format=json` - Get transcript
  - `/recordings/{id}/download` - Download MP4

**Audio Processing:**
- Download: MP4 video from Grain
- Extract: MP3 audio using ffmpeg (high quality, `-q:a 2`)
- Segment: 60-second clips starting at violation timestamp
- Cleanup: Remove temp MP4 and MP3 files after processing

**Speaker Identification:**
- Roger Westminster Housing Social Services
- Salen Westminster Housing Solutions
- WESTMINSTER_HOUSING SOLUTIONS
- Malik Westminster Housing Solutions
- Ben Mak / Mr. Mak Justice Minds Forensic Intelligence Ltd
- DR NEWTON - GP PRACTICE
- Speaker 1 & Speaker 2 (The Passage staff)

### ⏰ Timeline

- **Oct 18, 2025 00:06** - Created folder structure
- **Oct 18, 2025 00:07** - Extracted transcripts via Grain API
- **Oct 18, 2025 00:10** - Organized data into individual folders
- **Oct 18, 2025 00:15** - Started audio download process (9 recordings)
- **Est. Completion:** 00:30-00:45 (depending on file sizes)

### 📝 Notes for Next Session

1. Once downloads complete, verify all audio files exist
2. Update `institutional-investigation-s188.html` to use local audio
3. Find proper recording IDs for missing 3 violations
4. Test audio playback on website
5. Consider adding download links for full recordings
6. Add audio duration info to each violation display
