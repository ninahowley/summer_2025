import csv
import ast
import json
import jsonlines

import scraper_methods as s


def scrape_from_csv():
    """
    Scrapes the article with the longest URL from each site in the CSV, inserting it into the json file.
    """

    data = []
    
    with open("data/mbfc_sites_all.csv", 'r', newline='', encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    with jsonlines.open("articles.jsonl", 'w') as outfile:

        for d in data:
            info = None
            name = d['name']
            print("-------------------\n",name)
            domain = d['domain']
            bias = d['bias']
            credibility = d['credibility']
            reporting = d['reporting']

            q = d['questionable']
            q_list = ast.literal_eval(q)
            questionable = ", ".join(q_list)

            if questionable == "":
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
                                
                                info = {
                                    "name": name,
                                    "domain": domain,
                                    "bias": bias,
                                    "credibility": credibility,
                                    "reporting": reporting,
                                    "questionable": questionable,
                                    "url": urls[num],
                                    "title": title,
                                    "content": content
                                    }
                                nums_checked.append(num)
                                break
                        num+=1
                    if info:
                        outfile.write(info)
            except Exception as e:
                print(e)
                continue


# scrape_from_csv()