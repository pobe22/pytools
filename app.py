import streamlit as st
import os
import tempfile
import shutil
from datetime import datetime
from tools.seo_tool import (
    fetch_page,
    PDF,
    analyze_meta_tags,
    analyze_headings,
    analyze_images,
    analyze_links,
    analyze_load_time,
    analyze_structured_data,
    analyze_viewport,
    analyze_tfidf
)
from tools.soundcloud_downloader import download_playlist
from tools.pdf_tools import convert_and_merge_word_to_pdf
from tools.video_converter import avi_to_mp4


# --- Funktionen ---


def run_seo_analysis(url):
    soup = fetch_page(url)
    pdf = PDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    analyses = {
        "Meta Tags": analyze_meta_tags(soup),
        "Headings": analyze_headings(soup),
        "Images": analyze_images(soup),
        "Links": analyze_links(soup),
        "Load Time": analyze_load_time(url),
        "Structured Data": analyze_structured_data(soup),
        "Viewport": analyze_viewport(soup),
    }

    for title, data in analyses.items():
        pdf.add_chapter(f"{title} Analysis", data)

    tfidf_analysis = analyze_tfidf(soup)
    pdf.add_chapter(
        "TF-IDF Analysis",
        [f"{word}: {score:.2%}" for word, score in tfidf_analysis]
    )
    pdf.add_page()
    pdf.chapter_title("Top 10 Most Used Words (TF-IDF)")
    pdf.add_tfidf_table(tfidf_analysis)

    output_path = f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    pdf.output(output_path)
    return output_path


def run_soundcloud_downloader(url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    download_playlist(url, output_dir)
    return output_dir


def run_pdf_word_tools(uploaded_files, output_pdf):
    temp_dir = tempfile.mkdtemp()
    file_paths = []

    for f in uploaded_files:
        path = os.path.join(temp_dir, f.name)
        with open(path, "wb") as file:
            file.write(f.getbuffer())
        file_paths.append(path)

    convert_and_merge_word_to_pdf(file_paths, output_pdf)
    shutil.rmtree(temp_dir)
    return output_pdf


def run_video_converter(uploaded_file):
    temp_input = os.path.join(tempfile.gettempdir(), uploaded_file.name)
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.getbuffer())
    output_file = os.path.splitext(temp_input)[0] + ".mp4"
    avi_to_mp4(temp_input, output_file)
    return output_file


# --- Streamlit Layout ---


st.set_page_config(
    page_title="PyTools Dashboard", page_icon="🧰", layout="wide"
)
st.markdown(
    "<h1 style='text-align:center;'>🧰 PyTools Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "All-in-one toolkit for SEO, media & document automation</p>",
    unsafe_allow_html=True
)
st.divider()

tabs = st.tabs(
    [
        "🔍 SEO Analyzer",
        "🎵 SoundCloud Downloader",
        "📄 PDF/Word Tools",
        "🎬 Video Converter",
    ]
)

# --- SEO Tab ---
with tabs[0]:
    st.header("🔍 SEO Website Analyzer")
    st.info("Enter a website URL to generate a detailed SEO report as PDF.")
    url = st.text_input("Website URL:")
    if st.button("Start Analysis"):
        if url:
            with st.spinner("Analyzing website..."):
                pdf_path = run_seo_analysis(url)
            st.success("✅ Analysis complete!")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📥 Download PDF Report",
                    data=f,
                    file_name=os.path.basename(pdf_path)
                )

# --- SoundCloud Downloader ---
with tabs[1]:
    st.header("🎵 SoundCloud Playlist Downloader")
    st.info("Download an entire SoundCloud playlist and convert tracks to MP3.")
    sc_url = st.text_input("SoundCloud Playlist URL:")
    output_dir = st.text_input("Output folder (local path):")
    if st.button("Download Playlist"):
        if sc_url and output_dir:
            with st.spinner("Downloading playlist..."):
                run_soundcloud_downloader(sc_url, output_dir)
            st.success(
                f"✅ Download finished!\nFiles saved to {output_dir}"
            )

# --- PDF/Word Tools ---
with tabs[2]:
    st.header("📄 PDF & Word Tools")
    st.info("Upload Word or PDF files to convert and merge them into one PDF.")
    uploaded_files = st.file_uploader(
        "Upload files:", type=["docx", "pdf"], accept_multiple_files=True
    )
    output_name = st.text_input("Output PDF name:", value="merged_document.pdf")
    if st.button("Convert & Merge"):
        if uploaded_files:
            with st.spinner("Processing..."):
                output_pdf = run_pdf_word_tools(uploaded_files, output_name)
            st.success("✅ PDF created!")
            with open(output_pdf, "rb") as f:
                st.download_button(
                    "📥 Download PDF",
                    data=f,
                    file_name=os.path.basename(output_pdf)
                )

# --- Video Converter ---
with tabs[3]:
    st.header("🎬 AVI → MP4 Converter")
    st.info("Upload an AVI file to convert it into MP4 format.")
    uploaded_file = st.file_uploader("Select an AVI file:", type=["avi"])
    if uploaded_file and st.button("Convert Video"):
        with st.spinner("Converting video..."):
            output_path = run_video_converter(uploaded_file)
        st.success("✅ Conversion complete!")
        with open(output_path, "rb") as f:
            st.download_button(
                "📥 Download MP4",
                data=f,
                file_name=os.path.basename(output_path)
            )
