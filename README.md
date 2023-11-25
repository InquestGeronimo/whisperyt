<img align="center" width="200" height="160" src="./img/whisperyt.png">

**WhisperYT** is a Python client for interacting with Gladia's [API](https://docs.gladia.io/reference/pre-recorded#sending-video-for-transcription) designed specifically for transcribing YouTube videos. Powered by an optimized variant of OpenAI's Whisper model, Gladia's backend performs Automatic Speech Recognition (ASR), converting spoken words into written text with remarkable precision. Best of all, you can enjoy up to 10 hours of free API usage each month.

In addition to providing access to Gladia's API, this versatile library equips you with postprocessing features to effortlessly manipulate and refine your transcribed data, making it a valuable tool for post-transcription tasks.

## Install <img align="center" width="23" height="23" src="https://media.giphy.com/media/sULKEgDMX8LcI/giphy.gif">
<br>

```
pip install whisperyt
```

## Quick Start <img align="center" width="23" height="23" src="https://media.giphy.com/media/PeaNPlyOVPNMHjqTm7/giphy.gif">
<br>

The initial step involves initializing the YouTubeTranscriber class before proceeding with your API request. To get started, simply create a free account on [Gladia's website](https://app.gladia.io/?_gl=1*1thro73*_ga*MTI5MDgyMjkzMS4xNzAwMzE0NTc5*_ga_LMW59LN2SD*MTcwMDg3MTUwMy45LjAuMTcwMDg3MTUwMy4wLjAuMA..) and provide your API token. Afterwards, pass the YouTube video URL of your choice:

```py
from whisperyt import YouTubeTranscriber, pretty_json

Gladia = YouTubeTranscriber("YOUR-API-KEY")
response = Gladia.transcribe("https://www.youtube.com/watch?v=BrcKRhQ7K00")
json_data = pretty_json(response)
```
Output:

<img align="center" width="250" height="400" src="./img/pretty-json.png">