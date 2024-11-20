import requests
import csv
from datetime import datetime, timedelta
import os 

# my key beefd4e0a5a64887b8d27faad06cf8da
# ariane's key bf1be07d5e2947d6b6e91c4f6c9d1439

def fetch_latest_news():
    url = "https://newsapi.org/v2/everything"
    api_key = 'bf1be07d5e2947d6b6e91c4f6c9d1439'
    keywords = 'JD Vance OR "J.D. Vance" OR "J. D. Vance"'

    params = {
        'q': keywords,
        'apiKey': api_key,
        'language': 'en',
        'pageSize': 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    filtered_articles = []
    if data['status'] == 'ok':
        for article in data['articles']:
            try:
              # Ensure title and description are strings
              title = article.get('title', '') or ''
              description = article.get('description', '') or ''

              # Filter based on keywords
              if any(name.lower() in (title + description).lower() for name in
                    ["jd vance", "j.d. vance", "j. d. vance"]):
                  source = article['source']['name']
                  url = article['url']

                  # Print to verify
                  print(f"Title: {title}")
                  print(f"Source: {source}")
                  print(f"Description: {description}")
                  print(f"URL: {url}")

                  # Append to list
                  filtered_articles.append({
                      'title': title,
                      'description': description,
                      'source': source,
                      'url': url
                  })
            except Exception as e:
              continue
    else:
        print(f"API Error: {data.get('message', 'Unknown error')}")

    print(f"Total filtered articles: {len(filtered_articles)}")  # Check if articles were gathered
    return filtered_articles



# Fetch articles
articles = fetch_latest_news()

# Save to CSV
csv_file = 'articles.csv'
csv_columns = ['title', 'description', 'source', 'url']


try:
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        if not file_exists:
            writer.writeheader()  # Write column headers only if file doesn't exist
        writer.writerows(articles)  # Write article data
    print(f"Articles appended to {csv_file}")
except IOError:
    print("I/O error")
