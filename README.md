# Python Video Editing Tool

This project is a Python-based video editing tool that allows users to perform various video editing tasks, including trimming, merging, adjusting speed, adding background music, embedding subtitles, and using speech recognition to generate subtitles.

## Features

- **Trim Videos**: Cut specific parts of a video.
- **Merge Videos**: Combine multiple video files into one.
- **Adjust Speed**: Speed up or slow down the video playback.
- **Add Background Music**: Replace or add background music to a video.
- **Subtitles**: Automatically generate or manually add subtitles to a video.
- **Speech Recognition**: Use speech-to-text to generate subtitles from video audio.

## Libraries Used

- **MoviePy**: For video editing tasks like trimming, merging, adjusting speed, and adding background music.
- **FFmpeg**: For multimedia processing.
- **SpeechRecognition**: To convert video audio to text for subtitle generation.
- **Requests**: For making HTTP requests (e.g., interacting with APIs).
- **srt**: For working with SRT subtitle files (parsing, generating, editing).
- **Time** and **Pytz**: For handling time-related operations (e.g., timestamp management).

## Prerequisites

Before running the project, make sure you have:

- Python 3.x installed
- FFmpeg installed and added to your system path

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/vidtub.git

  
Navigate to the project directory:
```cd vid```

Create a virtual environment (optional but recommended):

```python -m venv venv```

Install the required dependencies:

```pip install -r requirements.txt```

