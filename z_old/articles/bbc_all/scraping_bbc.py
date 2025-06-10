import requests
from bs4 import BeautifulSoup
import csv
from datetime import date, datetime
import os

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
    with open("bbc_all.csv", 'r', newline='', encoding = "UTF-8") as infile:
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

    date_unformatted = datetime.strptime(str(date.today()), "%Y-%m-%d")
    date_formatted = date_unformatted.strftime("%#m/%#d/%Y")

    with open("bbc_all.csv", "a", newline='', encoding = "UTF-8") as outfile:
        writer = csv.writer(outfile)
        for item in items:
            link = item.find(attrs={"data-testid":"internal-link"})
            if link:
                url = "https://www.bbc.com/" + link['href']
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
                    writer.writerow([date_formatted,type, topic, title, url, text])
                    urls.append(url)

def run_scraping_past(archive_url, date):
    """
    Run scraping on the BBC website for a past date.
    """
    html = requests.get(archive_url)
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all(attrs={"data-testid":"dundee-card"})
    urls = get_urls()
    with open("bbc_all.csv", "a", newline='', encoding = "UTF-8") as outfile:
        writer = csv.writer(outfile)
        for item in items:
            link = item.find(attrs={"data-testid":"internal-link"})
            if link:
                url = "https" + (link['href'].split("https"))[-1]
            else:
                url = None
            title = item.find(attrs={"data-testid":"card-headline"}).text
            if url:
                if url not in urls:
                    html = requests.get(url)
                    soup = BeautifulSoup(html.text, "html.parser")

                    parts = url.split("/")
                    topic = parts[3].capitalize()

                    if "article" in parts or "articles" in parts:
                        type = "Article"
                        if topic == "Sport":
                            text = " ".join([content.text for content in (soup.find_all(attrs={"class":"ssrcss-1q0x1qg-Paragraph e1jhz7w10"}))])
                        else:
                            text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) 
                    elif "video" in parts or "videos" in parts:
                        type = "Video"
                        text = " ".join([content.text for content in (soup.find_all(attrs={"class":"sc-9a00e533-0 hxuGS"}))]) #})[:-2])])
                    writer.writerow([date,type, topic, title, url, text])
                    urls.append(url)

def sort_csv(file, sort_column):
    """
    Sorts CSV by date and removes duplicate entries.
    Use after running run_scraping_past().
    """
    with open(file, 'r', newline='', encoding = "UTF-8") as infile, open("temp.csv", 'w', newline='', encoding = "UTF-8") as outfile:
        reader = csv.reader(infile)
        header = next(reader)
        sorted_rows = sorted(reader, key=lambda row: row[sort_column])
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(sorted_rows)
    with open("temp.csv", 'r', newline='', encoding = "UTF-8") as infile, open(file, 'w', newline='', encoding="UTF-8") as outfile:
        reader = csv.reader(infile)
        header = next(reader)
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(sorted_rows)
    try:
        os.remove("temp.csv")
    except Exception:
        pass

# run this once a day

# run_scraping()
# run_scraping_past("https://web.archive.org/web/20250607120904/https://www.bbc.com/", "6/7/2025")
# sort_csv("bbc_all.csv", 0)

run_scraping()
sort_csv("bbc_all.csv", 0)



