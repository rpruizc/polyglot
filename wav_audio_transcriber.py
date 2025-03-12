"""
WAV Audio Transcriber

Transcribes WAV audio files using the Whisper AI model.
Usage: python wav_audio_transcriber.py <audio_file_path> [--model base|small|medium|large]
"""

import os
import argparse
import whisper
import torch

class WhisperTranscriber:
    def __init__(self, model_name="base"):
        # Load model with weights_only=True to address the FutureWarning
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_name, device=device)
    
    def transcribe(self, audio_path):
        result = self.model.transcribe(audio_path)
        return result["text"]
    
    def save_transcript(self, text, original_filename):
        os.makedirs("transcripts", exist_ok=True)
        base_name = os.path.splitext(os.path.basename(original_filename))[0]
        output_path = os.path.join("transcripts", f"{base_name}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return output_path

def main():
    parser = argparse.ArgumentParser(description="Transcribe WAV file using OpenAI's Whisper")
    parser.add_argument("audio_path", help="Path to the WAV file")
    parser.add_argument("--model", default="base", help="Model to use (tiny, base, small, medium, large)")
    args = parser.parse_args()
    
    transcriber = WhisperTranscriber(model_name=args.model)
    transcribed_text = transcriber.transcribe(args.audio_path)
    output_path = transcriber.save_transcript(transcribed_text, args.audio_path)
    print(f"Transcription completed. Output saved to: {output_path}")

if __name__ == "__main__":
    main() 