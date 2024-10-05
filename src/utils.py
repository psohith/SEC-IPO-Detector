# utils.py
import csv
import os

def initialize_csv(file_path):
    """Initialize CSV file with headers if it does not exist."""
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'URL', 'Summary', 'Updated', 'Category', 'Document Link', 'Is IPO'])

def fetch_existing_urls(file_path):
    """Fetch existing URLs from the CSV to avoid duplicate entries."""
    existing_urls = set()
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_urls.add(row['URL'])
    return existing_urls

def append_to_csv(file_path, entries):
    """Append new entries to the CSV."""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for entry in entries:
            writer.writerow([entry['title'], entry['url'], entry['summary'], entry['updated'], entry['category'], entry['documentLink'], entry['isIPO']])

def get_latest_updated_time(file_path):
    """Feteches the latest added timestamp"""
    latest_time = None
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            updated_time = datetime.strptime(row['Updated'], '%Y-%m-%dT%H:%M:%S%z')

            if latest_time is None or updated_time > latest_time:
                latest_time = updated_time

    return latest_time
