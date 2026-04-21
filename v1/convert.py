import json
import sys
from datetime import datetime

# Read existing file
with open('/home/jason/ai-knowledge-base/knowledge/raw/github-trending-2026-04-20.json', 'r') as f:
    data = json.load(f)

# Transform to new format
items = []
for item in data:
    # Extract name from title
    name = item.get('title', '')
    # Extract stars from popularity
    stars = item.get('popularity', 0)
    # Summary already exists
    summary = item.get('summary', '')
    # URL
    url = item.get('url', '')
    
    # Language and topics not available, set empty
    language = ''
    topics = []
    
    items.append({
        'name': name,
        'url': url,
        'summary': summary,
        'stars': stars,
        'language': language,
        'topics': topics
    })

# Create new structure
output = {
    'source': 'github_trending',
    'skill': 'github-trending',
    'collected_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
    'items': items
}

# Write to new file (overwrite existing)
output_file = '/home/jason/ai-knowledge-base/knowledge/raw/github-trending-2026-04-20.json'
with open(output_file, 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'Transformed {len(items)} items to {output_file}')