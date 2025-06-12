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

def detect_imposter(site_text: list, threshold: int) -> bool:
    """
    Returns a boolean indicating whether a given site is an imposter, 
    based on whether any lines are repeated a number of times at or above the threshold.
    """
    if site_text:
        l = pd.DataFrame(site_text)
        lines = l.value_counts()
        highest = lines.head(1)
        num = highest.iloc[0]

        if num >= threshold:
            # print(f"This website is an imposter or is otherwise suspicious based on the given repetition threshold of {threshold}.")
            # print(f"The following line is repeated {num} times.")
            # print(f'"{highest.index[0][0]}"')
            return True
        else:
            # print(f"This website does not appear to be suspicious based on the given repetition threshold of {threshold}.")
            return False
    return

def reset_csv():
    with open('detection.csv', 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(['url','expected','response','threshold'])

def test_urls(url_dict:dict) -> None:
    with open('detection.csv', 'a', newline='', encoding='utf-8') as outfile:
        with open('detection.txt', 'w') as file:
            writer = csv.writer(outfile)
            for i in range(0,11):
                correct = 0
                for url in url_dict:
                    text = get_url_text(url)
                    detected = detect_imposter(text, i)
                    writer.writerow([url, url_dict[url], detected, i])
                    if url_dict[url] == detected:
                        correct += 1
                if i!=0:
                     file.write("\n\n")
                file.write(f"Threshold: {i}")
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