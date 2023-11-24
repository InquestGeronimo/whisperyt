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

    def transcribe(self, audio_url, toggle_diarization="true"):
        """
        Transcribe the audio from a given YouTube URL.

        :param audio_url: URL of the YouTube video.
        :param toggle_diarization: Option to toggle diarization (default is 'true').
        :return: Response object from the transcription request.
        """
        files = {
            "audio_url": (None, audio_url),
            "toggle_diarization": (None, toggle_diarization)
        }

        try:
            response = requests.post("https://api.gladia.io/audio/text/audio-transcription/",
                                         headers=self.headers, files=files)
            response.raise_for_status()  # Raises a HTTPError if the response was an HTTP error
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None






# Usage
# API_KEY = "0a84339b-c22b-471a-aa1a-860365a5e985"
# Gladia = YouTubeTranscriber(API_KEY)
# response = Gladia.transcribe("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
# json_data = pretty_json(response)
# save_json_to_file(json_data, "output.json")
# df = get_table("output.json")
# get_transcription_by_turn(df)
# get_full_transcription("output.json")
# get_transcription_speaker("output.json")