import os
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import hashlib

FEED_URL = 'https://rss.app/feeds/E9RaLLqffEhiqsbk.xml'
OUTPUT_DIR = 'content/post/'  # Change this to match your structure

os.makedirs(OUTPUT_DIR, exist_ok=True)

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')

response = requests.get(FEED_URL)
root = ET.fromstring(response.content)

for item in root.findall(".//item"):
    description = item.find('description').text or ''
    pub_date = item.find('pubDate').text or datetime.now().isoformat()
    link = item.find('link').text or ''

    # Create a unique slug from date + content hash
    content_hash = hashlib.md5(description.encode()).hexdigest()[:6]
    date_str = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
    slug = f"{date_str}-{content_hash}"

    filename = os.path.join(OUTPUT_DIR, f"{slug}.md")

    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(f"---\n")
            f.write(f"title: \"Lab Update\"\n")
            f.write(f"date: {pub_date}\n")
            f.write(f"---\n\n")
            f.write(f"{description.strip()}\n")
        print(f"✅ Created: {filename}")
    else:
        print(f"⚠️ Already exists: {filename}")
