<div align="center">
    <img width="400" height="350" src="./img/whisperyt.png">
</div>

<br>

**WhisperYT** is a Python client for interacting with Gladia's [API](https://docs.gladia.io/reference/pre-recorded) designed specifically for transcribing YouTube videos. Powered by an optimized variant of OpenAI's Whisper model, Gladia's backend performs Automatic Speech Recognition (ASR), converting spoken words into written text with remarkable precision. Best of all, you can enjoy up to 10 hours of free API usage each month.

In addition to providing access to Gladia's API, this versatile library equips you with postprocessing features to effortlessly manipulate and refine your transcribed data, making it a valuable tool for post-transcription tasks.

## Install <img align="center" width="23" height="23" src="https://media.giphy.com/media/sULKEgDMX8LcI/giphy.gif">
<br>

```
pip install whisperyt
```

## Quick Start <img align="center" width="23" height="23" src="https://media.giphy.com/media/PeaNPlyOVPNMHjqTm7/giphy.gif">
<br>

The initial step involves initializing the `YouTubeTranscriber` class before proceeding with your API request. To get started, simply create a free account on [Gladia's site](https://app.gladia.io/?_gl=1*1thro73*_ga*MTI5MDgyMjkzMS4xNzAwMzE0NTc5*_ga_LMW59LN2SD*MTcwMDg3MTUwMy45LjAuMTcwMDg3MTUwMy4wLjAuMA..) and provide your API token. Afterwards, pass the YouTube video URL of your choice:

```py
from whisperyt import YouTubeTranscriber, DataProcessor

gladia = YouTubeTranscriber("YOUR-API-KEY")

response = gladia.transcribe("https://www.youtube.com/watch?v=BrcKRhQ7K00")
print(DataProcessor.pretty_json(response))
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

From Dataframe, display transcription by speaker turn:

```py
df = DataProcessor.get_table("output.json")
DataProcessor.print_transcription_by_turn(df)
```

Output:

<img align="center" width="650" height="250" src="./img/speakers.png">

---
### Best Practices with Gladia's API

**Audio Length**: The maximum length of audio that can be transcribed in a single request is currently 135 minutes. Attempts to transcribe longer audio files may result in errors.

**File Size**: Audio files must not exceed 500 MB in size. Larger files will not be accepted by the API.

**API Call Limits**: To ensure the quality of service and fairness to all users, API call limits have been implemented. For the free tier, users can make a maximum of 20 calls per hour, with up to 3 concurrent requests. Users subscribed to the Pro tier can make up to 200 calls per minute and up to 15 concurrent requests.

For further details, refer to the [documentation](https://docs.gladia.io/reference/limitations-and-best-practices).