import os
import re
import hashlib
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# === CONFIG ===
FEED_URL = 'https://rss.app/feeds/E9RaLLqffEhiqsbk.xml'
OUTPUT_DIR = 'content/news/'

# === SETUP ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')

# === FETCH FEED ===
response = requests.get(FEED_URL)
root = ET.fromstring(response.content)

# === PROCESS EACH ITEM ===
for item in root.findall(".//item"):
    description = item.find('description').text or ''
    pub_date = item.find('pubDate').text or datetime.now().isoformat()
    link = item.find('link').text or ''

    # Use content hash to guarantee uniqueness
    content_hash = hashlib.md5(description.encode()).hexdigest()[:6]

    # Parse RSS date format like: "Wed, 16 Apr 2025 15:37:59 GMT"
    try:
        date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
    except Exception:
        date_obj = datetime.now()

    date_str = date_obj.strftime('%Y-%m-%d')
    slug = f"{date_str}-{content_hash}"

    filename = os.path.join(OUTPUT_DIR, f"{slug}.md")

    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(f"---\n")
            f.write(f"title: \"Lab Update\"\n")
            f.write(f"date: {date_obj.isoformat()}\n")
            f.write(f"---\n\n")
            f.write(f"{description.strip()}\n")
        print(f"✅ Created: {filename}")
    else:
        print(f"⚠️ Already exists: {filename}")
