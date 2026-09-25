import requests
import json
url = "http://localhost:11434/api/generate"

payload1 = {
    "model": "gemma-custom",
    "prompt": "Name a Fruit",
    "format": "json",
    "options": {
        "temperature": 0.1,
        "num_ctx": 4096
    },
    "stream": False,
}

payload2 = {
    "model": "gemma-judge",
    "prompt": "Barana",
    "format": "json",
    "options": {
        "temperature": 0.5,
        "num_ctx": 4096
    },
    "stream": False,
}

def query(payload):
    response = requests.post(url, json=payload)
    response_data = response.json()
    fruit_json = json.loads(response_data["response"])
    print(type(fruit_json))
    print(fruit_json)
    return fruit_json["answers"]

def query2(payload, result):

    print(f"user_answer:{result},answer_key:{payload}")

    payload2["prompt"] = f"user_answer:{result},answer_key:{payload}"

    response = requests.post(url, json=payload2)
    response_data = response.json()
    final_answer = json.loads(response_data["response"])
    print(final_answer)

temp = query(payload1)
fruit_guess = input("Name a Fruit")
query2(temp, fruit_guess)