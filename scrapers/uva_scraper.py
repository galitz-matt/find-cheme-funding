from scrapers.cheme_scraper import ChemEScraper
from client.http_client import HttpClient
from lxml import html
import logging

logger = logging.getLogger(__name__)

class UVAScraper(ChemEScraper):
    SCHOOL_BASE_URL = "https://engineering.virginia.edu/"
    PEOPLE_URL = "https://engineering.virginia.edu/department/chemical-engineering/people?keyword=&position=2&impact_area=All&research_area=All"
    NO_RESULTS_XPATH = '//div[contains(@class, "results_message_inner typography") and contains(text(), "There are no results matching these criteria.")]'
    CONTACT_BLOCK_NAME_XPATH = '//a[contains(@class, "contact_block_name_link")]/@href'
    EMAIL_XPATH = "//a[contains(@class, 'people_meta_detail_info_link') and starts-with(@href, 'mailto:')]/@href"
    EDUCATION_XPATH = "//h2[text()='Education']"
    ABOUT_AND_EDUCATION_XPATH = "//h2[text()='About']/following-sibling::*[following-sibling::h2[text()='Education']]"
    ABOUT_XPATH = "//h2[text()='About']/following-sibling::*"
    RESEARCH_INTERESTS_XPATH = "//h2[normalize-space(text())='Research Interests']/following-sibling::div[@class='directory_grid_items']//div[@class='directory_grid_item']"

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def scrape_faculty_profiles(self):
        logger.info("Scraping UVA ChemE faculty profiles.")
        profile_endpoints = self.get_profile_endpoints()

        faculty_data = []
        for endpoint in profile_endpoints:
            profile_url = f"{self.SCHOOL_BASE_URL}{endpoint}"
            logger.info(f"Processing {profile_url}")
            name = self.get_name_from_profile(profile_url)
            about = self.get_about_from_profile(profile_url)

            faculty_data.append({
                "name": name,
                "school": "University of Virginia",
                "about": about,
                "url": profile_url
            })

        return faculty_data

    def get_profile_endpoints(self):
        response = self.http_client.get(self.PEOPLE_URL)
        tree = html.fromstring(response.content)
        return tree.xpath(self.CONTACT_BLOCK_NAME_XPATH)

    def get_name_from_profile(self, profile_url):
        endpoint = profile_url.split("/")[-1]
        return " ".join(name.capitalize() for name in endpoint.split("-"))

    def get_about_from_profile(self, profile_url):
        response = self.http_client.get(profile_url)
        tree = html.fromstring(response.content)
        raw_education = tree.xpath(self.EDUCATION_XPATH)
        if raw_education:
            raw_about = tree.xpath(self.ABOUT_AND_EDUCATION_XPATH)
        else:
            raw_about = tree.xpath(self.ABOUT_XPATH)
        about_content = [element.text_content().strip() for element in raw_about if element.text_content().strip()]
        if about_content:
            return "\n".join(about_content)
        else:
            return ""