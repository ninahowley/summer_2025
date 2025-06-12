import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def detect_whitespace(line:str) -> bool:
    """
    Returns a boolean indicating whether a line of text is mostly whitespace.
    """
    count = 0
    for char in line:
        if char == " ":
            count += 1
    if count > len(line)/3:
        return True
    return False

def detect_category(line:str) -> bool:
    """
    Returns a boolean indicating whether a line of text is a category.
    """
    return len(line.split(" ")) < 5

def get_url_text(url:str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout = 10)
        soup = BeautifulSoup(response.text, "html.parser")
        tags = soup.find_all(['p', 'h1', 'h2', 'h3', "li", "a"])

        text_parts = [(tag.text).split("\n") for tag in tags]
        lines = []
        for text in text_parts:
            for t in text:
                if t and (not detect_whitespace(t)) and (not detect_category(t)):
                    lines.append(t)
        return lines
    except Exception as e:
        print(e)
        return ""

def detect_imposter(site_text: list, threshold: int, amount:int) -> bool:
    """
    Returns a boolean indicating whether a given site is an imposter, 
    based on whether any lines are repeated a number of times at or above the threshold.
    """
    if site_text:
        l = pd.DataFrame(site_text)
        lines = l.value_counts()
        highest = lines.head(amount)
        nums = [num for num in highest]
        for num in nums:
            if num < threshold:
                return False
        return True
    return None

def reset_csv():
    with open('detection.csv', 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(['url','expected','response','threshold'])

def test_urls(url_dict:dict) -> None:
    with open('detection.csv', 'a', newline='', encoding='utf-8') as outfile:
        with open('detection.txt', 'w') as file:
            writer = csv.writer(outfile)
            file.write("Where Threshold is the number of times a line must repeat to be considered suspicious,\nand Amount is the minimum number of suspicious lines that make a website an imposter.")
            for t in range(1,11):
                for a in range(1, 6):
                    correct = 0
                    for url in url_dict:
                        text = get_url_text(url)
                        detected = detect_imposter(text, t, a)
                        writer.writerow([url, url_dict[url], detected, t])
                        if url_dict[url] == detected:
                            correct += 1
                    file.write(f"\n\nThreshold: {t}")
                    file.write(f"\nAmount: {a}")
                    file.write(f"\nCorrect: {correct}/{len(url_dict)}")
    
reset_csv()

url_dict = {
     "https://dartmouthtimes.com/": True,
     "https://hillsboroughsun.com/":True,
     "https://swnewhampshirenews.com/":True,
     "https://www.bbc.com/":False,
     "https://thewellesleynews.com/":False,
     "https://www.usatoday.com/":False
}

test_urls(url_dict)