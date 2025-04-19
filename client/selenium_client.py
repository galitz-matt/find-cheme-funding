import os
import time
import glob
import shutil
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


logger = logging.getLogger(__name__)

class SeleniumClient:
    @staticmethod
    def download_pdf(self, pdf_url: str, doi: str) -> str | None:
        # Use the system Downloads folder
        downloads_dir = os.path.abspath("downloads")

        # Configure Chrome options
        options = Options()
        #options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("prefs", {
            "download.default_directory": downloads_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        try:
            logger.info(f"Navigating to {pdf_url}")
            driver.get(pdf_url)

            # Wait up to 15 seconds for download to appear
            downloaded_file = None
            for _ in range(30):  # 30 x 0.5s = 15s max
                time.sleep(0.5)
                pdfs = glob.glob(os.path.join(downloads_dir, "*.pdf"))
                if pdfs:
                    downloaded_file = max(pdfs, key=os.path.getctime)
                    break

            if not downloaded_file:
                logger.error("PDF not downloaded in time.")
                return None

            # Rename and move to ./pdfs using DOI-based name
            safe_name = doi.replace("/", "-") + ".pdf"
            final_path = os.path.join(downloads_dir, safe_name)
            shutil.move(downloaded_file, final_path)
            logger.info(f"PDF renamed to {final_path}")
            return final_path

        finally:
            driver.quit()

