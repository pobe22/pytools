import streamlit as st
import os
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

# --- SEO Tool ---
from tools.seo_tool import fetch_page, analyze_meta_tags, analyze_headings, analyze_images, analyze_links, analyze_load_time, analyze_tfidf, analyze_structured_data, analyze_viewport, PDF

def run_seo_analysis(url):
    soup = fetch_page(url)
    pdf = PDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    meta_tags_analysis = analyze_meta_tags(soup)
    headings_analysis = analyze_headings(soup)
    images_analysis = analyze_images(soup)
    links_analysis = analyze_links(soup)
    load_time_analysis = analyze_load_time(url)
    tfidf_analysis = analyze_tfidf(soup)
    structured_data_analysis = analyze_structured_data(soup)
    viewport_analysis = analyze_viewport(soup)

    pdf.add_chapter("Meta Tags Analysis", meta_tags_analysis)
    pdf.add_chapter("Headings Analysis", headings_analysis)
    pdf.add_chapter("Images Analysis", images_analysis)
    pdf.add_chapter("Links Analysis", links_analysis)
    pdf.add_chapter("Load Time Analysis", load_time_analysis)
    pdf.add_chapter("TF-IDF Analysis", [f'{word}: {score:.2%}' for word, score in tfidf_analysis])
    pdf.add_chapter("Structured Data Analysis", structured_data_analysis)
    pdf.add_chapter("Viewport Analysis", viewport_analysis)
    pdf.add_page()
    pdf.chapter_title("Top 10 Most Used Words (TF-IDF)")
    pdf.add_tfidf_table(tfidf_analysis)

    output_path = f'report_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.pdf'
    pdf.output(output_path)
    return output_path


# --- SoundCloud Downloader ---
from tools.soundcloud_downloader import download_playlist

def run_soundcloud_downloader(url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    download_playlist(url, output_dir)
    return output_dir


# --- PDF/Word Tools ---
from tools.pdf_tools import convert_and_merge_word_to_pdf

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


# --- Streamlit Interface ---
st.title("📦 Python Tools Dashboard")

menu = ["SEO Analyse", "SoundCloud Downloader", "PDF/Word Tools"]
choice = st.sidebar.selectbox("Wähle ein Tool", menu)

if choice == "SEO Analyse":
    url = st.text_input("Gib die URL ein:")
    if st.button("Analysieren"):
        if url:
            with st.spinner("Analyse läuft..."):
                pdf_path = run_seo_analysis(url)
            st.success("Analyse abgeschlossen!")
            st.download_button("Download PDF", data=open(pdf_path, "rb"), file_name=os.path.basename(pdf_path))

elif choice == "SoundCloud Downloader":
    sc_url = st.text_input("SoundCloud Playlist URL:")
    output_dir = st.text_input("Ausgabeordner (lokal):")
    if st.button("Download starten"):
        if sc_url and output_dir:
            with st.spinner("Download läuft..."):
                run_soundcloud_downloader(sc_url, output_dir)
            st.success(f"Download abgeschlossen! Dateien liegen in {output_dir}")

elif choice == "PDF/Word Tools":
    uploaded_files = st.file_uploader("Word/PDF-Dateien hochladen", type=["docx","pdf"], accept_multiple_files=True)
    output_name = st.text_input("Name der zusammengeführten PDF:", value="zusammengefuegte_Datei.pdf")
    if st.button("Konvertieren & Zusammenfügen"):
        if uploaded_files:
            with st.spinner("Verarbeitung läuft..."):
                output_pdf = run_pdf_word_tools(uploaded_files, output_name)
            st.success("PDF erstellt!")
            st.download_button("Download PDF", data=open(output_pdf, "rb"), file_name=os.path.basename(output_pdf))
