"""Test script to verify Excel database and basic scraper functionality."""
import sys
from excel_client import ExcelClient
import config

def test_excel_connection():
    """Test connection to Excel database."""
    print("\n" + "=" * 60)
    print("TESTING EXCEL DATABASE")
    print("=" * 60)
    
    try:
        # Validate config
        print("\n✓ Checking configuration...")
        config.validate_config()
        print("  ✓ Configuration valid")
        
        # Initialize client
        print("\n✓ Initializing Excel client...")
        client = ExcelClient()
        print(f"  ✓ Excel file: {client.file_path}")
        
        # Get existing records
        print("\n✓ Fetching existing records...")
        existing_urls = client.get_all_urls()
        record_count = client.get_record_count()
        print(f"  ✓ Found {record_count} existing records")
        
        if existing_urls:
            print(f"\n  Sample URLs:")
            for url in existing_urls[:3]:
                print(f"    - {url}")
        
        # Test creating a record
        print("\n✓ Testing record creation...")
        test_post = {
            'url': 'https://example.com/test-post-12345',
            'text': 'This is a test post created by test_setup.py',
            'date': '2024-01-01T12:00:00Z',
            'image_links': 'https://example.com/image.jpg'
        }
        
        # Check if test record already exists
        if client.check_duplicate(test_post['url']):
            print("  ⚠ Test record already exists, skipping creation")
        else:
            print("  Creating test record...")
            record = client.create_record(test_post)
            print(f"  ✓ Test record created successfully")
            print("\n  ⚠ Note: You can delete this test record from the Excel file if needed")
        
        print("\n" + "=" * 60)
        print("✅ EXCEL DATABASE CONNECTION SUCCESSFUL!")
        print("=" * 60)
        print("\nYou're ready to run the scrapers!")
        print("  - Backfill: python backfill_scraper.py")
        print("  - Daily: python daily_scraper.py")
        print(f"\nData will be saved to: {client.file_path}")
        print("\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Check:")
        print("  1. You have write permissions in the current directory")
        print("  2. Excel file is not open in another program")
        print("  3. Dependencies are installed (pip install -r requirements.txt)")
        return False


def test_scraper_imports():
    """Test that scraper modules can be imported."""
    print("\n" + "=" * 60)
    print("TESTING SCRAPER IMPORTS")
    print("=" * 60 + "\n")
    
    try:
        print("✓ Testing backfill_scraper import...")
        import backfill_scraper
        print("  ✓ backfill_scraper imported successfully")
        
        print("\n✓ Testing daily_scraper import...")
        import daily_scraper
        print("  ✓ daily_scraper imported successfully")
        
        print("\n" + "=" * 60)
        print("✅ ALL IMPORTS SUCCESSFUL!")
        print("=" * 60 + "\n")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\n💡 Make sure you've installed dependencies:")
        print("  pip install -r requirements.txt\n")
        return False


def main():
    """Run all tests."""
    print("\n🧪 Running setup tests...\n")
    
    # Test imports first
    if not test_scraper_imports():
        sys.exit(1)
    
    # Test Excel connection
    if not test_excel_connection():
        sys.exit(1)
    
    print("✅ All tests passed! System is ready.\n")


if __name__ == "__main__":
    main()
