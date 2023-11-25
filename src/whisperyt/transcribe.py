import yt_dlp
import requests
import os

class YouTubeTranscriber:
    """
    A class for transcribing audio from YouTube videos.

    This class provides functionality to download YouTube videos and then
    utilize a transcription service to convert the audio from the video into text.
    The transcription service is accessed via an API, requiring an API key.

    Methods:
    - __init__(api_key): Initializes the YouTubeTranscriber with the required API key.
    - transcribe(url, toggle_diarization=True): Downloads a YouTube video from the given URL
      and sends its audio to the transcription service, returning the transcription response.

    Private Methods:
    - _download_video(url): Downloads the video from YouTube and returns the filename of the saved video.
    """
    
    def __init__(self, api_key):
        """
        Initialize the YouTubeTranscriber.
        :param api_key: API key for the transcription service.
        """
        self.api_endpoint = "https://api.gladia.io/audio/text/audio-transcription/"
        self.headers = {
            "accept": "application/json",
            "x-gladia-key": api_key,
        }

    def _download_video(self, url):
        """
        Private method to download video from YouTube. File is saved in working directory.
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

    def transcribe(self, url, toggle_diarization=True):
        """
        Transcribe the audio from a given YouTube URL.
        :param url: URL of the YouTube video.
        :param toggle_diarization: Option to toggle diarization (default is True).
        :return: Response object from the transcription request.
        """
        
        audio_path = self._download_video(url)
        if not os.path.exists(audio_path):
            print("- File does not exist")
            return None

        file_name, file_extension = os.path.splitext(audio_path)
        with open(audio_path, 'rb') as f:
            files = {
                'audio': (file_name, f, f'audio/{file_extension[1:]}'),
                'toggle_diarization': (None, str(toggle_diarization)),
            }

            try:
                response = requests.post(self.api_endpoint, headers=self.headers, files=files)
                response.raise_for_status()  # Raises a HTTPError if the response was an HTTP error
                return response
            except requests.RequestException as e:
                print(f"An error occurred: {e}")
                return None
