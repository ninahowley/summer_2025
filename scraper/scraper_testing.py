import requests
from bs4 import BeautifulSoup
import db_setup
import csv
import time
import random

def get_urls(domain_url: str) -> list:
    """
    Returns a list of article URLS present on a webpage.
    """
    try:
        domain = f"https://{domain_url}"
        try:
            html = requests.get(domain, timeout=5)
        except requests.exceptions.Timeout:
            print("The request timed out.")
            return None
        soup = BeautifulSoup(html.text, "html.parser")
        links = soup.find_all("a")
        urls = []
        for link in links:
            l = link.get('href')
            if l:
                if len(l) > len(domain)+15:
                    if (l != "https://www."+domain_url) and (l != "https://www."+domain_url+"/"):
                        if ("/category/" not in l) and ("/author/" not in l) and ("/topics/" not in l) and ("?" not in l) and ("-" in l):
                            if domain_url in l:
                                if "https" in l:
                                    urls.append(l)
                                else:
                                    if domain_url[-1] != "/":
                                        urls.append(f"{domain_url}/{l}")
                                    else:
                                        urls.append(f"{domain_url}{l}")

        if urls:
            urls = list(set(urls))
            urls = sorted(urls, key=lambda url: len(url), reverse=True)
            return urls
        return None
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
            return None
            pass
    else:
        print("URL is external from domain.")
        return None

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
        questionable = ",".join(d['questionable'])

        try:
            urls = get_urls(domain)
            num_urls = len(urls)
            if num_urls > 10:
                num = 0
                nums_checked = []
                while len(nums_checked)<1:

                    # num = random.randint(3,num_urls-3)

                    content = scrape_url(domain, urls[num])
                    length = len(content.split(" "))

                    if num not in nums_checked and length > 100:
                        print(f"{num}: {urls[num]}")
                        print(f"Word count: {length}")
                        db_setup.insert_page(conn, name, domain, urls[num], bias, credibility, reporting, content)
                        nums_checked.append(num)
                        num+=1
                    else:
                        break
            db_setup.commit_changes(conn)
        except Exception as e:
            continue
    db_setup.close_db(conn)

scrape_from_csv()

#ran until _, delete to there in csv and rerun

#testing

# domain = "100daysinappalachia.com"
# urls = get_urls(domain)
# scrape_url(domain, urls[1])