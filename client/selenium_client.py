from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class SeleniumClient:

    @staticmethod
    def download_pdf_with_browser(pdf_url, output_path="temp.pdf"):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.get(pdf_url)

        # Let Cloudflare pass (sleep = hacky but effective)
        time.sleep(5)

        # If redirected to the real PDF, re-fetch with requests
        resolved_url = driver.current_url
        driver.quit()

        if resolved_url.endswith(".pdf"):
            import requests
            r = requests.get(resolved_url)
            with open(output_path, "wb") as f:
                f.write(r.content)
            return output_path
        else:
            print("No direct PDF found after browser load.")
            return None