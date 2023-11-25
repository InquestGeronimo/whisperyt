import requests


class YouTubeTranscriber:
    def __init__(self, api_key):
        """
        Initialize the YouTubeTranscriber.

        :param cache_name: Name of the cache.
        :param api_key: API key for the transcription service.
        """

        self.headers = {
            "accept": "application/json",
            "x-gladia-key": api_key,
        }

    def transcribe(
        self, 
        video_url, 
        toggle_diarization="true",
        lang_behavior="automatic single language",
        lang="english",
    ):
        """
        Transcribe the audio from a given YouTube URL.

        :param video_url: URL of the YouTube video.
        :param toggle_diarization: Option to toggle diarization (default is 'true').
        :lang_behavior: Option for setting language detection (default is 'automatic single language').
        :lang: Option for setting the language of transcription (default is 'english').
        :return: Response object from the transcription request.
        """
        files = {
            "video_url": video_url,
            "language_behavior": lang_behavior,
            "language": lang,
            "toggle_diarization": toggle_diarization,
        }

        try:
            response = requests.post(
                "https://api.gladia.io/video/text/video-transcription/", headers=self.headers, files=files
            )
            response.raise_for_status()  # Raises a HTTPError if the response was an HTTP error
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
