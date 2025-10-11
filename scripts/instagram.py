import instaloader
from moviepy import VideoFileClip
import os
import re
from pathlib import Path


def safe_filename(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9а-яА-Я._-]', '_', name)


def instagram_video(url: str, session_id: str) -> Path:
    output_dir = Path("./media_temp") / session_id
    output_dir.mkdir(parents=True, exist_ok=True)

    loader = instaloader.Instaloader(dirname_pattern=str(output_dir), save_metadata=False)

    shortcode_match = re.search(r"instagram\.com/(?:p|reel)/([a-zA-Z0-9_-]+)", url)
    if not shortcode_match:
        raise ValueError("Неверная ссылка на пост Instagram")

    shortcode = shortcode_match.group(1)
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    loader.download_post(post, target=output_dir)

    for file in os.listdir(output_dir):
        if file.endswith(".mp4"):
            return output_dir / file

    raise FileNotFoundError("Видео не найдено")


def instagram_audio(video_path: Path) -> Path:
    audio_path = video_path.with_suffix(".mp3")
    clip = VideoFileClip(str(video_path))
    clip.audio.write_audiofile(str(audio_path))
    clip.close()
    return audio_path
