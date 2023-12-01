<div align="center">
    <img width="400" height="350" src="./img/whisperyt.png">
</div>

<br>

**WhisperYT** is a Python client for interacting with Gladia's [API](https://docs.gladia.io/reference/pre-recorded) designed specifically for transcribing YouTube videos. Powered by an optimized variant of OpenAI's Whisper model, Gladia's backend performs Automatic Speech Recognition (ASR), converting spoken words into written text with remarkable accuracy, speed, 99+ supported languages, code switching, auto-language detection, speaker diarization and word-level timestamp. Best of all, you can enjoy up to 10 hours of free API usage each month.

In addition to providing access to Gladia's API, this versatile library equips you with postprocessing features to manipulate and refine your transcribed data, making it a valuable tool for post-transcription downstream tasks.

>**Please note**: WhisperYT currently works for both pre-recorded and live YouTube videos, although the live feature is experimental and under development.

# Install <img align="center" width="30" height="29" src="https://media.giphy.com/media/sULKEgDMX8LcI/giphy.gif">
<br>

```
pip install whisperyt
```

# Quick Start <img align="center" width="30" height="29" src="https://media.giphy.com/media/PeaNPlyOVPNMHjqTm7/giphy.gif">
<br>

The initial step involves initializing the `YouTubeTranscriber` class before proceeding with your API request. To get started, simply create a free account on [Gladia's site](https://app.gladia.io/?_gl=1*1thro73*_ga*MTI5MDgyMjkzMS4xNzAwMzE0NTc5*_ga_LMW59LN2SD*MTcwMDg3MTUwMy45LjAuMTcwMDg3MTUwMy4wLjAuMA..) and provide your API token. Afterwards, pass the YouTube video URL of your choice:

```py
from whisperyt import YouTubeTranscriber, DataProcessor

gladia = YouTubeTranscriber("YOUR-API-KEY")

response = gladia.transcribe("https://www.youtube.com/watch?v=BrcKRhQ7K00")
response = DataProcessor.pretty_json(response)
print(response)
```
Chunk of output:

<img align="center" width="250" height="440" src="./img/pretty-json.png">

---
### Save Transcription to JSON File

```py
from whisperyt import YouTubeTranscriber, DataProcessor

gladia = YouTubeTranscriber("YOUR-API-KEY")

response = gladia.transcribe("https://www.youtube.com/watch?v=BrcKRhQ7K00")
DataProcessor.save_json_file(response.json(), "output.json")
```
---
### View Transcription in Pandas Dataframe

After your transcription has been saved in a JSON file, you can load it in a Pandas Dataframe:

```py
df = DataProcessor.get_table("output.json")
print(df)
```

Output:

<img align="center" width="700" height="95" src="./img/dataframe.png">

---

### View Transcription by Speaker Turn:

From Dataframe, print transcription by speaker turn:

```py
df = DataProcessor.get_table("output.json")
DataProcessor.print_transcription_by_turn(df)
```

Output:

<img align="center" width="650" height="250" src="./img/speakers.png">

---

# Transcribing Live YouTube Videos <img align="center" width="100" height="60" src="https://media.giphy.com/media/13Nc3xlO1kGg3S/giphy.gif">

**Status**: This feature is currently experimental and may not be stable. It is under active development, and we encourage users to test it and provide feedback.

Make sure you have `ffmpeg` installed on your machine and is accessible from the command line. You can download FFmpeg from the [official website](https://www.ffmpeg.org/download.html).

```py
gladia = YouTubeTranscriber("YOUR-API-KEY")

response = gladia.transcribe("https://www.youtube.com/watch?v=OBZqP69fOCE", stream=True)
```

**Streaming Options**: You can customize the streaming behavior by specifying the `output_file` to save the audio locally, set a `timer` to control the maximum duration of the stream, and choose the `encoding` format for the streamed audio, default is `WAV`. These options allow you to tailor the streaming experience to your specific needs while leveraging the power of real-time transcription.

---
### Best Practices with Gladia's API

**Audio Length**: The maximum length of audio that can be transcribed in a single request is currently 135 minutes. Attempts to transcribe longer audio files may result in errors.

**File Size**: Audio files must not exceed 500 MB in size. Larger files will not be accepted by the API.

**API Call Limits**: To ensure the quality of service and fairness to all users, API call limits have been implemented. For the free tier, users can make a maximum of 20 calls per hour, with up to 3 concurrent requests. Users subscribed to the Pro tier can make up to 200 calls per minute and up to 15 concurrent requests.

For further details, refer to the [documentation](https://docs.gladia.io/reference/limitations-and-best-practices).