import requests
import logging
from typing import Any, List
from requests.exceptions import RequestException, Timeout, HTTPError
from lxml import html

logger = logging.getLogger(__name__)

class HttpClient:
    def __init__(self, timeout: int = 10, retries: int = 3):
        self.timeout = timeout
        self.retries = retries

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        for attempt in range(self.retries):
            try:
                logger.info(f"Making {method} request to {url} (attempt {attempt + 1}/{self.retries})")
                response = requests.request(method, url, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response
            except (Timeout, HTTPError) as e:
                logger.warning(f"Attempt {attempt + 1} of {self.retries} failed for {url}: {e}")
                if attempt == self.retries - 1:
                    raise
            except RequestException as e:
                logger.error(f"Request error for {url}: {e}")
                raise

class MITScraper:
    BASE_URL = "https://cheme.mit.edu/people/faculty/"
    FACULTY_XPATH = '//a[starts-with(@href, "https://cheme.mit.edu/profile/") and @title]'

    @staticmethod
    def get_names(client: HttpClient) -> List[str]:
        try:
            response = client.request("GET", MITScraper.BASE_URL)
            tree = html.fromstring(response.content)
            faculty_links = tree.xpath(MITScraper.FACULTY_XPATH)
            faculty_names = sorted({link.get('title') for link in faculty_links})
            return faculty_names
        except Exception as e:
            logger.error(f"Failed to fetch or parse faculty data: {e}")
            return []
        
class PurdueScraper:
    BASE_URL = "https://engineering.purdue.edu/ChE/people/ptFaculty"
    FACULTY_XPATH = '//a[contains(@href, "ptProfile?resource_id=")]'

    @staticmethod
    def get_names(client) -> List[str]:
        try:
            response = client.request("GET", PurdueScraper.BASE_URL)
            tree = html.fromstring(response.content)

            faculty_links = tree.xpath(PurdueScraper.FACULTY_XPATH)

            faculty_names = sorted({link.text_content().strip() for link in faculty_links})
            return faculty_names

        except Exception as e:
            logger.error(f"Failed to fetch or parse faculty data: {e}")
            return []
        
class StanfordScraper:
    BASE_URL = "https://cheme.stanford.edu/people/faculty"
    FACULTY_XPATH = '//a[starts-with(@href, "/people/") and @hreflang="en"]'

    @staticmethod
    def get_names(client) -> List[str]:
        try:
            response = client.request("GET", StanfordScraper.BASE_URL)
            tree = html.fromstring(response.content)

            faculty_links = tree.xpath(StanfordScraper.FACULTY_XPATH)

            faculty_names = sorted({link.text_content().strip() for link in faculty_links})
            return faculty_names

        except Exception as e:
            logger.error(f"Failed to fetch or parse faculty data: {e}")
            return []
        
class GeorgiaTechScraper:
    BASE_URL = "https://chbe.gatech.edu/directory1"
    FACULTY_XPATH = '//a[starts-with(@href, "/directory/person/") and contains(@class, "dir_link")]//div[@class="field__item"]'

    @staticmethod
    def get_names(client) -> List[str]:
        try:
            response = client.request("GET", GeorgiaTechScraper.BASE_URL)
            tree = html.fromstring(response.content)

            name_elements = tree.xpath(GeorgiaTechScraper.FACULTY_XPATH)
            faculty_names = sorted({el.text_content().strip() for el in name_elements if el.text_content().strip()})
            return faculty_names

        except Exception as e:
            logger.error(f"Failed to fetch or parse faculty data: {e}")
            return []
        
class PrincetonScraper:
    BASE_URL = "https://cbe.princeton.edu/people/faculty"
    FACULTY_XPATH = '//a[starts-with(@href, "/people/") and @hreflang="und"]'

    @staticmethod
    def get_names(client) -> List[str]:
        try:
            response = client.request("GET", PrincetonScraper.BASE_URL)
            tree = html.fromstring(response.content)

            faculty_links = tree.xpath(PrincetonScraper.FACULTY_XPATH)
            faculty_names = sorted({link.text_content().strip() for link in faculty_links if link.text_content().strip()})
            return faculty_names

        except Exception as e:
            logger.error(f"Failed to fetch or parse faculty data: {e}")
            return []

# Call all staticmethods of scrapers
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     client = HttpClient()

#     scrapers = [
#         MITScraper,
#         PurdueScraper,
#         StanfordScraper,
#         GeorgiaTechScraper,
#         PrincetonScraper
#     ]

#     for scraper in scrapers:
#         faculty_names = scraper.get_names(client)
#         print(f"{scraper.__name__}: {faculty_names}")
#         print("-------------------------------- \n")