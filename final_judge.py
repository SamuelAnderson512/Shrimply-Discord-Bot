import requests
import json
url = "http://localhost:11434/api/generate"

user_answer = "Cavendish"
answer_key = [
    {"answer": "Apple", "rarity_score": 10},
    {"answer": "Banana", "rarity_score": 10},
    {"answer": "Orange", "rarity_score": 10},
    {"answer": "Strawberry", "rarity_score": 10},
    {"answer": "Grape", "rarity_score": 10},
    {"answer": "Watermelon", "rarity_score": 20},
    {"answer": "Pineapple", "rarity_score": 20},
    {"answer": "Mango", "rarity_score": 20},
    {"answer": "Blueberry", "rarity_score": 20},
    {"answer": "Peach", "rarity_score": 30},
    {"answer": "Kiwi", "rarity_score": 30},
    {"answer": "Lemon", "rarity_score": 30},
    {"answer": "Lime", "rarity_score": 30},
    {"answer": "Plum", "rarity_score": 40},
    {"answer": "Pomegranate", "rarity_score": 40},
    {"answer": "Fig", "rarity_score": 40},
    {"answer": "Passion Fruit", "rarity_score": 50},
    {"answer": "Dragon Fruit", "rarity_score": 50},
    {"answer": "Star Fruit", "rarity_score": 50},
    {"answer": "Guava", "rarity_score": 60},
    {"answer": "Durian", "rarity_score": 60},
    {"answer": "Jackfruit", "rarity_score": 60},
    {"answer": "Mangosteen", "rarity_score": 70},
    {"answer": "Rambutan", "rarity_score": 70}
]

payload = {
    "model": "gemma-judge",
    "prompt": "Name a Fruit",
    "format": "json",
    "options": {
        "temperature": 0.1,
        "num_ctx": 4096
    },
    "stream": False,
}

def query2(answer_key, result):

    print(f"user_answer:{result},answer_key:{payload}")

    payload["prompt"] = f"user_answer:{result},answer_key:{answer_key}"

    response = requests.post(url, json=payload)
    response_data = response.json()
    final_answer = json.loads(response_data["response"])
    print(final_answer)

query2(answer_key,user_answer)