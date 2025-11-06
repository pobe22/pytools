import os
import pytest
from app import (
    run_seo_analysis,
    run_soundcloud_downloader,
    run_pdf_word_tools,
    run_video_converter
)


# --- SEO Tests ---


def test_run_seo_analysis_creates_pdf(tmp_path):
    # Verwende eine bekannte URL
    url = "https://example.com"
    output_pdf = run_seo_analysis(url)
    assert os.path.exists(output_pdf)
    # Optional: PDF-Datei löschen nach Test
    os.remove(output_pdf)


# --- SoundCloud Tests ---


@pytest.mark.skip(reason="Requires network access and a real playlist URL")
def test_run_soundcloud_downloader(tmp_path):
    url = "https://soundcloud.com/artist/playlist"
    output_dir = tmp_path / "downloads"
    os.makedirs(output_dir, exist_ok=True)
    run_soundcloud_downloader(url, str(output_dir))
    # Prüfen, ob Dateien heruntergeladen wurden
    assert len(os.listdir(output_dir)) > 0


# --- PDF/Word Tools Tests ---


def test_run_pdf_word_tools_creates_pdf(tmp_path):
    # Erstelle Dummy-Dateien
    dummy_file1 = tmp_path / "test1.docx"
    dummy_file1.write_text("Hello world")
    dummy_file2 = tmp_path / "test2.docx"
    dummy_file2.write_text("Another file")

    uploaded_files = [
        type("File", (), {"name": "test1.docx", "getbuffer": lambda: b"Hello world"})(),
        type("File", (), {"name": "test2.docx", "getbuffer": lambda: b"Another file"})()
    ]

    output_pdf = tmp_path / "merged.pdf"
    run_pdf_word_tools(uploaded_files, str(output_pdf))
    assert os.path.exists(output_pdf)


# --- Video Converter Tests ---


@pytest.mark.skip(reason="Requires actual AVI file and ffmpeg")
def test_run_video_converter(tmp_path):
    uploaded_file = type(
        "File", (), {"name": "test.avi", "getbuffer": lambda: b"dummycontent"}
    )()
    output_file = run_video_converter(uploaded_file)
    assert output_file.endswith(".mp4")
    # Optional: löschen
    if os.path.exists(output_file):
        os.remove(output_file)
