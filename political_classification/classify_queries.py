import csv
import requests
import json

# use LMStudio to load a model and categorize queries

SYSTEM_PROMPT = """
You are a political science expert. You are given a search query and need to evaluate its nature as political or not political.
Return ONLY a single-line JSON object in this format:
{ \"nature\": \"potentially political\" | \"non political\" }
Respond with no explanation, no extra text.
"""

EXAMPLES = (
"What to look for: Is the query political in nature? Is it related to the process of making decisions, exercising power, and governing within a community or society?\n"
"Potentially political: 'What are the key policies of the Democratic and Republican parties?', 'Election results', 'Impact of climate change legislation on the economy', 'gun laws', 'voting rights'\n"
"Non-political: 'Best exercises for lower back pain relief', 'How to bake sourdough bread at home', 'Top 10 tourist attractions in Japan', 'youtube', 'cat breeds'\n"
)

def assess_query(query: str):
    try:
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json={
                "model":
                "qwen/qwen3-14b",  # change this when testing other models
                "messages": [
                    {
                        "role": "system",
                        "content": EXAMPLES
                    },
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "system",
                        "content": f"Query being evaluated: {query}"
                    },
                ],
                "stream":
                False
            })
        return response
    except Exception as e:
        print("Request error:", e)
        return None

def extract_nature_from_content(content: str) -> str:
    # Find first '{' and last '}' to extract JSON substring
    start = content.find('{')
    end = content.rfind('}') + 1
    if start == -1 or end == -1:
        print("No JSON found in content")
        return ""
    json_str = content[start:end]
    try:
        data = json.loads(json_str)
        return data.get("nature", "").lower()
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return ""

def get_nature(query: str):
    try:
        response = assess_query(query)
        if not response or response.status_code != 200:
            print("Bad or no response")
            return ""
        response_data = response.json()
        content = response_data['choices'][0]['message']['content'].strip()
        nature = extract_nature_from_content(content)
        return nature or "n/a"
    except Exception as e:
        print("Error parsing response:", e)
        return ""

new_limit = 10 * 1024 * 1024
csv.field_size_limit(new_limit)

if __name__ == "__main__":
    with open("query_collection.csv", "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        with open("queries_categorized.csv", "w", encoding="utf-8",
                  newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["query", "category", "nature"])
            next(reader)
            for r in reader:
                nature = get_nature(r[0])
                print(r[0])
                writer.writerow([r[0], r[1], nature])