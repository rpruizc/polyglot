# Transcriptor - Media Transcription Utilities

A collection of utilities for working with transcripts from various sources, including YouTube videos, audio files, and PDFs.

## Available Scripts

### YouTube Transcripts

- **youtube_transcript_downloader.py** - Downloads transcript from a single YouTube video.
  ```
  python youtube_transcript_downloader.py <youtube_video_id>
  ```

- **youtube_batch_transcriber.py** - Fetches and combines transcripts from multiple YouTube videos.
  ```
  python youtube_batch_transcriber.py -o output.txt video_id1 video_id2 ...
  ```

### Audio Transcription

- **wav_audio_transcriber.py** - Transcribes WAV audio files using Whisper AI.
  ```
  python wav_audio_transcriber.py <audio_file_path> [--model base|small|medium|large]
  ```

- **spanish_audio_transcriber.py** - Specialized for transcribing Spanish audio files, optimized for M1 Macs.
  ```
  python spanish_audio_transcriber.py <audio_file_path> [--model medium]
  ```

### Document Processing

- **pdf_text_extractor.py** - Extracts text from PDF files.
  ```
  python pdf_text_extractor.py <pdf_file_path>
  ```

- **images_to_pdf_converter.py** - Converts a folder of image files to a single PDF.
  ```
  python images_to_pdf_converter.py <image_directory>
  ```

- **web_docs_scraper.py** - Scrapes and cleans documentation from websites.
  ```
  python web_docs_scraper.py <website_url>
  ```

## Output Organization

- YouTube transcripts are saved to the `transcripts/` directory
- PDF extractions are saved to the `extractions/` directory
- Web content is saved based on domain name 