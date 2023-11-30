import yt_dlp
import os
import requests
import json

class Downloader:
    @staticmethod
    def download_video(url: str) -> str:
        """
        Download a video from YouTube and save it in the working directory.

        :param url: URL of the YouTube video.
        :return: File path of the downloaded video.
        """
        
        ydl_opts = {
            'outtmpl': '%(id)s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            video = result.get('entries', [result])[0]
            return f"{video['id']}.{video['ext']}"

class Transcriber(Downloader):
    def __init__(self, api_key: str, api_endpoint: str):
        """
        Initialize a Transcriber instance with the specified API endpoint.

        :param api_endpoint: The endpoint for the transcription service API.
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def transcribe_audio(self, url: str, toggle_diarization: bool):
        """
        Process an audio file from a YouTube video and send it to the transcription service.

        :param api_key: API key for the transcription service.
        :param url: URL of the YouTube video.
        :param toggle_diarization: Option to toggle diarization (default is True).
        :return: Response object from the transcription request.
        """
        audio_path = Downloader.download_video(url)
        if not os.path.exists(audio_path):
            print("- File does not exist")
            return None

        file_name, file_extension = os.path.splitext(audio_path)

        headers = {
            "accept": "application/json",
            "x-gladia-key": self.api_key,
        }
        with open(audio_path, 'rb') as f:
            files = {
                'audio': (file_name, f, f'audio/{file_extension[1:]}'),
                'toggle_diarization': str(toggle_diarization).lower(),
            }

            print("\nSending Request to API...")
            try:
                response = requests.post(self.api_endpoint, headers=headers, files=files)
                response.raise_for_status()  # Raises an HTTPError if the response was an HTTP error
                return response

            except requests.RequestException as e:
                print(f"An error occurred: {e}")
                return None
