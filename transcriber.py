import subprocess
from collections import deque
from pathlib import Path

from tafrigh import Config, TranscriptType, farrigh

from config import LANGUAGE_API_KEYS


def download_youtube_audio(youtube_url):
    download_dir = Path('./downloads')
    download_dir.mkdir(parents=True, exist_ok=True)

    # Clear previous downloads to avoid conflicts
    # for file in download_dir.iterdir():
    #     if file.is_file():
    #         file.unlink()

    # Get the video ID using yt-dlp with the --get-id option
    command_get_id = ['yt-dlp', '--get-id', youtube_url]
    result = subprocess.run(command_get_id, stdout=subprocess.PIPE, text=True, check=True)
    video_id = result.stdout.strip()

    # Specify the expected output path
    output_path = download_dir / f"{video_id}.wav"

    # Download and convert video to WAV, specifying the output path directly
    command = [
        'yt-dlp', '-x', '--audio-format', 'wav', '--audio-quality', '0',
        '--postprocessor-args', 'ffmpeg:-acodec pcm_s16le',
        '-o', str(output_path), youtube_url
    ]
    subprocess.run(command, check=True)

    # Check if the file exists before returning
    if not output_path.exists():
        raise FileNotFoundError(f"Expected WAV file not found: {output_path}")
    return output_path


def transcribe_file(file_path, language_sign):
    wit_api_key = LANGUAGE_API_KEYS.get(language_sign.upper())
    if not wit_api_key:
        print(f"API key not found for language: {language_sign}")
        return "API key not found"

    config = Config(
        urls_or_paths=[str(file_path)],
        skip_if_output_exist=False,
        playlist_items="",
        verbose=False,
        model_name_or_path="",
        task="",
        language="",
        use_faster_whisper=False,
        beam_size=0,
        ct2_compute_type="",
        wit_client_access_tokens=[wit_api_key],
        max_cutting_duration=5,
        min_words_per_segment=1,
        save_files_before_compact=False,
        save_yt_dlp_responses=False,
        output_sample=0,
        output_formats=[TranscriptType.TXT],
        output_dir=str(file_path.parent),
    )

    progress = deque(farrigh(config), maxlen=0)
    transcript_path = file_path.parent / (file_path.stem + '.txt')
    with open(transcript_path, 'r') as file:
        transcript = file.read()
    return transcript


def transcribe_link(youtube_url, language_sign):
    audio_file = download_youtube_audio(youtube_url)
    transcription_text = transcribe_file(audio_file, language_sign)
    return transcription_text
