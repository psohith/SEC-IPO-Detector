import requests
import xml.etree.ElementTree as ET
import time
import csv
import os
from bs4 import BeautifulSoup

# Constants for headers
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'priority': 'u=0, i',     
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
}

# Constants for URLs
SEC_BASE_URL = "https://www.sec.gov"
CSV_FILE = 'sec_filings.csv'

def initialize_csv(file_path):
    """Initialize the CSV file with headers if it does not exist."""
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'URL', 'Summary', 'Updated', 'Category', 'Document Link', 'Is IPO'])

def fetch_existing_entries(file_path):
    """Fetch the existing entries from the CSV to avoid duplicates."""
    existing_urls = set()
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_urls.add(row['URL'])
    return existing_urls

def append_to_csv(file_path, entries):
    """Append new entries to the CSV file."""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for entry in entries:
            writer.writerow([
                entry['title'], 
                entry['url'], 
                entry['summary'], 
                entry['updated'], 
                entry['category'], 
                entry['documentLink'], 
                entry['isIPO']
            ])

def fetch_xml(url):
    """Fetch XML data from a given URL."""
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        time.sleep(1)  # Delay to avoid being blocked
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {url}: {e}")
        return None

def parse_xml(content):
    """Parse the XML content and extract entries."""
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = []

    root = ET.fromstring(content)
    for entry in root.findall('atom:entry', ns):
        entry_data = {
            'title': entry.find('atom:title', ns).text,
            'url': entry.find('atom:link', ns).attrib['href'],
            'summary': entry.find('atom:summary', ns).text.strip(),
            'updated': entry.find('atom:updated', ns).text,
            'category': entry.find('atom:category', ns).attrib.get('term'),
        }
        entries.append(entry_data)
    
    return entries

def get_document_link(session, url):
    """Retrieve the document link from the entry URL."""
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        time.sleep(1)  # Delay to avoid overwhelming the server

        soup = BeautifulSoup(response.content, 'html.parser')
        cols  = soup.find_all('tr')[1].find_all('td') 
        document_link = cols[2].find('a')['href']
        
        return f"{SEC_BASE_URL}{document_link}" if document_link else "404"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SEC form from {url}: {e}")
        return None

def detect_ipo(filing_url):
    """Check if the filing document is related to an IPO."""
    try:
        response = requests.get(filing_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()

        ipo_keywords = ["Initial Public Offering", "IPO", "going public", "underwriter", "use of proceeds"]
        return any(keyword in text for keyword in ipo_keywords)
    except requests.exceptions.RequestException as e:
        print(f"Error checking IPO status from {filing_url}: {e}")
        return False

def sec_feed_parser(url, existing_urls):
    """Parse the SEC feed and retrieve document links along with IPO detection."""
    session = requests.Session()
    
    content = fetch_xml(url)
    if content is None:
        return []

    entries = parse_xml(content)
    new_entries = []

    for entry in entries:
        if entry['url'] not in existing_urls:
            document_link = get_document_link(session, entry['url'])
            entry["documentLink"] = document_link

            # Check if the document is an IPO filing
            is_ipo = detect_ipo(document_link) if document_link != "404" else False
            entry["isIPO"] = is_ipo
            new_entries.append(entry)
            print(entry)

    return new_entries

def main():
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=S-1&company=&dateb=&owner=exclude&start=0&count=10&output=atom"
    initialize_csv(CSV_FILE)

    while True:
        existing_urls = fetch_existing_entries(CSV_FILE)
        new_entries = sec_feed_parser(url, existing_urls)

        if new_entries:
            append_to_csv(CSV_FILE, new_entries)
            print(f"Added {len(new_entries)} new entries to the CSV.")
        else:
            print("No new entries found.")

        # Sleep for 2 minutes before the next fetch
        time.sleep(120)

if __name__ == "__main__":
    main()
