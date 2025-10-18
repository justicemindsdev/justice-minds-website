#!/usr/bin/env python3
"""
Create DUAL structure:
1. Recording folders (granular) - one per Grain file
2. Violation folders - one per violation with its segment

/Volumes/JUDGE_MAK/AUDIO_188/
  ├── RECORDINGS/
  │   ├── 2025-09-18 Roger-Ben-Westminster/
  │   │   ├── transcript.csv
  │   │   ├── FULL_RECORDING.mp4
  │   │   ├── FULL_RECORDING.mp3
  │   │   └── SEGMENTS/
  │   │       └── 001_Roger_Westminster_00-32.mp3
  │   └── ...
  └── VIOLATIONS/
      ├── violation-001/
      │   └── 001-Westminster Social Services Roger 2025-09-18 - Yeah of course.mp3
      ├── violation-002/
      │   └── 002-Westminster Social Services Ben Mak 2025-09-22 - Section 188 expert requirement.mp3
      └── ...
"""

import os
import csv
import shutil
import requests
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
MAIN_FOLDER = Path("/Volumes/JUDGE_MAK/AUDIO_188")
RECORDINGS_FOLDER = MAIN_FOLDER / "RECORDINGS"
VIOLATIONS_FOLDER = MAIN_FOLDER / "VIOLATIONS"
CSV_FILE = Path("section188_violation_transcripts.csv")
API_BASE = "https://api.grain.com/public/v1"
import os
WORKSPACE_TOKEN = os.getenv("GRAIN_WORKSPACE_TOKEN")
if not WORKSPACE_TOKEN:
    raise ValueError("GRAIN_WORKSPACE_TOKEN environment variable not set")
HEADERS = {"Authorization": f"Bearer {WORKSPACE_TOKEN}"}

def parse_grain_url(url):
    """Extract recording ID from Grain share URL"""
    parts = url.split('/')
    if len(parts) >= 6 and parts[4] == 'recording':
        return parts[5]
    return None

def convert_ms_to_mmss(ms):
    """Convert milliseconds to mm:ss"""
    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def convert_ms_to_hhmmssms(ms):
    """Convert milliseconds to hh:mm:ss:ms"""
    hours = ms // 3600000
    ms = ms % 3600000
    minutes = ms // 60000
    ms = ms % 60000
    seconds = ms // 1000
    milliseconds = ms % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

def sanitize_filename(text):
    """Sanitize text for filename"""
    text = text.replace('/', '_').replace('\\', '_').replace(':', '_')
    text = text.replace('*', '_').replace('?', '_').replace('"', '')
    text = text.replace('<', '_').replace('>', '_').replace('|', '_')
    text = text.replace('\n', ' ').strip()
    if len(text) > 80:
        text = text[:80]
    return text

def extract_site_info(recording_title):
    """Extract site/organization from recording title"""
    # Examples: "2025-09-18 Roger-Ben-Westminster-Social-Services"
    # Return: "Westminster Social Services"
    title_lower = recording_title.lower()
    if 'westminster' in title_lower:
        if 'social services' in title_lower or 'social-services' in title_lower:
            return "Westminster Social Services"
        elif 'housing solutions' in title_lower or 'housing-solutions' in title_lower:
            return "Westminster Housing Solutions"
        else:
            return "Westminster Housing"
    elif 'st john' in title_lower or 'stjohn' in title_lower:
        return "St John"
    elif 'medical' in title_lower or 'doctor' in title_lower or 'gp' in title_lower:
        return "GP Medical Practice"
    else:
        return "Westminster"

def download_recording(recording_id, output_path):
    """Download recording MP4"""
    print(f"  Downloading recording {recording_id}...")
    response = requests.get(
        f"{API_BASE}/recordings/{recording_id}/download",
        headers=HEADERS,
        allow_redirects=False
    )
    if response.status_code == 302:
        download_url = response.headers.get('Location')
        if download_url:
            video_response = requests.get(download_url, stream=True)
            if video_response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"    ✓ Downloaded ({output_path.stat().st_size / 1024 / 1024:.1f} MB)")
                return True
    print(f"    ✗ Failed to download")
    return False

def extract_mp3(mp4_path, mp3_path):
    """Extract MP3 from MP4"""
    print(f"  Extracting MP3...")
    cmd = ['ffmpeg', '-i', str(mp4_path), '-vn', '-acodec', 'libmp3lame', '-q:a', '2', str(mp3_path), '-y']
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        print(f"    ✓ Created MP3")
        return True
    return False

def create_segment(full_mp3_path, start_ms, duration_sec, output_path):
    """Create audio segment"""
    start_sec = start_ms / 1000
    cmd = ['ffmpeg', '-i', str(full_mp3_path), '-ss', str(start_sec), '-t', str(duration_sec), '-acodec', 'copy', str(output_path), '-y']
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0

def parse_timestamp(timestamp_str):
    """Parse timestamp to milliseconds"""
    time_parts = timestamp_str.split(':')
    if len(time_parts) == 2:
        minutes = int(time_parts[0])
        seconds = int(time_parts[1])
        return (minutes * 60 + seconds) * 1000
    return 0

