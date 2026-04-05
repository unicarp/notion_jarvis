"""
Notion AI Task Orchestrator - Audio Processing Service

This module handles the transcription od audio files using
the Groq Whisper API.
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client exclusively for audio processing
client = Groq(api_key=GROQ_API_KEY)

def transcribe_audio(file_path):
    """
    Transcribe an audio file to text using Whisper model.

    Args:
        file_path (str): The local path to the audio file.
    
    Returns:
        str: the transcribed text.
    
    Raises:
        Exception: If the API call fails.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file = (file_path, audio_file.read()),
                model = "whisper-large-v3",
                language = "es"
            )
        return transcription.text
    except Exception as e:
        raise Exception(f"Transcription failed: {e}")
