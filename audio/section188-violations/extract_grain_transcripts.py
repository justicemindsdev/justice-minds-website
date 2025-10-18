#!/usr/bin/env python3
"""
Extract exact speaker names, timestamps, and transcripts from Grain recordings
for Section 188 Housing Act violation evidence compilation.
"""

import requests
import csv
import time
import os
from datetime import datetime

# Grain API Configuration
WORKSPACE_TOKEN = os.getenv("GRAIN_WORKSPACE_TOKEN")
if not WORKSPACE_TOKEN:
    raise ValueError("GRAIN_WORKSPACE_TOKEN environment variable not set")
BASE_URL = "https://api.grain.com/_/workspace-api"
HEADERS = {
    "Authorization": f"Bearer {WORKSPACE_TOKEN}",
    "Content-Type": "application/json"
}

# Recording IDs extracted from Grain share URLs
VIOLATIONS = [
    {
        "id": "3ab95f37-bf55-4325-82bd-98ebd078745b",
        "timestamp_ms": 30000,
        "date": "2025-09-18",
        "violation_num": "001"
    },
    {
        "id": "e863f9ae-d65e-4ca9-bba7-67ee380fb7f1",
        "timestamp_ms": 2231000,
        "date": "2025-09-22",
        "violation_num": "002"
    },
    {
        "id": "maralyn-12-34",  # Note: This might need the full ID
        "timestamp_ms": 763000,
        "date": "2024-11-07",
        "violation_num": "003"
    },
    {
        "id": "1309bddd-fb22-4398-9c12-2a3ff36a377a",
        "timestamp_ms": 1917000,
        "date": "2025-08-29",
        "violation_num": "004"
    },
    {
        "id": "1309bddd-fb22-4398-9c12-2a3ff36a377a",
        "timestamp_ms": 553000,
        "date": "2025-08-29",
        "violation_num": "005"
    },
    {
        "id": "cef3a43e-6d2e-47df-a468-fe1889388cb4",
        "timestamp_ms": 3205000,
        "date": "2025-10-03",
        "violation_num": "006"
    },
    {
        "id": "cef3a43e-6d2e-47df-a468-fe1889388cb4",
        "timestamp_ms": 3463000,
        "date": "2025-10-03",
        "violation_num": "007"
    },
    {
        "id": "2b4a4988-c7e9-4ad2-90bc-fd053c3f75db",
        "timestamp_ms": 794000,
        "date": "2025-09-30",
        "violation_num": "008"
    },
    {
        "id": "b11921cb-7719-4f3e-a775-4c86d28e3c6f",
        "timestamp_ms": 510000,
        "date": "2025-09-26",
        "violation_num": "009"
    },
    {
        "id": "b02b892c-392e-4f48-9cae-bd8632fa8ffd",
        "timestamp_ms": 918000,
        "date": "2025-10-14",
        "violation_num": "010"
    },
    {
        "id": "b02b892c-392e-4f48-9cae-bd8632fa8ffd",
        "timestamp_ms": 951000,
        "date": "2025-10-14",
        "violation_num": "011"
    },
    {
        "id": "219fb1a7-b692-4c80-a4d8-ad6f9c68c079",
        "timestamp_ms": 30000,
        "date": "2025-09-16",
        "violation_num": "012"
    },
    {
        "id": "jade-ferguson-24-dec-2024",  # Note: This might need the full ID
        "timestamp_ms": 939000,
        "date": "2024-12-24",
        "violation_num": "013"
    },
    {
        "id": "2a1c2321-827f-4764-894e-ed5e51ef6a8e",
        "timestamp_ms": 2069000,
        "date": "2025-08-29",
        "violation_num": "014"
    },
    {
        "id": "formal-notice-26-sep-2025",  # Note: This might need the full ID
        "timestamp_ms": 721000,
        "date": "2025-09-26",
        "violation_num": "015"
    }
]


