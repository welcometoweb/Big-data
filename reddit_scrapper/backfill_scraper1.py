"""Backfill scraper for Reddit profile/subreddit page - one-time scraping of ~4600 posts."""

import time
import logging
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from excel_client import ExcelClient
import config

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ProfileScraper:
    """Scraper for Reddit profile or subreddit posts."""

    def __init__(self, headless: bool = True):
        """Initialize Selenium WebDriver (Chrome 145 compatible)."""

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={config.USER_AGENT}")

        # ✅ IMPORTANT: NO Service(), NO WebDriverManager
        self.driver = webdriver.Chrome(options=chrome_options)

        self.excel = ExcelClient()
        self.scraped_urls = set()

    # ------------------------------------------------------------------
    # Scrolling
    # ------------------------------------------------------------------
    def scroll_to_load_posts(self, target_count: int = 4600, max_scrolls: int = 500):
        logger.info(f"Scrolling to load posts (target={target_count})")

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scrolls = 0
        no_change_count = 0

        while scrolls < max_scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            posts = self.driver.find_elements(By.CSS_SELECTOR, "article")
            logger.info(f"Scroll {scrolls + 1}: loaded {len(posts)} posts")

            if len(posts) >= target_count:
                logger.info("Target post count reached")
                break

            if new_height == last_height:
                no_change_count += 1
                if no_change_count >= 3:
                    logger.info("No more content to load")
                    break
            else:
                no_change_count = 0

            last_height = new_height
            scrolls += 1
            time.sleep(1 / config.RATE_LIMIT)

    # ------------------------------------------------------------------
    # Post extraction
    # ------------------------------------------------------------------
    def extract_post_data(self, post_element) -> Dict:
        post_data = {
            "url": "",
            "text": "",
            "date": "",
            "image_links": ""
        }

        # URL
        try:
            link = post_element.find_element(By.CSS_SELECTOR, ".post-link")
            post_data["url"] = link.get_attribute("href")
        except:
            logger.debug("Post URL not found")

        # Title / text
        try:
            title = post_element.find_element(By.CSS_SELECTOR, "h3")
            post_data["text"] = title.text.strip()
        except:
            logger.debug("Post text not found")

        # Date
        try:
            time_el = post_element.find_element(By.CSS_SELECTOR, "time[datetime]")
            post_data["date"] = time_el.get_attribute("datetime")
        except:
            logger.debug("Post date not found")

        # Images
        try:
            images = post_element.find_elements(By.CSS_SELECTOR, "article img")
            urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]
            post_data["image_links"] = ", ".join(urls)
        except:
            logger.debug("Post images not found")

        return post_data

    # ------------------------------------------------------------------
    # Main scrape
    # ------------------------------------------------------------------
    def scrape_profile(self, profile_url: str = None) -> List[Dict]:
        url = profile_url or config.PROFILE_URL
        if not url:
            raise ValueError("Profile URL not provided")

        logger.info(f"Starting scrape: {url}")
        posts_data = []

        try:
            self.driver.get(url)

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
            )

            self.scroll_to_load_posts()

            post_elements = self.driver.find_elements(By.CSS_SELECTOR, "article")
            logger.info(f"Found {len(post_elements)} article elements")

            for idx, post in enumerate(post_elements, start=1):
                if idx % 100 == 0:
                    logger.info(f"Processing post {idx}/{len(post_elements)}")

                data = self.extract_post_data(post)
                if data["url"] and data["url"] not in self.scraped_urls:
                    posts_data.append(data)
                    self.scraped_urls.add(data["url"])

            logger.info(f"Extracted {len(posts_data)} unique posts")
            return posts_data

        finally:
            self.driver.quit()

    # ------------------------------------------------------------------
    # Excel upload
    # ------------------------------------------------------------------
    def run_backfill(self):
        logger.info("Starting backfill")

        posts = self.scrape_profile()
        if not posts:
            logger.warning("No posts scraped")
            return

        existing_urls = set(self.excel.get_all_urls())
        new_posts = [p for p in posts if p["url"] not in existing_urls]

        logger.info(
            f"Uploading {len(new_posts)} new posts "
            f"(skipping {len(posts) - len(new_posts)})"
        )

        if new_posts:
            self.excel.create_records_batch(new_posts)
            logger.info("Backfill completed successfully")
        else:
            logger.info("Nothing new to upload")


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------
def main():
    scraper = ProfileScraper(headless=True)
    scraper.run_backfill()


if __name__ == "__main__":
    main()