import logging
import requests
import os

logger = logging.getLogger(__name__)

class PDFDownloader:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    def __init__(self, unpaywall_client, selenium_client):
        self.unpaywall_client = unpaywall_client
        self.selenium_client = selenium_client

    def download_pdf(self, url):
        doi = self.unpaywall_client.parse_doi(url).replace("/", "-")
        pdf_url = self.unpaywall_client.get_oa_pdf_url(url)

        logger.info(f"Downloading {pdf_url}")
        res = requests.get(pdf_url, headers=self.headers)

        destination = os.path.join(os.getcwd(), "pdfs")
        os.makedirs(destination, exist_ok=True)

        if "application/pdf" not in res.headers.get("Content-Type", ""):
            logger.info("Attempting download with headless browser - expect high latency")
            return self.selenium_client.download_pdf(pdf_url, doi)

        file_path = f"pdfs/{doi}.pdf"
        with open(file_path, "wb") as f:
            f.write(res.content)
        return file_path