def format_timestamp_ms(ms):
    """Convert milliseconds to MM:SS format"""
    seconds = ms // 1000
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def get_recording_transcript(recording_id):
    """Fetch transcript from Grain API for specific recording"""
    url = f"{BASE_URL}/recordings/{recording_id}?transcript_format=json&include_highlights=true&include_participants=true"
    
    print(f"Fetching transcript for recording ID: {recording_id}")
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            transcript_json = data.get('transcript_json', [])
            recording_title = data.get('title', 'Unknown')
            recording_url = data.get('url', '')
            
            print(f"  ✓ Success: Found {len(transcript_json)} transcript segments")
            print(f"  Recording: {recording_title}")
            
            return {
                'transcript': transcript_json,
                'title': recording_title,
                'url': recording_url
            }
        else:
            print(f"  ✗ Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"  ✗ Exception: {str(e)}")
        return None


def find_segment_at_timestamp(transcript, target_ms, window_ms=30000):
    """Find transcript segment closest to target timestamp within window"""
    
    closest_segment = None
    min_diff = float('inf')
    
    for segment in transcript:
        segment_start = segment.get('start', 0)
        diff = abs(segment_start - target_ms)
        
        if diff < min_diff and diff <= window_ms:
            min_diff = diff
            closest_segment = segment
    
    return closest_segment


def extract_violation_segments():
    """Extract transcript segments for all 15 violations"""
    
    results = []
    
    for violation in VIOLATIONS:
        print(f"\n{'='*80}")
        print(f"Processing Violation {violation['violation_num']}")
        print(f"{'='*80}")
        
        recording_data = get_recording_transcript(violation['id'])
        
        if recording_data:
            transcript = recording_data['transcript']
            title = recording_data['title']
            base_url = recording_data['url']
            
            # Find the segment at the specified timestamp
            target_segment = find_segment_at_timestamp(
                transcript, 
                violation['timestamp_ms']
            )
            
            if target_segment:
                speaker = target_segment.get('speaker', 'Unknown Speaker')
                text = target_segment.get('text', '')
                start_ms = target_segment.get('start', 0)
                
                # Create segment URL with timestamp
                segment_url = f"{base_url}?t={start_ms}"
                
                results.append({
                    'violation_num': violation['violation_num'],
                    'date': violation['date'],
                    'recording_title': title,
                    'speaker': speaker,
                    'timestamp': format_timestamp_ms(start_ms),
                    'transcript': text,
                    'segment_url': segment_url,
                    'recording_url': base_url
                })
                
                print(f"  ✓ Found segment:")
                print(f"    Speaker: {speaker}")
                print(f"    Timestamp: {format_timestamp_ms(start_ms)}")
                print(f"    Text preview: {text[:100]}...")
            else:
                print(f"  ✗ No segment found at timestamp {format_timestamp_ms(violation['timestamp_ms'])}")
        
        # Rate limiting
        time.sleep(0.5)
    
    return results


def save_to_csv(results, filename='section188_violation_transcripts.csv'):
    """Save extracted segments to CSV"""
    
    print(f"\n{'='*80}")
    print(f"Saving {len(results)} violation segments to {filename}")
    print(f"{'='*80}\n")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'violation_num',
            'date',
            'recording_title',
            'speaker',
            'timestamp',
            'transcript',
            'segment_url',
            'recording_url'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            writer.writerow(result)
    
    print(f"✓ CSV file created successfully: {filename}")
    print(f"\nSummary:")
    print(f"  Total violations: {len(results)}")
    print(f"  Date range: {min(r['date'] for r in results)} to {max(r['date'] for r in results)}")
    
    # Show unique speakers
    speakers = set(r['speaker'] for r in results)
    print(f"  Unique speakers: {len(speakers)}")
    for speaker in sorted(speakers):
        count = sum(1 for r in results if r['speaker'] == speaker)
        print(f"    - {speaker}: {count} segments")


def main():
    """Main execution function"""
    print("="*80)
    print("GRAIN API TRANSCRIPT EXTRACTION")
    print("Section 188 Housing Act Violation Evidence")
    print("="*80)
    
    # Extract all violation segments
    results = extract_violation_segments()
    
    # Save to CSV
    if results:
        save_to_csv(results)
    else:
        print("\n✗ No results to save")


if __name__ == "__main__":
    main()
