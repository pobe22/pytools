import os
import subprocess
from PyPDF2 import PdfMerger
import platform


def merge_pdfs(pdf_files, output_path):
    merger = PdfMerger()
    for pdf in pdf_files:
        if os.path.exists(pdf):
            merger.append(pdf)
        else:
            print(f"Datei nicht gefunden: {pdf}")
    merger.write(output_path)
    merger.close()
    print(f"Zusammengeführte PDF gespeichert: {output_path}")


def word_to_pdf(input_path, output_path):
    system = platform.system()
    if system == "Windows":
        import comtypes.client
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False
        try:
            doc = word.Documents.Open(input_path)
            doc.SaveAs(output_path, FileFormat=17)  # 17 = PDF
            doc.Close()
        finally:
            word.Quit()
    else:
        # Linux / macOS
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf",
                        "--outdir", os.path.dirname(output_path), input_path],
                       check=True)


def convert_and_merge_word_to_pdf(word_files, output_pdf):
    temp_pdf_files = []
    for word_file in word_files:
        if not os.path.exists(word_file):
            print(f"Datei nicht gefunden: {word_file}")
            continue
        if not word_file.lower().endswith(('.doc', '.docx')):
            print(f"Ungültige Datei: {word_file}")
            continue
        temp_pdf = os.path.splitext(word_file)[0] + "_temp.pdf"
        word_to_pdf(word_file, temp_pdf)
        temp_pdf_files.append(temp_pdf)


    if temp_pdf_files:
        merge_pdfs(temp_pdf_files, output_pdf)
        # temporäre Dateien löschen
        for temp_pdf in temp_pdf_files:
            os.remove(temp_pdf)
    else:
        print("Keine Dateien zur Verarbeitung gefunden.")
