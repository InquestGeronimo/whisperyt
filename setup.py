from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.1.2"
DESCRIPTION = "Using Gladia's Whisper API for transcribing YouTube videos"
LONG_DESCRIPTION = "Use Whisper speech-to-text to transcribe YouTube videos and run postprocessing with the transcription."
DEPENDENCIES = ["requests>=2.31.0", "pandas>=2.1.3", "yt_dlp>=2023.11.16, streamlink>=6.4.2"]
# Setting up
setup(
    name="whisperyt",
    version=VERSION,
    author="InquestGeronimmo",
    author_email="rcostanl@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=,
    keywords=["python", "youtube", "whisper", "transcription", "speech-to-text", "ASR"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)