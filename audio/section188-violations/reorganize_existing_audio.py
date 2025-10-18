#!/usr/bin/env python3
"""
Reorganize existing downloaded audio to new dual structure using files from violation-* folders
"""

import os
import csv
import shutil
from pathlib import Path

# Configuration
MAIN_FOLDER = Path("/Volumes/JUDGE_MAK/AUDIO_188")
RECORDINGS_FOLDER = MAIN_FOLDER / "RECORDINGS"
VIOLATIONS_FOLDER = MAIN_FOLDER / "VIOLATIONS"
CSV_FILE = Path("section188_violation_transcripts.csv")
EXISTING_AUDIO = Path(".")  # Current directory has violation-01, violation-02, etc.

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
    print("REORGANIZING EXISTING AUDIO TO DUAL STRUCTURE")
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
                    'segments': []
                }
            recordings[recording_title]['segments'].append(row)
            violations.append(row)
    
    print(f"  {len(recordings)} recordings, {len(violations)} violations")
    
    # PART 1: Create recording folders (GRANULAR)
    print(f"\n{'=' * 80}")
    print("PART 1: CREATING RECORDING FOLDERS (GRANULAR)")
    print(f"{'=' * 80}")
    
    # Track which full recordings we've copied
    recording_audio_map = {}
    
    for idx, (recording_title, data) in enumerate(recordings.items(), 1):
        print(f"\n[{idx}/{len(recordings)}] {recording_title}")
        
        folder_name = sanitize_filename(recording_title)
        recording_folder = RECORDINGS_FOLDER / folder_name
        recording_folder.mkdir(exist_ok=True)
        segments_folder = recording_folder / "SEGMENTS"
        segments_folder.mkdir(exist_ok=True)
        
        # Find source audio from any violation that has this recording
        source_found = False
        for segment in data['segments']:
            violation_num = segment['violation_num']
            source_folder = EXISTING_AUDIO / f"violation-{violation_num}"
            
            if source_folder.exists():
                # Copy full recording if not already done
                full_mp3_source = source_folder / "full-recording.mp3"
                full_mp3_dest = recording_folder / "FULL_RECORDING.mp3"
                
                if full_mp3_source.exists() and not full_mp3_dest.exists():
                    shutil.copy2(full_mp3_source, full_mp3_dest)
                    print(f"  ✓ Copied FULL_RECORDING.mp3 ({full_mp3_dest.stat().st_size / 1024 / 1024:.1f} MB)")
                    source_found = True
                    recording_audio_map[recording_title] = full_mp3_dest
                    break
        
        if not source_found:
            print(f"  ✗ No source audio found")
            continue
        
        # Create CSV and segments
        print(f"  Creating {len(data['segments'])} segments...")
        csv_rows = []
        
        for seg_idx, segment in enumerate(data['segments'], 1):
            violation_num = segment['violation_num']
            source_folder = EXISTING_AUDIO / f"violation-{violation_num}"
            segment_source = source_folder / f"violation-{violation_num}-segment.mp3"
            
            timestamp_ms = parse_timestamp(segment['timestamp'])
            mmss = convert_ms_to_mmss(timestamp_ms)
            speaker_short = segment['speaker'].split()[0] if segment['speaker'] else "Unknown"
            
            segment_filename = f"{seg_idx:03d}_{sanitize_filename(speaker_short)}_{mmss.replace(':', '-')}.mp3"
            segment_dest = segments_folder / segment_filename
            
            # Copy segment if exists
            if segment_source.exists() and not segment_dest.exists():
                shutil.copy2(segment_source, segment_dest)
                print(f"    ✓ {segment_filename}")
            elif segment_dest.exists():
                print(f"    ✓ {segment_filename} (exists)")
            else:
                print(f"    ⚠ {segment_filename} (source not found)")
            
            csv_rows.append({
                'SPEAKER': segment['speaker'],
                'TIME_STAMP_mmss': mmss,
                'TRANSCRIPT': segment['transcript'],
                'TIME_STAMP_hhmmssms': convert_ms_to_hhmmssms(timestamp_ms),
                'SUPABASE_LINK': '',
                'SEGMENT_FILE': segment_filename
            })
        
        # Write CSV
        csv_path = recording_folder / "transcript.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['SPEAKER', 'TIME_STAMP_mmss', 'TRANSCRIPT', 'TIME_STAMP_hhmmssms', 'SUPABASE_LINK', 'SEGMENT_FILE']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f"  ✓ CSV created with {len(csv_rows)} entries")
    
    # PART 2: Create violation folders (INDIVIDUAL)
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
        
        # Extract site info and build filename
        site = extract_site_info(recording_title)
        speaker_name = speaker.split()[0] if speaker else "Unknown"
        
        # Get violation description (first few words)
        transcript_words = transcript.split()[:8]
        violation_desc = ' '.join(transcript_words)
        if len(transcript) > len(violation_desc):
            violation_desc += "..."
        
        # Filename: "001-Westminster Social Services Roger 2025-09-18 - Yeah of course.mp3"
        filename = f"{violation_num}-{site} {speaker_name} {date} - {sanitize_filename(violation_desc)}.mp3"
        violation_audio_dest = violation_folder / filename
        
        # Find source segment
        source_folder = EXISTING_AUDIO / f"violation-{violation_num}"
        segment_source = source_folder / f"violation-{violation_num}-segment.mp3"
        
        if segment_source.exists():
            if not violation_audio_dest.exists():
                shutil.copy2(segment_source, violation_audio_dest)
                print(f"  ✓ {violation_num}: {filename}")
            else:
                print(f"  ✓ {violation_num}: {filename} (exists)")
        else:
            print(f"  ⚠ {violation_num}: Source segment not found")
    
    print("\n" + "=" * 80)
    print("REORGANIZATION COMPLETE!")
    print("=" * 80)
    print(f"\n📁 {RECORDINGS_FOLDER}/")
    print(f"   └── {len(recordings)} recording folders with full audio + segments")
    print(f"\n📁 {VIOLATIONS_FOLDER}/")
    print(f"   └── {len(violations)} violation folders with named segments")
    print("\nNext steps:")
    print("1. Upload audio to Supabase storage")
    print("2. Update transcript.csv files with Supabase links")
    print("3. Update HTML page with new structure")

if __name__ == "__main__":
    main()
