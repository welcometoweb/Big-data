"""Utility script to help discover CSS selectors for your target platform."""
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def inspect_page(url: str):
    """
    Open a page and help discover selectors.
    
    Args:
        url: The URL to inspect
    """
    print(f"\n🔍 Inspecting: {url}\n")
    
    # Set up Chrome with visible browser
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
   # service = Service(ChromeDriverManager().install())
   # driver = webdriver.Chrome(service=service, options=chrome_options)

   
    
    driver = webdriver.Chrome(options=chrome_options)

    
    try:
        driver.get(url)
        print("✓ Page loaded. Waiting 5 seconds for content to load...\n")
        time.sleep(5)
        
        # Try different common selectors
        selectors_to_test = {
            "Posts": [
                "article",
                "[data-testid='post']",
                "[data-testid='tweet']",
                ".post",
                ".post-item",
                "[role='article']",
                ".timeline-item"
            ],
            "Links": [
                "a[href*='/status/']",
                "a[href*='/post/']",
                "a[href*='/p/']",
                "time a",
                ".post-link"
            ],
            "Text": [
                "[data-testid='tweetText']",
                ".post-content",
                ".text-content",
                ".caption",
                "article p",
                "[role='article'] p"
            ],
            "Date/Time": [
                "time",
                "[datetime]",
                ".timestamp",
                ".post-date",
                ".timeago"
            ],
            "Images": [
                "img[src*='media']",
                ".post-image img",
                "article img",
                "[role='article'] img"
            ]
        }
        
        print("=" * 60)
        print("SELECTOR TEST RESULTS")
        print("=" * 60)
        
        for category, selectors in selectors_to_test.items():
            print(f"\n📌 {category}:")
            print("-" * 60)
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    count = len(elements)
                    
                    if count > 0:
                        print(f"  ✓ '{selector}' → Found {count} elements")
                        
                        # Show sample data for first element
                        if elements and category != "Posts":
                            sample = elements[0]
                            try:
                                if category == "Text":
                                    text = sample.text[:100]
                                    if text:
                                        print(f"    Sample: {text}...")
                                elif category == "Links":
                                    href = sample.get_attribute('href')
                                    if href:
                                        print(f"    Sample: {href}")
                                elif category == "Date/Time":
                                    dt = sample.get_attribute('datetime') or sample.text
                                    if dt:
                                        print(f"    Sample: {dt}")
                                elif category == "Images":
                                    src = sample.get_attribute('src')
                                    if src:
                                        print(f"    Sample: {src[:80]}...")
                            except:
                                pass
                    else:
                        print(f"  ✗ '{selector}' → Not found")
                except Exception as e:
                    print(f"  ⚠ '{selector}' → Error: {str(e)[:50]}")
        
        print("\n" + "=" * 60)
        print("\n💡 TIPS:")
        print("  1. Selectors with the most matches are usually the best")
        print("  2. Test post container selectors first")
        print("  3. Use Chrome DevTools (F12) for manual inspection")
        print("  4. Update backfill_scraper.py and daily_scraper.py with working selectors")
        print("\n  Browser will stay open for 30 seconds for manual inspection...")
        time.sleep(30)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        driver.quit()
        print("\n✓ Done!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python selector_inspector.py <URL>")
        print("Example: python selector_inspector.py https://twitter.com/username\n")
        sys.exit(1)
    
    url = sys.argv[1]
    inspect_page(url)
