from client.http_client import HttpClient
from scrapers.uva_scraper import UVAScraper
import logging
from client.scholarly_client import ScholarlyClient

logging.basicConfig(level=logging.INFO)

# scraper = UVAScraper(HttpClient())
# profiles = scraper.scrape_faculty_profiles()

name = "Bryan Berger"
affiliation = "University of Virginia"

client = ScholarlyClient()
author_profile = client.get_author_profile(name, affiliation)
publications = client.get_publications(author_profile)
from pprint import pprint

pprint(publications)