import csv
import requests
from datetime import datetime, timedelta
import time 

"""
API DATA:

mediastack api key 94c6f2f922dd0c0dd6dd1aea0acbed27
mediastack url http://api.mediastack.com/v1/news

#gdelt url https://api.gdeltproject.org/api/v2/doc/doc

newsdata.io key pub_59879195b81d0c56a22751d35fc801277f5bc
newsdata.io url https://newsdata.io/api/1/news
"""

def fetch_latest_news():
    url = "http://api.mediastack.com/v1/news"
    api_key = "94c6f2f922dd0c0dd6dd1aea0acbed27"
    keywords_list = ['JD Vance', 'J.D. Vance', 'J. D. Vance']  # List of keywords to search for

    # Date range: One year ago
    today = datetime.now()
    two_mo_ago = today - timedelta(days=14)
    from_date = two_mo_ago.strftime('%Y%m%d000000') #gdelt format 
    to_date = today.strftime('%Y%m%d235959')
    page = 1

    all_articles = []
    while True:
        params = {
            'access_key': api_key,
            'q': keywords_list,
            'language': 'en',
            'date': f"{from_date},{to_date}"
        }
        

        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            print(response.text)  # Print the error for debugging
            continue

        data = response.json()

        if not data.get('data'):
            continue

        # Append matching articles to the list
        for article in data['data']:
            all_articles.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'publishedAt': article.get('publishedAt', ''),
                'source': article.get('source', ''),
                'url': article.get('url', '')
            })

  
        print(f"Total articles fetched: {len(all_articles)}")
        return all_articles


def save_to_csv(articles, filename):
    # Append articles to a CSV file
    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header only if the file is empty
        if csvfile.tell() == 0:
            writer.writerow(['Title', 'Description', 'Published At', 'Source'])
        
        for article in articles:
            writer.writerow([
                article['title'], 
                article['description'], 
                article['publishedAt'], 
                article['source'], 
            ])


# Fetch articles and save to CSV
if __name__ == '__main__':
    articles = fetch_latest_news()
    if articles:
        save_to_csv(articles, 'mediastack_dec1.csv')
        print("Articles have been saved to 'news_dataio_articles.csv'.")
