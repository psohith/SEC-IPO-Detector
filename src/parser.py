# parser.py
import xml.etree.ElementTree as ET
from .constants import IPO_KEYWORDS
from .fetcher import fetch_form_s1_content

def parse_rss_feed(content):
    """Parse the RSS XML content and return a list of entries."""
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = []
    root = ET.fromstring(content)
    for entry in root.findall('atom:entry', ns):
        entries.append({
            'title': entry.find('atom:title', ns).text,
            'url': entry.find('atom:link', ns).attrib['href'],
            'summary': entry.find('atom:summary', ns).text.strip(),
            'updated': entry.find('atom:updated', ns).text,
            'category': entry.find('atom:category', ns).attrib.get('term'),
        })
    return entries


def is_ipo_filing(filing_url):
    """Check if the document content is related to an IPO."""
    document_content = fetch_form_s1_content(filing_url)
    return any(keyword in document_content for keyword in IPO_KEYWORDS)