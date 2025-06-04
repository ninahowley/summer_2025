import requests
import csv
from datetime import date
from googleapiclient.discovery import build

search_id = "e11ea7739f91c4174"
api_key = "AIzaSyDN9-FruLC5fdPd0pfFMaQ0MHj9gt9eg1A"

def google_custom_search(query, num_results=10):
    """ Pulls the top 10 results from a google search with the provided query.
    """
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(
        q=query,
        cx=search_id,
        num=num_results, # Number of results (max 10 per request)
    ).execute()
    return res

# with open('search_results.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["date", "query", "title", "link", "snippet"])

def test_getting_urls(query):
    results = google_custom_search(query)

    if 'items' in results:
        print(f"Search results for '{query}':")
        with open('search_results.csv', 'a', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for i, item in enumerate(results['items']):
                print(item['title'])
                writer.writerow([date.today(), query, item['title'], item['link'], item.get('snippet', '')])

query = "economy"

test_getting_urls(query)



