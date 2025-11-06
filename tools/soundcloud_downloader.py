import yt_dlp
import os


def download_playlist(playlist_url, output_dir, ffmpeg_path=None):
    if ffmpeg_path is None:
        ffmpeg_path = "ffmpeg"  # default für Linux/Windows im PATH

    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'ffmpeg_location': ffmpeg_path,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'geo_bypass': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
        except yt_dlp.utils.DownloadError as e:
            print(f"Fehler beim Herunterladen: {e}")
