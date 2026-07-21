"""
Voice Processor - Handles audio input/output processing (Optional)
"""

import io
from typing import Optional
from pathlib import Path

from app.config import settings


class VoiceProcessor:
    """Voice processing for speech-to-text and text-to-speech."""

    def __init__(self):
        self.whisper_model = None
        self.tts_engine = None
        self._whisper_available = False
        self._tts_available = False
        self._check_dependencies()

    def _check_dependencies(self):
        """Check if voice processing dependencies are available."""
        try:
            import whisper
            self._whisper_available = True
        except ImportError:
            print("Warning: Whisper not installed. Voice input disabled.")

        try:
            import pyttsx3
            self._tts_available = True
        except ImportError:
            print("Warning: pyttsx3 not installed. Voice output disabled.")

    async def speech_to_text(self, audio_data: bytes) -> str:
        """
        Convert speech audio to text using Whisper.

        Args:
            audio_data: Audio bytes

        Returns:
            Transcribed text
        """
        if not self._whisper_available:
            raise RuntimeError("Whisper not installed. Install with: pip install openai-whisper")

        if self.whisper_model is None:
            import whisper
            self.whisper_model = whisper.load_model(settings.WHISPER_MODEL)

        # Save audio to temporary file
        temp_path = Path("./data/temp_audio.wav")
        temp_path.parent.mkdir(parents=True, exist_ok=True)

        with open(temp_path, "wb") as f:
            f.write(audio_data)

        # Transcribe
        result = self.whisper_model.transcribe(str(temp_path))

        # Cleanup
        temp_path.unlink(missing_ok=True)

        return result["text"]

    async def text_to_speech(self, text: str) -> bytes:
        """
        Convert text to speech.

        Args:
            text: Text to convert

        Returns:
            Audio bytes
        """
        if not self._tts_available:
            raise RuntimeError("pyttsx3 not installed. Install with: pip install pyttsx3")

        if self.tts_engine is None:
            import pyttsx3
            self.tts_engine = pyttsx3.init()

        # Save to bytes buffer
        buffer = io.BytesIO()

        # Configure voice
        voices = self.tts_engine.getProperty("voices")
        if voices:
            self.tts_engine.setProperty("voice", voices[0].id)

        self.tts_engine.setProperty("rate", 150)

        # Save to file then read
        output_path = Path("./data/temp_speech.wav")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        self.tts_engine.save_to_file(text, str(output_path))
        self.tts_engine.runAndWait()

        with open(output_path, "rb") as f:
            audio_bytes = f.read()

        # Cleanup
        output_path.unlink(missing_ok=True)

        return audio_bytes

    async def process_audio_query(self, audio_data: bytes) -> str:
        """
        Process audio query: convert speech to text.

        Args:
            audio_data: Audio bytes from user

        Returns:
            Transcribed query text
        """
        return await self.speech_to_text(audio_data)
