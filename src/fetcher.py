# fetcher.py
import requests
import time
from bs4 import BeautifulSoup
from .constants import HEADERS, SEC_BASE_URL

def fetch_rss_feed(url):
    """Fetch XML data from the SEC RSS feed URL."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        time.sleep(1)  # Avoid rate-limiting
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {url}: {e}")
        return None

def fetch_document_link(entry_url):
    """Retrieve the filing document link from the SEC entry URL."""
    try:
        response = requests.get(entry_url, headers=HEADERS)
        response.raise_for_status()
        time.sleep(1)
        soup = BeautifulSoup(response.content, 'html.parser')
        document_link = soup.find_all('tr')[1].find_all('td')[2].find('a')['href']
        return f"{SEC_BASE_URL}{document_link}" if document_link else None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SEC form from {entry_url}: {e}")
        return None

def fetch_form_s1_content(filing_url):
    """Retrieve the filing document content from the filling URL"""
    try:
        response = requests.get(filing_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error checking IPO status from {filing_url}: {e}")
        return ""