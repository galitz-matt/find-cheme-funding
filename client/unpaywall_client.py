import requests
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class UnpaywallClient:
    known_libs = ["wiley.com", "pnas.org", "science.org"]

    def __init__(self, email):
        self.params = {"email": email}

    def get_oa_pdf_url(self, url):
        doi = self.parse_doi(url)
        if not doi:
            return None

        api_url = f"https://api.unpaywall.org/v2/{doi}"
        response = requests.get(api_url, params=self.params)

        if response.status_code != 200:
            logger.info(f"Unpaywall request failed: {response.status_code}")
            return None

        data = response.json()
        best_oa = data.get("best_oa_location")
        if best_oa and best_oa.get("url_for_pdf"):
            return best_oa["url_for_pdf"]
        else:
            print("No open access PDF available")
            return None

    def parse_doi(self, url):
        parsed = urlparse(url)
        is_known_lib = any(lib in parsed.netloc for lib in self.known_libs)
        if not is_known_lib or "/doi/abs" not in parsed.path:
            return None

        start = parsed.path.rfind("abs/") + 4
        return parsed.path[start:]

