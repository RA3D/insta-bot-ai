# Instagram Bot

This Python script automates interactions on Instagram, including posting comments and liking posts. It utilizes Selenium for web automation and a custom AI model for generating comments.

## Setup

1. Install Python if you haven't already.
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
3. Ensure you have Google Chrome installed.
4. Update config.py:

- Chrome Configuration
   ```bash
   CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   CHROME_ARGS = "--remote-debugging-port=9222 --user-data-dir='/Users/{user}/Library/Application Support/Google/Chrome' --profile-directory='Default'"
- OpenAI API Key   
   ```bash
   OPENAI_API_KEY = "OPENAI_API_KEY"
- Wit.ai API keys
   ```bash
   LANGUAGE_API_KEYS = {
       'EN': 'WIT_API_KEY_EN',
       'AR': 'WIT_API_KEY_AR',
       'FR': 'WIT_API_KEY_FR',
       'JA': 'WIT_API_KEY_JA',
   }

## Usage

1. Run the `main.py` script:
    ```bash
    python main.py

2. Follow the prompts to enter video links for transcription and language key.
3. The script will transcribe the videos, generate comments using AI, post comments, and like the posts automatically.

## Dependencies

- `selenium`: For web automation.
- `yt-dlp`: For downloading videos.
- `tafrigh`: For transcribing videos.
- `openai` for generating comments.