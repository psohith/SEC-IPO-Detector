import time
from .fetcher import fetch_rss_feed, fetch_document_link
from .parser import parse_rss_feed, is_ipo_filing
from .utils import initialize_csv, fetch_existing_urls, append_to_csv, get_latest_updated_time
from .constants import get_rss_feed_url, CSV_FILE_PATH, POLLING_INTERVAL
from datetime import datetime

def sec_ipo_detector():
    """Main function to detect IPO filings."""
    initialize_csv(CSV_FILE_PATH)
    
    # Get the latest updated time from the CSV file
    latest_updated_time = get_latest_updated_time(CSV_FILE_PATH)
    
    while True:
        content = fetch_rss_feed(get_rss_feed_url())
        if content:
            entries = parse_rss_feed(content, latest_updated_time)
            if entries:
                for entry in entries:
                    document_link = fetch_document_link(entry['url'])
                    if document_link:
                        is_ipo = is_ipo_filing(document_link)
                        entry['documentLink'] = document_link
                        entry['isIPO'] = is_ipo

                append_to_csv(CSV_FILE_PATH, entries)
                print(f"Added {len(entries)} new IPO entries.")
                latest_updated_time = datetime.strptime(entries[0]['updated'],  '%Y-%m-%dT%H:%M:%S%z')
            else:
                print("No new IPO entries found.")

        time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    sec_ipo_detector()
