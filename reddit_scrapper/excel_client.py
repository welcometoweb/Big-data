"""Excel client for managing scraped posts."""
import os
import pandas as pd
from typing import List, Dict
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExcelClient:
    """Client for interacting with Excel database."""
    
    def __init__(self, file_path: str = None):
        """
        Initialize the Excel client.
        
        Args:
            file_path: Path to the Excel file (defaults to config)
        """
        self.file_path = file_path or config.EXCEL_FILE_PATH
        self.columns = config.COLUMN_NAMES
        
        # Create new Excel file if it doesn't exist
        if not os.path.exists(self.file_path):
            self._create_new_file()
            logger.info(f"Created new Excel database: {self.file_path}")
        else:
            logger.info(f"Using existing Excel database: {self.file_path}")
    
    def _create_new_file(self):
        """Create a new Excel file with headers."""
        df = pd.DataFrame(columns=self.columns)
        df.to_excel(self.file_path, index=False, engine='openpyxl')
    
    def _read_data(self) -> pd.DataFrame:
        """Read data from Excel file."""
        try:
            return pd.read_excel(self.file_path, engine='openpyxl')
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            # Return empty DataFrame with correct columns if file is corrupted
            return pd.DataFrame(columns=self.columns)
    
    def _write_data(self, df: pd.DataFrame):
        """Write data to Excel file."""
        try:
            df.to_excel(self.file_path, index=False, engine='openpyxl')
        except Exception as e:
            logger.error(f"Error writing to Excel file: {e}")
            raise
    
    def create_record(self, post_data: Dict) -> Dict:
        """
        Create a single record in Excel.
        
        Args:
            post_data: Dictionary containing post fields (url, text, date, image_links)
        
        Returns:
            Created record data
        """
        df = self._read_data()
        
        new_row = {
            'URL': post_data.get('url', ''),
            'Text': post_data.get('text', ''),
            'Date': post_data.get('date', ''),
            'Image Links': post_data.get('image_links', '')
        }
        
        try:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            self._write_data(df)
            logger.info(f"Created record: {new_row['URL']}")
            return new_row
        except Exception as e:
            logger.error(f"Error creating record: {e}")
            raise
    
    def create_records_batch(self, posts: List[Dict]) -> List[Dict]:
        """
        Create multiple records in Excel using batch operation.
        
        Args:
            posts: List of dictionaries containing post data
        
        Returns:
            List of created records
        """
        if not posts:
            logger.warning("No posts to create")
            return []
        
        df = self._read_data()
        
        new_rows = [
            {
                'URL': post.get('url', ''),
                'Text': post.get('text', ''),
                'Date': post.get('date', ''),
                'Image Links': post.get('image_links', '')
            }
            for post in posts
        ]
        
        try:
            new_df = pd.DataFrame(new_rows)
            df = pd.concat([df, new_df], ignore_index=True)
            self._write_data(df)
            logger.info(f"Created batch of {len(new_rows)} records")
            return new_rows
        except Exception as e:
            logger.error(f"Error creating batch: {e}")
            raise
    
    def check_duplicate(self, post_url: str) -> bool:
        """
        Check if a post URL already exists in Excel.
        
        Args:
            post_url: The URL to check
        
        Returns:
            True if duplicate exists, False otherwise
        """
        try:
            df = self._read_data()
            if df.empty:
                return False
            return post_url in df['URL'].values
        except Exception as e:
            logger.error(f"Error checking duplicate: {e}")
            return False
    
    def get_all_urls(self) -> List[str]:
        """
        Retrieve all existing URLs from Excel.
        
        Returns:
            List of URLs
        """
        try:
            df = self._read_data()
            if df.empty:
                return []
            return df['URL'].tolist()
        except Exception as e:
            logger.error(f"Error retrieving URLs: {e}")
            return []
    
    def get_record_count(self) -> int:
        """
        Get the total number of records in the database.
        
        Returns:
            Number of records
        """
        try:
            df = self._read_data()
            return len(df)
        except Exception as e:
            logger.error(f"Error getting record count: {e}")
            return 0
    
    def export_to_csv(self, csv_path: str = 'posts_export.csv'):
        """
        Export data to CSV format.
        
        Args:
            csv_path: Path for the CSV export
        """
        try:
            df = self._read_data()
            df.to_csv(csv_path, index=False, encoding='utf-8')
            logger.info(f"Exported {len(df)} records to {csv_path}")
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise
