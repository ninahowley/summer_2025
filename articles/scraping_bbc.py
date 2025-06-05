import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import csv
import re
from datetime import date

def reset_csv():
    with open("bbc_articles.csv", "w", newline='', encoding="UTF-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['date','type','topic','title','text','url'])

def run_scraping():
    html = requests.get("https://www.bbc.com/")
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all(attrs={"data-testid":"dundee-card"})

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
        
                html = requests.get(url)
                soup = BeautifulSoup(html.text, "html.parser")

                parts = url.split("/")

                if "article" in parts or "articles" in parts:
                    type = "Article"
                    topic = parts[4].capitalize()
                    text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) 
                elif "video" in parts or "videos" in parts:
                    type = "Video"
                    topic = parts[4].capitalize()
                    text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) #})[:-2])])
                writer.writerow([date.today(),type, topic, title, text, url])

#run this once a day
#run_scraping()
