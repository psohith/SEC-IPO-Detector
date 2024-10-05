# constants.py

# Base URLs
SEC_BASE_URL = "https://www.sec.gov"
RSS_FEED_PATH = "/cgi-bin/browse-edgar"
RSS_FEED_PARAMS = {
    "action": "getcurrent",
    "CIK": "",
    "type": "S-1",
    "company": "",
    "dateb": "",
    "owner": "exclude",
    "start": "0",
    "count": "10",
    "output": "atom",
}

# Headers
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
}

# CSV file path
CSV_FILE_PATH = 'sec_filings.csv'

# Polling interval
POLLING_INTERVAL = 2  # in seconds

# Keywords
IPO_KEYWORDS = ["Initial Public Offering", "IPO", "going public", "underwriter", "use of proceeds"]

# Function to generate the full RSS feed URL with parameters
def get_rss_feed_url():
    from urllib.parse import urlencode
    return f"{SEC_BASE_URL}{RSS_FEED_PATH}?{urlencode(RSS_FEED_PARAMS)}"

