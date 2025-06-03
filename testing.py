import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date

def get_response(system, user):
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json={
            # "model": "deepseek/deepseek-r1-0528-qwen3-8b",
            "model": "deepseek/deepseek-r1-0528-qwen3-8b",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "character_schema": [
                {
                "type": "json_schema",
                "json_schema": {
                    "name": "fact checker",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "characters": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "fact": {"type": "boolean"},
                                        "reasoning": {"type": "string"}
                                    },
                                    "required": ["fact", "reasoning"]
                                }
                            }
                        },
                        "required": ["characters"]
                    },
                }
            }
        ]
        }
    )
    return response

# Define the expected response structure

#print(response.json())
#response = response.json()['choices'][0]['message']['content'].split("\n")
#print(response[-1])


def test_bot_urls(urls, system):
    for url in urls:
        site = requests.get(url)
        site.raise_for_status() 
        text = site.text
        # meta = str(BeautifulSoup(html, "html.parser").meta)
        # soup = BeautifulSoup(html, "html.parser")
        # text = str(soup.find_all("div"))

        # stuff = f"meta: {meta}, text: {text}"
        

        response = get_response(system, text).json()
        print(response)
        response = response['choices'][0]['message']['content'].split("\n")

        print(f"URL: {url}")
        print(response[-1], "\n")
        
# urls = ["https://www.cnn.com/", "https://www.foxnews.com/"]
# system = "You are a simple credibility checker. Respond in 2 sentences. The first sentence is a credibility score from 1 through 5. The second sentence is a brief reasoning." 
# test_bot_urls(user, system)


def test_bot(user, system):
        for statement in user:
            response = get_response(system, statement).json()
            response = response['choices'][0]['message']['content'].split("\n")

            print(f"Statement: {statement}")
            print(f"Response: {response[-1]}", "\n")

user = ["Cats are mammals.", "The current year is 2025.", "Joe Biden is president."]
system = f"You are a simple fact checker. Respond in 2 sentences. The first sentence is True or False. The second sentence is an explanation."

test_bot(user, system)
