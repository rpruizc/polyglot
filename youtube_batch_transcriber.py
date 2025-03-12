"""
YouTube Batch Transcriber

Fetches and combines transcripts from multiple YouTube videos into a single file.
Usage: python youtube_batch_transcriber.py -o output.txt video_id1 video_id2 ...
"""

import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import sys

def fetch_transcript(video_id):
    """
    Fetch transcript for a single video ID.
    Returns None if transcript is not available.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {str(e)}", file=sys.stderr)
        return None

def save_transcripts(video_ids, output_file):
    """
    Fetch and save transcripts for multiple videos.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, video_id in enumerate(video_ids):
            transcript = fetch_transcript(video_id)
            if transcript:
                if i > 0:
                    f.write('\n===\n')
                f.write(transcript)

def main():
    parser = argparse.ArgumentParser(description='Fetch YouTube video transcripts')
    parser.add_argument('-o', '--output', default='transcripts.txt',
                      help='Output file name (default: transcripts.txt)')
    
    # Add this argument after the optional arguments
    parser.add_argument('video_ids', nargs='+', 
                       help='YouTube video IDs (use -- before IDs that start with -)')
    
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        print("Error: For video IDs that start with '-', please use -- before the list of IDs")
        print("Example: python youtube_batch_transcriber.py -o output.txt -- -S83fysRwn4 Ipf247AmhiI")
        sys.exit(1)
    
    print(f"Fetching transcripts for {len(args.video_ids)} videos...")
    save_transcripts(args.video_ids, args.output)
    print(f"Transcripts saved to {args.output}")

if __name__ == "__main__":
    main() 