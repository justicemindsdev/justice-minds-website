#!/usr/bin/env python3
"""
Download audio files from Grain API for Section 188 violations.
"""

import requests
import csv
import subprocess
import os
import time

# Grain API Configuration
WORKSPACE_TOKEN = os.getenv("GRAIN_WORKSPACE_TOKEN")
if not WORKSPACE_TOKEN:
    raise ValueError("GRAIN_WORKSPACE_TOKEN environment variable not set")
BASE_URL = "https://api.grain.com/_/workspace-api"
HEADERS = {
    "Authorization": f"Bearer {WORKSPACE_TOKEN}",
    "Content-Type": "application/json"
}

# Read violations from CSV
violations = []
with open('section188_violation_transcripts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        violations.append(row)

print(f"Found {len(violations)} violations to process\n")

# Extract unique recording IDs
recording_ids = {}
for v in violations:
    # URL format: https://grain.com/share/recording/{ID}/{share_token}
    rec_id = v['recording_url'].split('/')[5]  # Extract ID from URL
    if rec_id not in recording_ids:
        recording_ids[rec_id] = []
    recording_ids[rec_id].append(v)

print(f"Unique recordings: {len(recording_ids)}\n")

# Download each unique recording
for rec_id, violation_list in recording_ids.items():
    print(f"{'='*80}")
    print(f"Recording ID: {rec_id}")
    print(f"Violations using this recording: {[v['violation_num'] for v in violation_list]}")
    print(f"{'='*80}\n")
    
    # Get download URL from Grain API
    download_url = f"{BASE_URL}/recordings/{rec_id}/download"
    
    try:
        print(f"Requesting download URL...")
        response = requests.get(download_url, headers=HEADERS, allow_redirects=False)
        
        if response.status_code == 302 or response.status_code == 301:
            # Get the redirect URL
            video_url = response.headers.get('Location')
            print(f"✓ Got redirect URL")
            
            # Download the MP4
            temp_video = f"temp_{rec_id}.mp4"
            print(f"Downloading video to {temp_video}...")
            
            video_response = requests.get(video_url, stream=True)
            total_size = int(video_response.headers.get('content-length', 0))
            
            with open(temp_video, 'wb') as f:
                downloaded = 0
                for chunk in video_response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"  Progress: {percent:.1f}%", end='\r')
            
            print(f"\n✓ Downloaded {downloaded / 1024 / 1024:.1f} MB")
            
            # Extract full audio
            full_audio = f"temp_{rec_id}_full.mp3"
            print(f"Extracting audio to {full_audio}...")
            
            cmd = [
                'ffmpeg',
                '-i', temp_video,
                '-vn',  # No video
                '-acodec', 'libmp3lame',
                '-q:a', '2',  # High quality
                '-y',  # Overwrite
                full_audio
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(full_audio):
                print(f"✓ Extracted audio")
                
                # Process each violation that uses this recording
                for violation in violation_list:
                    num = violation['violation_num']
                    folder_num = num.lstrip('0') if len(num) > 1 else num
                    folder = f"violation-{folder_num.zfill(2)}"
                    
                    # Copy full audio to violation folder
                    full_dest = f"{folder}/full-recording.mp3"
                    subprocess.run(['cp', full_audio, full_dest])
                    print(f"  ✓ Copied full audio to {full_dest}")
                    
                    # Extract segment
                    timestamp = violation['timestamp']
                    parts = timestamp.split(':')
                    start_seconds = int(parts[0]) * 60 + int(parts[1])
                    
                    segment_audio = f"{folder}/violation-{num}-segment.mp3"
                    
                    cmd = [
                        'ffmpeg',
                        '-i', full_audio,
                        '-ss', str(start_seconds),
                        '-t', '60',  # 60 seconds
                        '-acodec', 'libmp3lame',
                        '-q:a', '2',
                        '-y',
                        segment_audio
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0 and os.path.exists(segment_audio):
                        print(f"  ✓ Created segment: {segment_audio}")
                    else:
                        print(f"  ✗ Failed to create segment")
                
                # Clean up temp full audio
                os.remove(full_audio)
                print(f"✓ Cleaned up temp audio\n")
            else:
                print(f"✗ Failed to extract audio")
            
            # Clean up temp video
            os.remove(temp_video)
            print(f"✓ Cleaned up temp video\n")
            
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text[:200]}\n")
    
    except Exception as e:
        print(f"✗ Error: {str(e)}\n")
    
    # Rate limiting
    time.sleep(2)

print(f"\n{'='*80}")
print("AUDIO DOWNLOAD COMPLETE")
print(f"{'='*80}")
print("\nEach violation folder now contains:")
print("  - CSV data file")
print("  - Full recording audio (MP3)")
print("  - Extracted violation segment (MP3)")
print("  - README with details")
