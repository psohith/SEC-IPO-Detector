# parser.py
import xml.etree.ElementTree as ET
from datetime import datetime
from .constants import IPO_KEYWORDS
from .fetcher import fetch_form_s1_content
from .utils import normalize_spaces_and_newlines
from .openAI import get_gpt_responce



def parse_rss_feed(content, latest_updated_time=None):
    """Parse the RSS XML content and return a list of entries up to the  latest_updated_time"""
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = []
    root = ET.fromstring(content)

    for entry in root.findall('atom:entry', ns):
        updated_time_str = entry.find('atom:updated', ns).text
        updated_time = datetime.strptime(updated_time_str,  '%Y-%m-%dT%H:%M:%S%z')

        if latest_updated_time is not None and updated_time <= latest_updated_time:
            break

        entries.append({
            'title': entry.find('atom:title', ns).text,
            'url': entry.find('atom:link', ns).attrib['href'],
            'summary': entry.find('atom:summary', ns).text.strip(),
            'updated': updated_time_str,
            'category': entry.find('atom:category', ns).attrib.get('term'),
        })

    return entries


def is_ipo_filing(filing_url):
    """Check if the document content is related to an IPO."""
    document_content = fetch_form_s1_content(filing_url)
    document_content = normalize_spaces_and_newlines(document_content)
    index_table_ind = 12000
    try:
        index_table_ind = document_content.index("table of content")
    except:
        pass
    trimed_doc = document_content[:index_table_ind]
    gptResonce = str(get_gpt_responce(trimed_doc)).lower()
    keywords = ['yes','true']
    return any(keyword in gptResonce for keyword in keywords)