def main():
    print("=" * 80)
    print("CREATING DUAL AUDIO STRUCTURE")
    print("=" * 80)
    
    # Create folders
    RECORDINGS_FOLDER.mkdir(parents=True, exist_ok=True)
    VIOLATIONS_FOLDER.mkdir(parents=True, exist_ok=True)
    print(f"\n✓ Created:\n  - {RECORDINGS_FOLDER}\n  - {VIOLATIONS_FOLDER}")
    
    # Read CSV
    print(f"\n📄 Reading {CSV_FILE}...")
    recordings = {}
    violations = []
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recording_title = row['recording_title']
            if recording_title not in recordings:
                recordings[recording_title] = {
                    'recording_url': row['recording_url'],
                    'segments': []
                }
            recordings[recording_title]['segments'].append(row)
            violations.append(row)
    
    print(f"  {len(recordings)} recordings, {len(violations)} violations")
    
    # Process recordings (GRANULAR structure)
    print(f"\n{'=' * 80}")
    print("PART 1: CREATING RECORDING FOLDERS (GRANULAR)")
    print(f"{'=' * 80}")
    
    for idx, (recording_title, data) in enumerate(recordings.items(), 1):
        print(f"\n[{idx}/{len(recordings)}] {recording_title}")
        
        folder_name = sanitize_filename(recording_title)
        recording_folder = RECORDINGS_FOLDER / folder_name
        recording_folder.mkdir(exist_ok=True)
        segments_folder = recording_folder / "SEGMENTS"
        segments_folder.mkdir(exist_ok=True)
        
        recording_id = parse_grain_url(data['recording_url'])
        if not recording_id:
            print(f"  ✗ No recording ID")
            continue
        
        mp4_path = recording_folder / "FULL_RECORDING.mp4"
        mp3_path = recording_folder / "FULL_RECORDING.mp3"
        csv_path = recording_folder / "transcript.csv"
        
        # Download if needed
        if not mp4_path.exists():
            if not download_recording(recording_id, mp4_path):
                continue
        else:
            print(f"  ✓ MP4 exists")
        
        if not mp3_path.exists():
            if not extract_mp3(mp4_path, mp3_path):
                continue
        else:
            print(f"  ✓ MP3 exists")
        
        # Create segments
        print(f"  Creating {len(data['segments'])} segments...")
        csv_rows = []
        
        for seg_idx, segment in enumerate(data['segments'], 1):
            timestamp_ms = parse_timestamp(segment['timestamp'])
            mmss = convert_ms_to_mmss(timestamp_ms)
            speaker_short = segment['speaker'].split()[0] if segment['speaker'] else "Unknown"
            
            segment_filename = f"{seg_idx:03d}_{sanitize_filename(speaker_short)}_{mmss.replace(':', '-')}.mp3"
            segment_path = segments_folder / segment_filename
            
            if not segment_path.exists():
                if create_segment(mp3_path, timestamp_ms, 60, segment_path):
                    print(f"    ✓ {segment_filename}")
                else:
                    print(f"    ✗ {segment_filename}")
            
            csv_rows.append({
                'SPEAKER': segment['speaker'],
                'TIME_STAMP_mmss': mmss,
                'TRANSCRIPT': segment['transcript'],
                'TIME_STAMP_hhmmssms': convert_ms_to_hhmmssms(timestamp_ms),
                'SUPABASE_LINK': '',
                'SEGMENT_FILE': segment_filename
            })
        
        # Write CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['SPEAKER', 'TIME_STAMP_mmss', 'TRANSCRIPT', 'TIME_STAMP_hhmmssms', 'SUPABASE_LINK', 'SEGMENT_FILE']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f"  ✓ CSV created")
    
    # Process violations (INDIVIDUAL structure)
    print(f"\n{'=' * 80}")
    print("PART 2: CREATING VIOLATION FOLDERS (INDIVIDUAL)")
    print(f"{'=' * 80}")
    
    for violation in violations:
        violation_num = violation['violation_num']
        date = violation['date']
        recording_title = violation['recording_title']
        speaker = violation['speaker']
        transcript = violation['transcript']
        
        # Create violation folder
        violation_folder = VIOLATIONS_FOLDER / f"violation-{violation_num}"
        violation_folder.mkdir(exist_ok=True)
        
        # Extract site info
        site = extract_site_info(recording_title)
        
        # Get speaker name (first part)
        speaker_name = speaker.split()[0] if speaker else "Unknown"
        
        # Get violation description (first few words)
        transcript_words = transcript.split()[:8]
        violation_desc = ' '.join(transcript_words)
        if len(transcript) > len(violation_desc):
            violation_desc += "..."
        
        # Build filename: "001-Westminster Social Services Roger 2025-09-18 - Yeah of course.mp3"
        filename = f"{violation_num}-{site} {speaker_name} {date} - {sanitize_filename(violation_desc)}.mp3"
        violation_audio_path = violation_folder / filename
        
        # Find source segment in recordings
        recording_folder_name = sanitize_filename(recording_title)
        source_recording = RECORDINGS_FOLDER / recording_folder_name
        
        if source_recording.exists():
            segments_folder = source_recording / "SEGMENTS"
            # Find matching segment (by speaker)
            found = False
            for seg_file in segments_folder.glob("*.mp3"):
                if speaker_name.lower() in seg_file.stem.lower():
                    # Copy to violation folder
                    if not violation_audio_path.exists():
                        shutil.copy2(seg_file, violation_audio_path)
                        print(f"  ✓ {violation_num}: {filename}")
                    found = True
                    break
            
            if not found:
                print(f"  ⚠ {violation_num}: Segment not found for {speaker_name}")
        else:
            print(f"  ⚠ {violation_num}: Source recording not found")
    
    print("\n" + "=" * 80)
    print("DUAL STRUCTURE COMPLETE!")
    print("=" * 80)
    print(f"\n📁 {RECORDINGS_FOLDER}/")
    print(f"   └── [Recording folders with full audio + segments]")
    print(f"\n📁 {VIOLATIONS_FOLDER}/")
    print(f"   └── [Individual violation folders with named segments]")

if __name__ == "__main__":
    main()
