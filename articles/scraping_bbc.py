import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import csv
import re
from datetime import date

html = requests.get("https://www.bbc.com/")
soup = BeautifulSoup(html.text, "html.parser")
items = soup.find_all(attrs={"data-testid":"dundee-card"})

with open("bbc_articles.csv", "w", newline='', encoding="UTF-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['date','type','topic','title','text','url'])

with open("bbc_articles.csv", "a", newline='', encoding = "UTF-8") as outfile:
    writer = csv.writer(outfile)
    for item in items:

        link = item.find(attrs={"data-testid":"internal-link"})
        if link:
            url = "https://www.bbc.com/" + link['href']
        else:
            url = None
        title = item.find(attrs={"data-testid":"card-headline"}).text

        if url:
            parts = url.split("/")
        
            if "article" in parts or "articles" in parts:
                type = "Article"
                topic = parts[4].capitalize()
            elif "video" in parts or "videos" in parts:
                type = "Video"
                topic = parts[4].capitalize()
            else:
                type=None
                topic=None
            writer.writerow([date.today(),type, topic, title,None,url])
