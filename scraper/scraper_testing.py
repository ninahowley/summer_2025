import requests
from bs4 import BeautifulSoup
import db_setup
import csv
from datetime import time
import random

def get_urls(domain_url: str) -> list:
    """
    Returns a list of article URLS present on a webpage.
    """
    try:
        domain = f"https://{domain_url}"
        html = requests.get(domain)
        soup = BeautifulSoup(html.text, "html.parser")
        links = soup.find_all("a")
        urls = []
        for link in links:
            l = link.get('href')
            if len(l) > len(domain)+15:
                if (l != "https://www."+domain_url) and (l != "https://www."+domain_url+"/"):
                    if "https" in l:
                        urls.append(l)
                    else:
                        if domain_url[-1] != "/":
                            urls.append(f"{domain_url}/{l}")
                        else:
                            urls.append(f"{domain_url}{l}")
        return urls
    except Exception:
        return None

def scrape_url(domain_url:str, url:str) -> str:
    """
    Returns the HTML string of the content within all 'p', 'h1', 'h2', 'h3' and 'a' tags from a URL.
    Checks whether the article is part of the domain before scraping.
    """
    if domain_url in url:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            tags = soup.find_all(['p', 'h1', 'h2', 'h3'])
            text = []
            for tag in tags:
                text.append(tag.get_text(separator=' ', strip=True))
            content = '\n'.join(text)
            return content
        except Exception:
            pass
    else:
        print("URL is external from domain.")

def scrape_from_csv():
    """
    Scrapes the 3 middle-most articles from each site in the CSV and adds them to the database.
    """
    conn = db_setup.connect_db()
    data = []
    with open("mbfc_sites.csv", 'r', newline='', encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    
    for d in data:
        name = d['name']
        print("-------------------\n",name)
        domain = d['domain']
        bias = d['bias']
        credibility = d['credibility']
        reporting = d['reporting']

        try:
            urls = get_urls(domain)
            num_urls = len(urls)
            if num_urls > 10:

                nums_checked = []
                while len(nums_checked)<3:

                    num = random.randint(4,num_urls-4)
                    content = scrape_url(domain, urls[num])

                    if num not in nums_checked and len(content.split(" ")) > 250:
                        print(f"{len(nums_checked)+1}: {urls[num]}")
                        print(f"Word count: {len(content.split(' '))}")
                        db_setup.insert_page(conn, name, domain, urls[num], bias, credibility, reporting, content)
                        nums_checked.append(num)

                    else:
                        continue
            db_setup.commit_changes(conn)
        except Exception:
            continue
    db_setup.close_db(conn)


scrape_from_csv()

#testing

# domain = "100daysinappalachia.com"
# urls = get_urls(domain)
# scrape_url(domain, urls[1])