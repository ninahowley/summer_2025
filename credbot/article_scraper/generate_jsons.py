import csv
import ast
import json
import sqlite3
from bs4 import BeautifulSoup

def parseHTML(website_text: str):
    """
    Created by: https://github.com/ezhowl/CredBot/blob/main/credbot2024_v2/backend/assessment.py
    """
    soup = BeautifulSoup(website_text, 'html.parser')
    content = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])
    formatted_text = []

    for tag in content:
        text = tag.get_text(strip=True)
        if tag.name.startswith('h'):
            formatted_text.append(f"**{text}**")
        else:
            formatted_text.append(text)

    final_text = '\n'.join(formatted_text)
    cleaned_text = ' '.join(final_text.split())
    return cleaned_text

def articlesdb_to_jsons():
    """
    Transfers the article data collected in the large db to individual jsons.
    Parses and saves raw HTML as text using credbot parseHTML function.
    ("articles.db" @ https://github.com/ninahowley/summer_2025/releases/tag/Data)
    """
    conn = sqlite3.connect("articles.db")
    cur = conn.cursor()

    data = cur.execute("SELECT * FROM articles").fetchall()
    
    for d in data:
        line = {"id":d[0], "name":d[1], "domain":d[2], "bias":d[3], "credibility":d[4], "reporting":d[5], "questionable":d[6], "url":d[7], "title":d[8], "content": parseHTML(d[9])}
        with open(f"articles/article-{line['id']}.json", "w") as outfile:
            json.dump(line, outfile)

articlesdb_to_jsons()