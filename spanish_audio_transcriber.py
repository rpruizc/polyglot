"""
Spanish Audio Transcriber

Transcribes Spanish audio files using the Whisper AI model.
Optimized for M1 MacBooks.
Usage: python spanish_audio_transcriber.py <audio_file_path>
"""

import os
import argparse
import whisper
import torch
from pathlib import Path
import logging
from tqdm import tqdm
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WhisperTranscriber:
    def __init__(self, model_name="medium", language="es"):
        """
        Initialize WhisperTranscriber with speed optimizations for M1 MacBook.
        We use the medium model as it offers a good balance of speed and accuracy.
        """
        try:
            # Track initialization time
            start_time = time.time()
            
            # Use MPS (Metal Performance Shaders) if available
            if torch.backends.mps.is_available():
                self.device = torch.device("mps")
                logger.info("Using Metal Performance Shaders (MPS) for acceleration")
            else:
                self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                logger.info(f"Using device: {self.device}")
            
            # Load the model
            self.model = whisper.load_model(model_name, device=self.device)
            self.language = language
            
            # Log initialization time
            elapsed_time = time.time() - start_time
            logger.info(f"Model '{model_name}' loaded in {elapsed_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Error initializing transcriber: {e}")
            raise
    
    def transcribe(self, audio_path):
        """Transcribe audio file using Whisper model"""
        try:
            logger.info(f"Transcribing: {audio_path}")
            start_time = time.time()
            
            # Load and transcribe the audio
            result = self.model.transcribe(
                audio_path,
                language=self.language,
                verbose=False,
                fp16=(self.device.type == "cuda")  # Use FP16 for CUDA
            )
            
            elapsed_time = time.time() - start_time
            audio_duration = result.get("duration", 0)
            
            if audio_duration > 0:
                speed_ratio = audio_duration / elapsed_time
                logger.info(f"Transcription completed in {elapsed_time:.2f} seconds " +
                           f"({speed_ratio:.2f}x real-time)")
            else:
                logger.info(f"Transcription completed in {elapsed_time:.2f} seconds")
                
            return result
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise

    def save_transcript(self, result, original_filename):
        """Save transcription result to text file"""
        try:
            # Extract path and filename without extension
            path = Path(original_filename)
            base_name = path.stem
            
            # Create output directory if it doesn't exist
            os.makedirs("transcripts", exist_ok=True)
            
            # Basic transcript (text only)
            text_output_path = os.path.join("transcripts", f"{base_name}.txt")
            with open(text_output_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            # Detailed transcript (with timestamps)
            detailed_output_path = os.path.join("transcripts", f"{base_name}_detailed.txt")
            with open(detailed_output_path, "w", encoding="utf-8") as f:
                f.write(f"Transcript for: {original_filename}\n\n")
                
                for segment in result["segments"]:
                    start_time = format_timestamp(segment["start"])
                    end_time = format_timestamp(segment["end"])
                    text = segment["text"]
                    f.write(f"[{start_time} --> {end_time}] {text}\n")
            
            logger.info(f"Basic transcript saved to: {text_output_path}")
            logger.info(f"Detailed transcript saved to: {detailed_output_path}")
            
            return text_output_path, detailed_output_path
            
        except Exception as e:
            logger.error(f"Error saving transcript: {e}")
            raise

def format_timestamp(seconds):
    """Format time in seconds to HH:MM:SS format"""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:05.2f}"

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe Spanish audio files using Whisper AI"
    )
    parser.add_argument(
        "audio_path", 
        help="Path to the audio file to transcribe"
    )
    parser.add_argument(
        "--model", 
        default="medium", 
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model to use (default: medium)"
    )
    args = parser.parse_args()
    
    try:
        transcriber = WhisperTranscriber(model_name=args.model)
        result = transcriber.transcribe(args.audio_path)
        transcriber.save_transcript(result, args.audio_path)
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 