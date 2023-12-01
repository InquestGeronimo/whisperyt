import requests
import asyncio
from typing import Optional

from .prerecorded import Transcriber
from .stream import StreamTranscriber

class YouTubeTranscriber(Transcriber, StreamTranscriber):
    """
    A class for transcribing audio from YouTube videos.

    This class provides functionality to transcribe YouTube videos and then
    utilize Gladia's transcription API to convert the audio from the video into text.

    Methods:
    - __init__(api_key): Initializes the YouTubeTranscriber with the required API key.
    - transcribe(url, toggle_diarization=True): Downloads a YouTube video from the given URL
      and sends its audio to the transcription service, returning the transcription response.
    """
    
    def __init__(self, api_key: str) -> None:
        """
        Initialize the YouTubeTranscriber.
        :param api_key: API key for the transcription service.
        :param api_endpoint: URL for HTTP API calls.
        :param wss_endpoint: URL for Websocket API calls.
        """
        
        self.api_key = api_key
        self.api_endpoint = "https://api.gladia.io/audio/text/audio-transcription/"
        self.wss_endpoint = "wss://api.gladia.io/audio/text/audio-transcription"

    def transcribe(
        self, 
        url: str,
        toggle_diarization: bool = True,
        stream: bool = False,
        output_file: str = "output.wav",
        timer: int = 10,
        encoding: str = "WAV"
    ) -> Optional[requests.Response]:
        """
        Transcribe the audio from a given YouTube URL.
        :param url: URL of the YouTube video.
        :param toggle_diarization: Option to toggle diarization (default is True).
        :param streaming: If True, stream audio using YouTubeAudioStreamer (default is False).
        :param output_filename: Output filename for streaming only (default is 'output.wav').
        :param timer_seconds: Timer duration in seconds for streaming only (default is 10).
        :return: Response object from the transcription request.
        """
        
        if not stream:
            transcriber = Transcriber(self.api_key, self.api_endpoint)
            transcription =  transcriber.transcribe_audio(url, toggle_diarization)
            return transcription
        else:
            s_transcriber = StreamTranscriber(self.api_key, self.wss_endpoint)
            asyncio.run(s_transcriber.run_transcription(url, output_file, timer, encoding))