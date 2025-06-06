import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

def reset_csv():
    with open("bbc_news.csv", "w", newline='', encoding="UTF-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['date','type','title', 'url', 'text'])

def run_scraping():
    html = requests.get("https://www.bbc.com/news")
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all(attrs={"data-testid":"dundee-card"})

    with open("bbc_news.csv", "a", newline='', encoding = "UTF-8") as outfile:
        writer = csv.writer(outfile)
        for item in items:

            link = item.find(attrs={"data-testid":"internal-link"})
            if link:
                url = "https://www.bbc.com/" + link['href']
            else:
                url = None
            title = item.find(attrs={"data-testid":"card-headline"}).text

            if url:
        
                html = requests.get(url)
                soup = BeautifulSoup(html.text, "html.parser")

                parts = url.split("/")
                topic = parts[4]

                if topic == "news":
                    if "article" in parts or "articles" in parts:
                        type = "Article"
                        text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) 
                    elif "video" in parts or "videos" in parts:
                        type = "Video"
                        text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) #})[:-2])])
                    writer.writerow([date.today(),type, title, url, text])

def run_scraping_past(archive_url, date):
    html = requests.get(archive_url)
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all(attrs={"data-testid":"dundee-card"})
    with open("bbc_news.csv", "a", newline='', encoding = "UTF-8") as outfile:
        writer = csv.writer(outfile)
        for item in items:

            link = item.find(attrs={"data-testid":"internal-link"})

            if link:
                url = "https" + (link['href'].split("https"))[-1]
            else:
                url = None
            title = item.find(attrs={"data-testid":"card-headline"}).text

            if url:
                html = requests.get(url)
                soup = BeautifulSoup(html.text, "html.parser")
                
                parts = url.split("/")
                topic = parts[3]

                if topic == "news":
                    if "article" in parts or "articles" in parts:
                        type = "Article"
                        text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) 
                    elif "video" in parts or "videos" in parts:
                        type = "Video"
                        text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) #})[:-2])])
                    writer.writerow([date, type, title, url, text])

#run this once a day

# reset_csv()
# run_scraping()

#run this with a webarchive link to get past articles --> choose first time after noon
#examples:
# run_scraping_past("https://web.archive.org/web/20250604121145/https://www.bbc.com/news", "2025-06-04")
# run_scraping_past("https://web.archive.org/web/20250603121113/https://www.bbc.com/news", "2025-06-03")
