import os
import re
import subprocess
from pathlib import Path
from pytubefix import YouTube # type: ignore
from pytubefix.cli import on_progress # type: ignore


def safe_filename(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9а-яА-Я._-]', '_', name)


def combine(audio_path: Path, video_path: Path, output_path: Path) -> None:
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
    yt = YouTube(url=url, on_progress_callback=on_progress)

    video_stream = yt.streams.filter(type="video").order_by("resolution").desc().first()
    audio_stream = yt.streams.filter(mime_type="audio/mp4").order_by("filesize").desc().first()

    output_dir = Path("./media_temp") / session_id
    output_dir.mkdir(parents=True, exist_ok=True)

    base_name = safe_filename(yt.title)
    video_path = output_dir / f"{base_name}_video.mp4"
    audio_path = output_dir / f"{base_name}_audio.mp4"
    output_path = output_dir / f"{base_name}_final.mp4"

    video_stream.download(output_path=output_dir, filename=video_path.name)
    audio_stream.download(output_path=output_dir, filename=audio_path.name)

    combine(audio_path, video_path, output_path)

    return audio_path, video_path, output_path





