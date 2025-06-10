import requests
import asyncio

def get_response(model, prompt, input):
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json={
            "model": model,
            "messages": [
                {"role": "assistant", "content": prompt},
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
        total = len(inputs)
        correct = 0
        for input in inputs:
            statement = input
            answer = inputs[input]

            response = get_response(model, prompt, input).json()
            response = response['choices'][0]['message']['content'].split("\n")

            print(f"Statement: {statement}")
            print(f"Answer: {answer}")
            print(f"Response: {response[-1]}", "\n")

            if str(answer) in response[-1]:
                 correct += 1
        if correct > 0:
            percent_correct = round((correct/total)*100, 2)
        else:
             percent_correct = 0.0
        print("Testing complete...")
        print(f"Percent correct: {percent_correct}%")

model = "mistralai/mistral-7b-instruct-v0.3"
inputs = {"Cats are mammals.": True, "Blue is a warm color.": False, }
prompt = f"You are a simple fact checker. Respond in one word: True or False."

test_bot(model, inputs, prompt)