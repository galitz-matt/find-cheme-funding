from client.selenium_client import SeleniumClient
from client.unpaywall_client import UnpaywallClient
from services.pdf_downloader import PDFDownloader
from parsers.pdf_parser import PDFParser
import logging

logging.basicConfig(level=logging.INFO)

# scraper = UVAScraper(http_client)
# profiles = scraper.scrape_faculty_profiles()

# name = "Bryan Berger"
# affiliation = "University of Virginia"
email = "galitz.matthew@gmail.com"
#
# client = ScholarlyClient()
# author_profile = client.get_author_profile(name, affiliation)
# publications = client.get_publications(author_profile)

# pub_url = publications[4]["url"]

pub_url = 'https://www.pnas.org/doi/abs/10.1073/pnas.1523633113'
pdf_downloader = PDFDownloader(UnpaywallClient(email), SeleniumClient())
pdf_downloader.download_pdf(pub_url)
