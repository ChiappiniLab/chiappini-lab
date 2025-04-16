import feedparser
import os
import re
from datetime import datetime

# 🔁 Replace this with your RSS feed from rss.app
FEED_URL = 'https://rss.app/feeds/E9RaLLqffEhiqsbk.xml'
OUTPUT_DIR = 'content/post/'  # or content/post/

os.makedirs(OUTPUT_DIR, exist_ok=True)

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')

feed = feedparser.parse(FEED_URL)

for entry in feed.entries:
    title = entry.title or "Untitled Post"
    slug = slugify(title)[:50]
    date = entry.published or datetime.now().isoformat()
    link = entry.link
    summary = entry.summary or ""

    filename = os.path.join(OUTPUT_DIR, f"{slug}.md")

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(f"---\n")
            f.write(f"title: \"{title}\"\n")
            f.write(f"date: {date}\n")
            f.write(f"summary: \"{summary.strip()}\"\n")
            f.write(f"---\n\n")
            f.write(f"[View on Twitter]({link})\n")
        print(f"✅ Created: {filename}")
    else:
        print(f"⚠️ Skipped (already exists): {filename}")
