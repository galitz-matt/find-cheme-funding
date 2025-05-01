import requests
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class UnpaywallClient:
    known_libs = ["www.wiley.com",
                  "onlinelibrary.wiley.com",
                  "www.pnas.org",
                  "www.science.org",
                  "www.cell.com",
                  "journals.asm.org"]

    def __init__(self, email):
        self.params = {"email": email}

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get_oa_pdf_url(self, url):
        doi = self.parse_doi(url)
        if not doi:
            return None

        api_url = f"https://api.unpaywall.org/v2/{doi}"
        logger.info(f"Retrieving open access URL at endpoint {api_url}")
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
        logger.info(f"Parsing DOI from URL: {url}")
        parsed = urlparse(url)

        if parsed.netloc == "www.cell.com":
            logger.info("Encountered parser edge case, extracting DOI from metadata")
            return self.parse_doi_from_cell_lib(url)

        is_known_lib = any(lib == parsed.netloc for lib in self.known_libs)
        if not is_known_lib and "/doi/abs" not in parsed.path:
            logger.error(f"No DOI was found in URL: {url}")
            return None


        start = parsed.path.rfind("abs/") + 4
        return parsed.path[start:]

    def parse_doi_from_cell_lib(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(3)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        doi_meta = soup.find("meta", {"name": "citation_doi"})
        return doi_meta["content"] if doi_meta else None