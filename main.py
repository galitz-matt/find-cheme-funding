from client.unpaywall_client import UnpaywallClient
import logging

from parsers.pdf_parser import PDFParser

logging.basicConfig(level=logging.INFO)

# scraper = UVAScraper(http_client)
# profiles = scraper.scrape_faculty_profiles()

# name = "Bryan Berger"
# affiliation = "University of Virginia"
#
# client = ScholarlyClient()
# author_profile = client.get_author_profile(name, affiliation)
# publications = client.get_publications(author_profile)

# pub_url = publications[4]["url"]

pub_url = 'https://www.pnas.org/doi/abs/10.1073/pnas.1523633113'
unpaywall = UnpaywallClient("galitz.matthew@gmail.com")
pdf_url = unpaywall.get_oa_pdf_url(pub_url)
print("OA PDF URL:", pdf_url)

pdf_parser = PDFParser()
print(pdf_parser.scrape_acknowledgments(pdf_url))


