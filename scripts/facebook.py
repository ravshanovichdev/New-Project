import subprocess
from pathlib import Path
import requests
from yt_dlp import YoutubeDL
import re


def safe_filename(name: str) -> str:
    """Nomi xavfsiz bo'lishi uchun tozalash"""
    return re.sub(r'[^a-zA-Z0-9а-яА-Я._-]', '_', name)


def combine(audio_path: Path, video_path: Path, output_path: Path) -> None:
    """FFmpeg yordamida audio va videoni birlashtirish"""
    if output_path.exists():
        output_path.unlink()

    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c", "copy",
            str(output_path)
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr.decode()}")


def download(url: str, session_id: str):
    """Facebook video + audio yuklab olish"""
    output_dir = Path("./media_temp") / session_id
    output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info['formats']

        video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') == 'none']
        best_video = max(video_formats, key=lambda x: x.get('height', 0))

        audio_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
        best_audio = max(audio_formats, key=lambda x: x.get('abr', 0))

        base_name = safe_filename(info.get('title', 'video'))
        video_path = output_dir / f"{base_name}_video.{best_video['ext']}"
        audio_path = output_dir / f"{base_name}_audio.{best_audio['ext']}"
        output_path = output_dir / f"{base_name}_final.mp4"

        # Video yuklab olish
        r = requests.get(best_video['url'], stream=True)
        with open(video_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        # Audio yuklab olish
        r = requests.get(best_audio['url'], stream=True)
        with open(audio_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        # Birlashtirish
        combine(audio_path, video_path, output_path)

        return audio_path, video_path, output_path