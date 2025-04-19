from client.selenium_client import SeleniumClient
from client.unpaywall_client import UnpaywallClient
from client.scholarly_client import ScholarlyClient
from services.pdf_downloader import PDFDownloader
from parsers.pdf_parser import PDFParser
from scrapers.uva_scraper import UVAScraper
import logging

logging.basicConfig(level=logging.INFO)

# scraper = UVAScraper()
# profiles = scraper.scrape_faculty_profiles()

name = "Bryan Berger"
affiliation = "University of Virginia"
email = "galitz.matthew@gmail.com"

client = ScholarlyClient()
author_profile = client.get_author_profile(name, affiliation)
publications = client.get_publications(author_profile)

pub_url = publications[4]["url"]
print(pub_url)

pdf_downloader = PDFDownloader(UnpaywallClient(email), SeleniumClient())
file_path = pdf_downloader.download_pdf(pub_url)

pdf_parser = PDFParser()
print(pdf_parser.scrape_acknowledgments(file_path))