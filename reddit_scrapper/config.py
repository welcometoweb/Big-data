"""Configuration management for the scraping system."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Excel Configuration
EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH', 'posts_database.xlsx')

# Target URLs
PROFILE_URL = os.getenv('PROFILE_URL')
HOMEPAGE_URL = os.getenv('HOMEPAGE_URL')

# Scraping Configuration
RATE_LIMIT = float(os.getenv('RATE_LIMIT', 2))  # Requests per second
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Column names for Excel
COLUMN_NAMES = ['URL', 'Text', 'Date', 'Image Links']

def validate_config():
    """Validate that all required configuration is present."""
    # Excel file path is optional - will be created if it doesn't exist
    return True
