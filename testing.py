import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
import csv
import pandas as pd

def get_response(model, prompt, input):
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": input}
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

def test_bot(model, inputs, prompt):
        for input in inputs:
            response = get_response(model, prompt, input).json()
            response = response['choices'][0]['message']['content'].split("\n")

            print(f"Statement: {input}")
            print(f"Response: {response[-1]}", "\n")

            with open('tests.csv', 'a', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow([model, input, inputs[input], response[-1]])

model = "deepseek/deepseek-r1-0528-qwen3-8b"
inputs = {"Cats are mammals.": True, "Blue is a warm color.": False, "The current year is 2025.":True, "Joe Biden is president.":False}
prompt = f"You are a simple fact checker. Respond in 2 sentences. The first sentence is True or False. The second sentence is an explanation."

test_bot(model, inputs, prompt)