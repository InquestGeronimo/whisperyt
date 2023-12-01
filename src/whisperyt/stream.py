import os
import json
import base64
import subprocess
import asyncio
import websockets

import streamlink

from typing import Optional

class YouTubeStreamer:
    def __init__(
        self, 
        video_url: str, 
        output_filename: str, 
        timer_seconds: int
    ):
        """
        Initialize a YouTubeStreamer.

        :param video_url: The URL of the YouTube video to stream audio from.
        :param output_filename: The name of the output WAV file.
        :param timer_seconds: The maximum duration in seconds to stream audio.
        """
        self.video_url = video_url
        self.output_filename = output_filename
        self.timer_seconds = timer_seconds

    def stream_audio(self):
        """
        Stream audio from a YouTube video and save it as a WAV file.

        :return: None
        """
        # Check if the output file already exists and delete it if it does
        if os.path.exists(self.output_filename):
            os.remove(self.output_filename)

        session = streamlink.Streamlink()
        streams = session.streams(self.video_url)
        best_stream = streams['best']

        ffmpeg_command = [
            'ffmpeg',
            '-i', 'pipe:0',          # Input from pipe
            '-f', 'wav',             # Output format is WAV
            '-ar', '16000',          # Set sample rate to 16000 Hz
            '-ac', '2',              # Set audio channels to stereo (adjust as needed)
            '-sample_fmt', 's16',    # Set bit size to 16-bit
            self.output_filename      # Output file name
        ]

        with best_stream.open() as stream, \
             subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE) as ffmpeg_process:

            print("Opened the stream")

            start_time = asyncio.get_event_loop().time()
            try:
                while True:
                    audio_chunk = stream.read(1024)
                    if not audio_chunk:
                        break

                    # Write the audio chunk to FFmpeg's stdin
                    ffmpeg_process.stdin.write(audio_chunk)

                    # Check if the timer has been set and exceeded
                    if self.timer_seconds is not None:
                        elapsed_time = asyncio.get_event_loop().time() - start_time
                        if elapsed_time >= self.timer_seconds:
                            break

            except KeyboardInterrupt:
                pass

            print("Closed the stream and saved audio as WAV")

class StreamTranscriber(YouTubeStreamer):
    """
    A class for interacting with the Gladia audio transcription API via WebSocket.
    """

    ERROR_KEY = 'error'
    TYPE_KEY = 'type'
    TRANSCRIPTION_KEY = 'transcription'
    LANGUAGE_KEY = 'language'

    def __init__(self, api_key: str, wss_endpoint: str):
        """
        Initialize the StreamTranscriber instance.

        :param api_key: Your Gladia API key.
        :param wss_endpoint: WebSocket endpoint for Gladia API.
        """
        self.api_key = api_key
        self.wss_endpoint = wss_endpoint

    async def send_audio(
        self, 
        socket: websockets.WebSocketClientProtocol, 
        output_filename: str, 
        encoding: str
    ):
        """
        Send audio data to the Gladia API.

        :param socket: WebSocket connection to the Gladia API.
        :param output_filename: Name of the audio file for transcription.
        :param encoding: Encoding type for the audio data.
        """
        # Configure stream with a configuration message
        configuration = {
            "x_gladia_key": self.api_key,
            "encoding": encoding
            }
        
        await socket.send(json.dumps(configuration))

        with open(output_filename, 'rb') as f:
            file_sync = f.read()
        base64_frames = base64.b64encode(file_sync).decode('utf-8')
        part_size = 200000
        number_of_parts = -(-len(base64_frames) // part_size)

        # Split the audio data into parts and send them sequentially
        for i in range(number_of_parts):
            start = i * part_size
            end = min((i + 1) * part_size, len(base64_frames))
            part = base64_frames[start:end]

            # Delay between sending parts (500 milliseconds in this case)
            await asyncio.sleep(0.5)
            message = {'frames': part}
            await socket.send(json.dumps(message))

        await asyncio.sleep(2)

    async def receive_transcription(self, socket: websockets.WebSocketClientProtocol):
        """
        Receive and process transcriptions from the Gladia API.

        :param socket: WebSocket connection to the Gladia API.
        """
        while True:
            response = await socket.recv()
            utterance = json.loads(response)

            if not utterance:
                print('Empty response, waiting for the next utterance...')
                continue

            event_type = utterance.get(self.TYPE_KEY, "unknown")
            if event_type == "transcript":
                transcription = utterance.get(self.TRANSCRIPTION_KEY, "")
                language = utterance.get(self.LANGUAGE_KEY, "")
                print(f"Transcription: ({language}) {transcription}")
            elif event_type == "error":
                error_message = utterance.get(self.ERROR_KEY, "Unknown error")
                print(f"API Error: {error_message}")
            else:
                print(f"Received response: {utterance}")


    async def run_transcription(self, url, output_file, timer, encoding):
        """
        Run the audio transcription process.
        """
        streamer = YouTubeStreamer(
            video_url=url, 
            output_filename=output_file, 
            timer_seconds=timer
        )
        
        streamer.stream_audio()
        
        async with websockets.connect(self.wss_endpoint) as socket:
            send_task = asyncio.create_task(self.send_audio(socket, output_file, encoding))
            receive_task = asyncio.create_task(self.receive_transcription(socket))
            await asyncio.gather(send_task, receive_task)