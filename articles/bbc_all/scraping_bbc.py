import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

def reset_csv():
    """
    Reset CSV.
    """
    with open("bbc_all.csv", "w", newline='', encoding="UTF-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['date','type','topic','title', 'url', 'text'])

def get_urls():
    """
    Returns a list of URLS present in CSV.
    Use for avoidance of duplicates.
    """
    with open("bbc_news.csv", 'r', newline='') as infile:
        reader = csv.reader(infile)
        return [row[3] for row in reader]

def run_scraping():
    """
    Run scraping on the BBC news website for the current day.
    """
    html = requests.get("https://www.bbc.com/")
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all(attrs={"data-testid":"dundee-card"})
    urls = get_urls()
    with open("bbc_all.csv", "a", newline='', encoding = "UTF-8") as outfile:
        writer = csv.writer(outfile)
        for item in items:
            link = item.find(attrs={"data-testid":"internal-link"})
            if link:
                url = "https://www.bbc.com/" + link['href']
                urls.append(url)
            else:
                url = None
            title = item.find(attrs={"data-testid":"card-headline"}).text
            if url:
                if url not in urls:
                    html = requests.get(url)
                    soup = BeautifulSoup(html.text, "html.parser")

                    parts = url.split("/")

                    if "article" in parts or "articles" in parts:
                        type = "Article"
                        topic = parts[4].capitalize()
                        if topic == "Sport":
                            text = " ".join([content.text for content in (soup.find_all(attrs={"class":"ssrcss-1q0x1qg-Paragraph e1jhz7w10"}))])
                        else:
                            text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) 
                    elif "video" in parts or "videos" in parts:
                        type = "Video"
                        topic = parts[4].capitalize()
                        text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) #})[:-2])])
                    writer.writerow([date.today(),type, topic, title, url, text])

# run this once a day

# run_scraping()


