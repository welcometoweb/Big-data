# Social Media Scraping System

A two-part web scraping system for collecting posts from public social media profiles and saving them to Excel.

## Features

- **Part 1: One-Time Backfill** - Scrape ~4600 historical posts from a public profile page
- **Part 2: Daily Automation** - Automatically scrape ~3 new posts daily from the homepage
- **Excel Database** - All data saved to a local Excel file (no API keys needed!)
- **Duplicate Detection** - Avoid re-scraping existing posts
- **GitHub Actions** - Automated daily scheduling with automatic database commits

## Data Fields

Each post captures 4 columns in Excel:
- **URL** - Direct link to the post
- **Text** - Post content/caption
- **Date** - Publication date/timestamp
- **Image Links** - URLs of all images in the post

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure URLs in .env file
PROFILE_URL=https://yoursite.com/profile
HOMEPAGE_URL=https://yoursite.com/

# 3. Test setup
python test_setup.py

# 4. Find CSS selectors for your target site
python selector_inspector.py YOUR_PROFILE_URL

# 5. Update selectors in scraper files

# 6. Run scrapers
python daily_scraper.py       # Test with 3 posts first
python backfill_scraper.py    # Then run full backfill
```

## Why Excel?

✅ **No API keys needed** - Works completely offline  
✅ **No rate limits** - No external API calls  
✅ **Free** - No subscription costs  
✅ **Easy to view** - Open directly in Excel or Google Sheets  
✅ **Easy to edit** - Manual corrections if needed  
✅ **Portable** - Take your data anywhere  
✅ **Version control** - Commit to Git for history tracking  

## Installation

### Windows

```powershell
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Mac/Linux

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit [.env](.env) file:

```env
# Excel file path (will be created automatically)
EXCEL_FILE_PATH=posts_database.xlsx

# Target URLs - UPDATE THESE!
PROFILE_URL=https://example.com/profile/username
HOMEPAGE_URL=https://example.com/

# Rate limiting (requests per second)
RATE_LIMIT=2
```

## Customizing for Your Platform

The scrapers use generic CSS selectors. **You MUST customize them** for your target platform.

### Step 1: Find Selectors

```bash
python selector_inspector.py https://yoursite.com/profile
```

This tool will test common selectors and show you which ones work.

### Step 2: Update Scraper Files

Edit both [backfill_scraper.py](backfill_scraper.py) and [daily_scraper.py](daily_scraper.py):

```python
# In extract_post_data() method, update these selectors:

# Post URL
link_element = post_element.find_element(By.CSS_SELECTOR, "YOUR_SELECTOR_HERE")

# Post text  
text_element = post_element.find_element(By.CSS_SELECTOR, "YOUR_SELECTOR_HERE")

# Date
date_element = post_element.find_element(By.CSS_SELECTOR, "YOUR_SELECTOR_HERE")

# Images
image_elements = post_element.find_elements(By.CSS_SELECTOR, "YOUR_SELECTOR_HERE")
```

## Usage

### Test Setup

```bash
python test_setup.py
```

Creates Excel file and verifies everything works.

### Daily Scraper (3 posts)

```bash
python daily_scraper.py
```

Scrapes 3 recent posts from homepage and saves to Excel.

### Backfill Scraper (~4600 posts)

```bash
python backfill_scraper.py
```

Scrapes all posts from a profile page. May take 30-60 minutes.

## Excel Database

The Excel file (`posts_database.xlsx`) features:
- **Auto-created** on first run
- **Duplicate detection** via URL checking
- **Easy viewing** in Excel, Google Sheets, or LibreOffice
- **Export capability** to CSV if needed
- **No external dependencies** - works offline

### Exporting to CSV

```python
from excel_client import ExcelClient

client = ExcelClient()
client.export_to_csv('posts_export.csv')
```

## GitHub Actions Automation

### Setup

1. Push code to GitHub
2. Add secrets (Settings → Secrets): `PROFILE_URL`, `HOMEPAGE_URL` (optional - can use .env)
3. Workflow runs daily at 9 AM UTC
4. Excel file automatically commits back to repo

### Modify Schedule

Edit [.github/workflows/daily_scraper.yml](.github/workflows/daily_scraper.yml):

```yaml
schedule:
  - cron: '0 9 * * *'    # 9 AM UTC daily
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 0 * * 1'    # Every Monday
```

## Project Structure

```
Web_scraping/
├── backfill_scraper.py      # Profile scraper (~4600 posts)
├── daily_scraper.py         # Homepage scraper (~3 posts)
├── excel_client.py          # Excel database manager
├── config.py                # Configuration
├── test_setup.py            # Setup verification
├── selector_inspector.py    # CSS selector discovery
├── requirements.txt         # Dependencies
├── .env                     # Local configuration
├── .env.example             # Configuration template
├── posts_database.xlsx      # Excel database (auto-created)
└── .github/workflows/
    └── daily_scraper.yml    # Automation workflow
```

## Troubleshooting

**"No element found" errors**
- Run `selector_inspector.py` to find correct selectors
- Website structure may have changed
- Try `headless=False` to see browser

**"Permission denied" on Excel file**
- Close Excel if file is open
- Check write permissions

**No new posts found**
- Verify website has new content
- Check if posts are duplicates
- Review scraper logs

**Excel file too large**
- Excel supports 1M+ rows
- Export to CSV for analysis
- Archive old data to separate file

## Best Practices

1. **Test locally** before automation
2. **Respect rate limits** (default: 2 req/sec)
3. **Update selectors** when sites change
4. **Backup Excel file** regularly
5. **Monitor GitHub Actions** for failures

## Legal & Ethical

⚠️ **Important:**
- Only scrape **public** data
- Respect robots.txt and Terms of Service
- Don't overload servers
- Be aware of privacy regulations  
- For educational/personal use only

## License

Provided as-is for educational purposes.

---

**Need help?** Check [QUICKSTART.md](QUICKSTART.md) for detailed setup guide or open an issue.
