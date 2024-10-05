import time
from .fetcher import fetch_rss_feed, fetch_document_link
from .parser import parse_rss_feed, is_ipo_filing
from .utils import initialize_csv, fetch_existing_urls, append_to_csv
from .constants import get_rss_feed_url, CSV_FILE_PATH, POLLING_INTERVAL

def sec_ipo_detector():
    """Main function to detect IPO filings."""
    initialize_csv(CSV_FILE_PATH)
    
    # Fetch existing URLs once and store them in memory
    existing_urls = set(fetch_existing_urls(CSV_FILE_PATH))
    
    while True:
        content = fetch_rss_feed(get_rss_feed_url())
        if content:
            entries = parse_rss_feed(content)
            new_entries = []

            for entry in entries:
                if entry['url'] not in existing_urls:  
                    document_link = fetch_document_link(entry['url'])
                    if document_link:
                        is_ipo = is_ipo_filing(document_link)
                        entry['documentLink'] = document_link
                        entry['isIPO'] = is_ipo
                        new_entries.append(entry)
                        existing_urls.add(entry['url'])  

            if new_entries:
                append_to_csv(CSV_FILE_PATH, new_entries)
                print(f"Added {len(new_entries)} new IPO entries.")
            else:
                print("No new IPO entries found.")

        time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    sec_ipo_detector()
