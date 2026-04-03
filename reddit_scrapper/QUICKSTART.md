# Quick Start Guide - Excel Edition

Get your scraping system running in minutes!

## Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install packages
pip install -r requirements.txt
```

## Step 2: Configure URLs

The `.env` file is already created. Just update the URLs:

```bash
# Open .env file
notepad .env  # Windows
# nano .env  # Mac/Linux
```

Update these lines:
```env
PROFILE_URL=https://yourplatform.com/profile/username
HOMEPAGE_URL=https://yourplatform.com/
```

**That's it! No API keys needed!**

## Step 3: Test Setup

```bash
python test_setup.py
```

You should see:
```
✅ EXCEL DATABASE CONNECTION SUCCESSFUL!

Data will be saved to: posts_database.xlsx
```

This creates the Excel file automatically.

## Step 4: Find CSS Selectors

This is the most important step!

```bash
python selector_inspector.py YOUR_PROFILE_URL

# Example:
# python selector_inspector.py https://twitter.com/username
```

A browser will open and show you which selectors work. Look for:
- ✓ Marks (selectors that found elements)
- The ones with the most matches are usually best

Example output:
```
📌 Posts:
  ✓ 'article' → Found 20 elements
  ✗ '.post-item' → Not found

📌 Text:
  ✓ '[data-testid="tweetText"]' → Found 20 elements
    Sample: This is a post...
```

**Write down the selectors that work!**

## Step 5: Update Selectors

Edit both `backfill_scraper.py` and `daily_scraper.py`:

### Find the post container selector

Search for this line (around line 115 in backfill, line 85 in daily):
```python
post_elements = self.driver.find_elements(By.CSS_SELECTOR, "article, [data-testid='post'], .post-item")
```

Replace with your working selector:
```python
post_elements = self.driver.find_elements(By.CSS_SELECTOR, "article")  # Use what worked
```

### Find the extract_post_data() method

Update these selectors (around line 49 in both files):

**URL selector:**
```python
# Before:
link_element = post_element.find_element(By.CSS_SELECTOR, "a[href*='/status/'], a[href*='/post/'], time a")

# After (use your working selector):
link_element = post_element.find_element(By.CSS_SELECTOR, "time a")
```

**Text selector:**
```python
# Before:
text_element = post_element.find_element(By.CSS_SELECTOR, "[data-testid='tweetText'], .post-content, .text-content, p")

# After (use your working selector):
text_element = post_element.find_element(By.CSS_SELECTOR, "[data-testid='tweetText']")
```

**Date selector:**
```python
# Before:
date_element = post_element.find_element(By.CSS_SELECTOR, "time, .timestamp, .post-date")

# After (use your working selector):
date_element = post_element.find_element(By.CSS_SELECTOR, "time")
```

**Image selector:**
```python
# Before:
image_elements = post_element.find_elements(By.CSS_SELECTOR, "img[src*='media'], .post-image img, img[alt]")

# After (use your working selector):
image_elements = post_element.find_elements(By.CSS_SELECTOR, "img[src*='media']")
```

## Step 6: Test Daily Scraper

Start with the daily scraper (only 3 posts):

```bash
python daily_scraper.py
```

Expected output:
```
Starting homepage scrape: https://...
Found 20 post elements
Extracted 3 posts
Uploading 3 new posts to Excel...
Daily scrape complete! Added 3 new posts.
```

### Check Your Data

Open `posts_database.xlsx` in Excel. You should see 3 rows with:
- URL column filled
- Text column filled
- Date column filled
- Image Links column (may be empty if no images)

**If data looks good, proceed! If not, check your selectors.**

## Step 7: Run Backfill (Optional)

Once the daily scraper works, run the full backfill:

```bash
python backfill_scraper.py
```

This will take 30-60 minutes to scrape ~4600 posts.

Output:
```
Starting backfill process...
Scroll 1: Loaded 20 posts
Scroll 2: Loaded 40 posts
...
Successfully extracted 4600 unique posts
Uploading 4600 posts to Excel...
Created batch of 10 records (10/4600 total)
...
Backfill complete!
```

## Step 8: Automate with GitHub Actions (Optional)

### Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main
```

### Add Secrets (Optional)

Go to: Settings → Secrets → Actions → New repository secret

Add:
- `PROFILE_URL` (optional, can use .env)
- `HOMEPAGE_URL` (optional, can use .env)

### Enable Workflow

1. Go to Actions tab
2. Enable workflows
3. Runs daily at 9 AM UTC automatically
4. Excel file commits back to repo

## Viewing Results

### Locally
Just open `posts_database.xlsx` in:
- Microsoft Excel
- Google Sheets (upload file)
- LibreOffice Calc
- Any spreadsheet app

### On GitHub
After automated runs:
1. Pull latest changes: `git pull`
2. Open the Excel file

Or download from Actions artifacts:
1. Actions tab → Click run
2. Download "posts-database" artifact

## Common Issues

### "No element found"
- Go back to Step 4 and find better selectors
- The generic selectors don't match your site

### "Permission denied" on Excel file
- Close the Excel file if it's open

### No posts scraped
- Check PROFILE_URL and HOMEPAGE_URL are correct
- Try running with `headless=False` to see the browser

### Duplicate posts only
- This is normal if you run it twice
- System prevents duplicates automatically

## What's Next?

### Schedule Changes
Edit `.github/workflows/daily_scraper.yml` to change timing:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

### Export to CSV
```python
from excel_client import ExcelClient
client = ExcelClient()
client.export_to_csv('my_posts.csv')
```

### Analyze Data
Open Excel and use:
- Filters
- Pivot tables
- Charts
- Formulas

## Success Checklist

- [  ] Dependencies installed
- [  ] .env configured with URLs
- [  ] test_setup.py runs successfully
- [  ] selector_inspector.py shows working selectors
- [  ] Selectors updated in both scraper files
- [  ] daily_scraper.py produces 3 good records
- [  ] Excel file opens and shows correct data
- [  ] (Optional) backfill_scraper.py runs successfully
- [  ] (Optional) GitHub Actions workflow enabled

## Need Help?

1. Check [README.md](README.md) for detailed docs
2. Review scraper logs for errors
3. Test selectors in browser console
4. Start with small tests (daily scraper first)

---

**You did it!** 🎉 Your scraping system is ready to use.
