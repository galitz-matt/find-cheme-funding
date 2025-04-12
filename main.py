from client.http_client import HttpClient
from scrapers.uva_scraper import UVAScraper
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = UVAScraper(HttpClient())
    print(scraper.scrape_faculty_profiles())