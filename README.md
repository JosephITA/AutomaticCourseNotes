# AutomaticCourseNotes

This repository provides a simple script for automatically downloading and transcribing videos from an online course.

The script `course_transcriber.py` uses Selenium to log in to a course website, download each video found on the page, and transcribe the audio using [OpenAI's Whisper](https://github.com/openai/whisper). Transcripts are stored in the `transcripts` folder.

## Requirements

- Python 3.8+
- `selenium`
- `webdriver_manager`
- `requests`
- `whisper` (requires `ffmpeg`)
- `pyvirtualdisplay` to create a virtual `Xvfb` display when running headless
- A compatible browser (Chrome) installed

Install dependencies with:

```bash
pip install selenium webdriver-manager requests whisper pyvirtualdisplay
```

### System packages

The script relies on `ffmpeg` for audio processing and `Xvfb` for running the
browser in headless mode. Install them using your system package manager,
for example:

```bash
sudo apt-get install ffmpeg xvfb
```

## Usage

After installing these tools and dependencies, run the script and provide the
course URL along with your login credentials when prompted:

```bash
python course_transcriber.py
```

After logging in, the script searches the page for `<video>` elements, downloads each video's source file, transcribes the audio and saves a text file under `transcripts/`. After every video the script will ask whether to proceed to the next one.

Selectors for the login form and video elements may need to be adjusted depending on the course website structure.
