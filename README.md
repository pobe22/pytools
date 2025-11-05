# Pytools

## SEO Optimizer

This program allows you to perform SEO optimization for your website.

### Usage
Start the program and enter the URL of your website. The program will generate a PDF report with SEO suggestions and optimization insights for your site.

---

## SoundCloud Playlist Downloader

This project is a Python-based downloader that fetches audio from SoundCloud playlists and converts the files to MP3 format using `yt-dlp` and `FFmpeg`. It handles playlists, bypasses geo-restrictions, and ensures any download errors are handled gracefully.

### Features
- Downloads SoundCloud playlists.
- Converts audio to MP3 format using `FFmpeg`.
- Customizes audio quality (default 192 kbps).
- Automatically creates the output directory if it doesn't exist.
- Bypasses geo-restricted tracks.
- Handles download errors with a clear error message.

### Usage
1. Run the program.
2. Provide the URL of the SoundCloud playlist.
3. The MP3 files will be saved in the specified output folder.

---

## PDF Converter

The PDF Converter is a tool to create, merge, and manipulate PDF files programmatically.

### Features
- Convert HTML, text, or other documents into PDF.
- Merge multiple PDFs into a single document.
- Split PDFs into individual pages.
- Add metadata (title, author, subject) to PDFs.
- Rotate, watermark, or annotate PDF pages.
- Compatible with Python 3.8+ using `fpdf2` and `PyPDF2`.

### Usage
1. Run the converter script.
2. Specify input files or content.
3. Configure output options (filename, directory, metadata).
4. The program will generate the PDF or merged PDF file.

---

## Requirements

```text
streamlit>=1.25
requests>=2.32
beautifulsoup4>=4.12
scikit-learn>=1.4,<1.6
fpdf2>=2.7
PyPDF2>=3.0,<3.1
yt-dlp>=2025.10.31.222828.dev0
