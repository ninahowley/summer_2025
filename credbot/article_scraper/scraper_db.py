import requests
from bs4 import BeautifulSoup
import db_methods as db_methods
import csv
import ast

import scraper_methods as s

def scrape_from_csv():
    """
    Scrapes the article with the longest URL from each site in the CSV, inserting it into the database.
    """
    conn = db_methods.connect_db()
    data = []
    with open("data/mbfc_sites_all.csv", 'r', newline='', encoding="UTF-8") as csvfile:
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

        q = d['questionable']
        q_list = ast.literal_eval(q)
        if q:
            questionable = ", ".join(q_list)
        else:
            questionable = None

        try:
            urls = s.get_urls(domain)

            if urls is None:
                print("No valid URLs.")
                continue

            num_urls = len(urls)
            if num_urls > 5:
                num = 0
                nums_checked = []
                while len(nums_checked)<1:
                    content = s.scrape_url(domain, urls[num])

                    if content:
                        if len(content) > 500:
                            title = s.get_article_title(urls[num])
                            if title:
                                print(title)
                            if questionable:
                                print(questionable)
                            db_methods.insert_page(conn, name, domain, bias, credibility, reporting, questionable, urls[num], title, content)
                            nums_checked.append(num)
                            break
                    num+=1
                db_methods.commit_changes(conn)
        except Exception as e:
            print(e)
            continue
    db_methods.close_db(conn)


# scrape_from_csv()