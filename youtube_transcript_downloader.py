"""
YouTube Transcript Downloader

Downloads transcript from a single YouTube video by ID and saves it to a file.
Usage: python youtube_transcript_downloader.py <youtube_video_id>
"""

from youtube_transcript_api import YouTubeTranscriptApi
import sys
import os

def get_video_transcript(video_id, languages=['en', 'es']):
    """
    Get transcript from a YouTube video in specified languages.
    
    Args:
        video_id (str): YouTube video ID
        languages (list): List of language codes to try, in order of preference
                         Default is ['en', 'es'] for English and Spanish
    
    Returns:
        str: Formatted transcript text
    """
    try:
        # Get transcript in any of the specified languages
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        
        # Format transcript to plain text manually
        formatted_transcript = ""
        for entry in transcript:
            formatted_transcript += entry['text'] + "\n"
        
        return formatted_transcript
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        # Get available transcript languages
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            print("\nAvailable transcripts for this video:")
            
            # Get all transcripts and check if they're generated or manual
            transcripts = list(transcript_list)
            
            manual_transcripts = []
            auto_transcripts = []
            
            for transcript in transcripts:
                if transcript.is_generated:
                    auto_transcripts.append(transcript)
                else:
                    manual_transcripts.append(transcript)
            
            print("\nManually Created:")
            for transcript in manual_transcripts:
                print(f" - {transcript.language_code} ({transcript.language})")
            
            print("\nAuto-Generated:")
            for transcript in auto_transcripts:
                print(f" - {transcript.language_code} ({transcript.language})")
                
        except Exception as inner_e:
            print(f"Could not fetch transcript list: {str(inner_e)}")
        
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python youtube_transcript_downloader.py <youtube_video_id>")
        sys.exit(1)
        
    video_id = sys.argv[1]
    transcript = get_video_transcript(video_id)
    
    if transcript:
        # Create 'transcripts' directory if it doesn't exist
        os.makedirs('transcripts', exist_ok=True)
        
        # Write transcript to file
        output_file = os.path.join('transcripts', f'{video_id}.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        print(f"Transcript saved to: {output_file}") 