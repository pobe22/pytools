import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa: E402

import unittest  # noqa: E402
from tools.seo_tool import (  # noqa: E402
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


class TestSEOTool(unittest.TestCase):
    def setUp(self):
        # Beispiel-URL für Tests
        self.url = "https://www.example.com"
        self.soup = fetch_page(self.url)

    def test_fetch_page(self):
        self.assertIsNotNone(self.soup)
        self.assertTrue(hasattr(self.soup, 'find_all'))

    def test_analyze_meta_tags(self):
        result = analyze_meta_tags(self.soup)
        self.assertIsInstance(result, str)
        self.assertIn("Title", result)

    def test_analyze_headings(self):
        result = analyze_headings(self.soup)
        self.assertIsInstance(result, str)

    def test_analyze_images(self):
        result = analyze_images(self.soup)
        self.assertIsInstance(result, str)

    def test_analyze_links(self):
        result = analyze_links(self.soup)
        self.assertIsInstance(result, str)

    def test_analyze_load_time(self):
        result = analyze_load_time(self.url)
        self.assertIn("Page Load Time", result)

    def test_analyze_structured_data(self):
        result = analyze_structured_data(self.soup)
        self.assertIsInstance(result, str)

    def test_analyze_viewport(self):
        result = analyze_viewport(self.soup)
        self.assertIsInstance(result, str)

    def test_analyze_tfidf(self):
        result = analyze_tfidf(self.soup)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(t, tuple) for t in result))

    def test_pdf_generation(self):
        pdf = PDF()
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)

        analyses = {
            "Meta Tags": analyze_meta_tags(self.soup),
            "Headings": analyze_headings(self.soup),
            "Images": analyze_images(self.soup),
            "Links": analyze_links(self.soup),
            "Load Time": analyze_load_time(self.url),
            "Structured Data": analyze_structured_data(self.soup),
            "Viewport": analyze_viewport(self.soup),
        }

        for title, data in analyses.items():
            pdf.add_chapter(f"{title} Analysis", data)

        tfidf_analysis = analyze_tfidf(self.soup)
        pdf.add_chapter(
            "TF-IDF Analysis",
            [f"{word}: {score:.2%}" for word, score in tfidf_analysis]
        )

        output_path = "test_report.pdf"
        pdf.output(output_path)
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path)


if __name__ == "__main__":
    unittest.main()
