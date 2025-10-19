#!/usr/bin/env python3
"""
Organize Section 188 violations into individual folders with CSV, full audio, and segments.
"""

import csv
import os
import subprocess
import time

# Read the master CSV
violations = []
with open('section188_violation_transcripts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        violations.append(row)

print(f"Found {len(violations)} violations in CSV")

# Process each violation
for violation in violations:
    num = violation['violation_num']
    # Ensure folder name matches (violation-01 format)
    folder_num = num.lstrip('0') if len(num) > 1 else num
    folder = f"violation-{folder_num.zfill(2)}"
    
    print(f"\n{'='*80}")
    print(f"Processing Violation {num}")
    print(f"{'='*80}")
    
    # Create individual CSV for this violation
    csv_path = f"{folder}/violation-{num}-data.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = violation.keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(violation)
    
    print(f"✓ Created CSV: {csv_path}")
    
    # Extract recording URL (base URL without timestamp)
    recording_url = violation['recording_url']
    segment_url = violation['segment_url']
    
    # Download full audio
    full_audio = f"{folder}/full-recording.mp3"
    print(f"Downloading full audio to: {full_audio}")
    
    try:
        # Use yt-dlp to download from Grain
        cmd = [
            'yt-dlp',
            '-x',  # Extract audio
            '--audio-format', 'mp3',
            '--audio-quality', '0',  # Best quality
            '-o', full_audio,
            recording_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 or os.path.exists(full_audio):
            print(f"✓ Downloaded full audio")
        else:
            print(f"⚠ Could not download: {result.stderr[:200]}")
    
    except Exception as e:
        print(f"✗ Error downloading: {str(e)}")
    
    # Extract segment (if full audio exists)
    if os.path.exists(full_audio):
        segment_audio = f"{folder}/violation-{num}-segment.mp3"
        timestamp = violation['timestamp']
        
        # Convert MM:SS to seconds
        parts = timestamp.split(':')
        start_seconds = int(parts[0]) * 60 + int(parts[1])
        
        print(f"Extracting segment starting at {timestamp} ({start_seconds}s)")
        
        try:
            # Extract 60 seconds from timestamp
            cmd = [
                'ffmpeg',
                '-i', full_audio,
                '-ss', str(start_seconds),
                '-t', '60',  # 60 seconds duration
                '-acodec', 'libmp3lame',
                '-q:a', '2',  # High quality
                '-y',  # Overwrite
                segment_audio
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(segment_audio):
                print(f"✓ Extracted segment: {segment_audio}")
            else:
                print(f"⚠ Could not extract segment: {result.stderr[:200]}")
        
        except Exception as e:
            print(f"✗ Error extracting segment: {str(e)}")
    
    # Create README for this violation
    readme_path = f"{folder}/README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f"# Violation {num}\n\n")
        f.write(f"**Date:** {violation['date']}\n")
        f.write(f"**Speaker:** {violation['speaker']}\n")
        f.write(f"**Timestamp:** {violation['timestamp']}\n")
        f.write(f"**Recording:** {violation['recording_title']}\n\n")
        f.write(f"## Transcript\n\n")
        f.write(f"{violation['transcript']}\n\n")
        f.write(f"## Files\n\n")
        f.write(f"- `violation-{num}-data.csv` - CSV data for this violation\n")
        f.write(f"- `full-recording.mp3` - Complete audio recording\n")
        f.write(f"- `violation-{num}-segment.mp3` - Extracted violation segment\n\n")
        f.write(f"## Links\n\n")
        f.write(f"- [Segment URL]({violation['segment_url']})\n")
        f.write(f"- [Full Recording]({violation['recording_url']})\n")
    
    print(f"✓ Created README: {readme_path}")
    
    # Rate limiting between downloads
    time.sleep(1)

print(f"\n{'='*80}")
print("PROCESSING COMPLETE")
print(f"{'='*80}")
print(f"\nOrganized {len(violations)} violations into individual folders")
print("Each folder contains:")
print("  - CSV data file")
print("  - Full recording audio (if downloaded)")
print("  - Extracted segment audio (if processed)")
print("  - README with violation details")
