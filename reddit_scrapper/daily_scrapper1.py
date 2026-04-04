"""Daily scraper for Reddit homepage or subreddit - scrapes ~3 new posts per day."""

import time
import logging
from typing import Dict, List

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


class DailyScraper:
    """Scraper for daily Reddit posts."""

    def __init__(self, headless: bool = True):
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless=new")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # 🔥 ADD THESE (important)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        # ✅ IMPORTANT: Selenium auto-driver (NO Service / NO WebDriverManager)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.excel = ExcelClient()

    # -------------------------------------------------------------
    # Extract single post
    # -------------------------------------------------------------
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
            pass

        # Title
        try:
            title = post_element.find_element(By.CSS_SELECTOR, "h3")
            post_data["text"] = title.text.strip()
        except:
            pass

        # Timestamp
        try:
            time_el = post_element.find_element(By.CSS_SELECTOR, "time[datetime]")
            post_data["date"] = time_el.get_attribute("datetime")
        except:
            pass

        # Images
        try:
            images = post_element.find_elements(By.CSS_SELECTOR, "article img")
            urls = [
                img.get_attribute("src")
                for img in images if img.get_attribute("src")
            ]
            post_data["image_links"] = ", ".join(urls)
        except:
            pass

        return post_data

    # -------------------------------------------------------------
    # Scrape homepage or subreddit
    # -------------------------------------------------------------
    def scrape_homepage(
        self,
        homepage_url: str = None,
        max_posts: int = 5
    ) -> List[Dict]:

        url = homepage_url or config.HOMEPAGE_URL
        if not url:
            raise ValueError("Homepage URL not provided")

        logger.info(f"Starting homepage scrape: {url}")
        # Step 1: Open reddit base first (needed for cookies)
        self.driver.get("https://www.reddit.com")
        
        # Step 2: Set cookie to force old reddit
        self.driver.add_cookie({
            'name': 'over18',
            'value': '1',
            'domain': '.reddit.com'
        })
        
        # Step 3: Now open target
        self.driver.get(url)
        
        # 🔍 DEBUG (VERY IMPORTANT)
        print("FINAL URL:", self.driver.current_url)

        # Wait for Reddit posts
        time.sleep(5)
        print(self.driver.page_source[:2000])
        # WebDriverWait(self.driver, 15).until(
            #EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        #)

        # Small scroll to trigger lazy loading
        self.driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(2)

        post_elements = self.driver.find_elements(By.CSS_SELECTOR, "article")
        logger.info(f"Found {len(post_elements)} article elements")

        posts = []
        seen_urls = set()

        for post in post_elements:
            if len(posts) >= max_posts:
                break

            data = self.extract_post_data(post)
            if data["url"] and data["url"] not in seen_urls:
                posts.append(data)
                seen_urls.add(data["url"])

        self.driver.quit()
        logger.info(f"Extracted {len(posts)} posts from homepage")
        return posts

    # -------------------------------------------------------------
    # Daily pipeline
    # -------------------------------------------------------------
    def run_daily_scrape(self, target_posts: int = 50):
        logger.info("Fetching existing URLs from Excel")

        existing_urls = set(self.excel.get_all_urls())
        logger.info(f"Found {len(existing_urls)} existing records")

        # Fetch a few extra to filter duplicates
        posts = self.scrape_homepage(max_posts=target_posts + 5)

        new_posts = [
            post for post in posts if post["url"] not in existing_urls
        ][:target_posts]

        if new_posts:
            logger.info(f"Uploading {len(new_posts)} new posts")
            self.excel.create_records_batch(new_posts)

            for post in new_posts:
                logger.info(f"  + {post['url']}")
        else:
            logger.info("No new posts found today")


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------
def main():
    scraper = DailyScraper(headless=True)
    scraper.run_daily_scrape(target_posts=3)


if __name__ == "__main__":
    main()
