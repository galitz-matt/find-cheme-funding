import fitz
import re
import requests

class PDFParser:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    def scrape_acknowledgments(self, pdf_url):
        try:

            doc = fitz.open("temp.pdf")
            text = ""
            for page in doc:
                text += page.get_text()

            match = re.search(r"(acknowledg(e)?ments?|funding).{0,20}\n(.*?)(\n\n|\Z)", text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(0).strip()
            else:
                return "Acknowledgements not found"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return "Error reading PDF"

