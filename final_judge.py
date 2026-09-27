import json
import requests

url = "http://localhost:11434/api/generate"


'''
user_answer = "Blood Orange"
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
    {"answer": "Rambutan", "rarity_score": 70},
]
'''

def query2(answer_key_list, user_guess):
    # Extract string items from the list of dicts
    valid_answers = [
        item["answer"] if isinstance(item, dict) else item
        for item in answer_key_list
    ]

    # Reconstruct the prompt dynamically using the provided instructions
    formatted_prompt = f"""
You are a trivia evaluation judge for a game where players try to guess answers from a given list.

TASK:
Determine if `user_answer` is a correct match for any item in `answer_key`. Consider exact matches, minor typos, alternate spellings, and semantic sub-types or varieties (e.g., "Cavendish" is a type of "Banana").

EVALUATION RULES:
1. `matched_answer` MUST be an exact string from `answer_key` or null.
2. If `user_answer` matches a concept or variety of an item in `answer_key`, set `is_correct` to true and `matched_answer` to that exact item from `answer_key`.
3. If `user_answer` is unrelated or not represented in `answer_key`, set `is_correct` to false and `matched_answer` to null.

EXAMPLES =
- Input: user_answer="Aple", answer_key={json.dumps(valid_answers)}
  Output: {{"reasoning": "Aple is a minor typo for Apple.", "is_correct": true, "matched_answer": "Apple"}}

- Input: user_answer="Cavendish", answer_key={json.dumps(valid_answers)}
  Output: {{"reasoning": "Cavendish is a variety of Banana.", "is_correct": true, "matched_answer": "Banana"}}

- Input: user_answer="Peregrine Falcon", answer_key={json.dumps(valid_answers)}
  Output: {{"reasoning": "Peregrine Falcon is a bird and not in the key.", "is_correct": false, "matched_answer": null}}

- Input: user_answer="Jark Fruit", answer_key={json.dumps(valid_answers)}
  Output: {{"reasoning": "Jark Fruit is a minor typo for Jackfruit, which is in the key.", "is_correct": true, "matched_answer": "Jackfruit"}}
  

NOW EVALUATE:
user_answer: "{user_guess}"
answer_key: {json.dumps(valid_answers)}
"""

    payload = {
        "model": "gemma3:4b",
        "prompt": formatted_prompt,
        "format": {
            "type": "object",
            "properties": {
                "reasoning": {"type": "string"},
                "is_correct": {"type": "boolean"},
                "matched_answer": {"type": ["string", "null"]},
            },
            "required": ["reasoning", "is_correct", "matched_answer"],
        },
        "options": {
            "temperature": 0.0,
            "num_ctx": 4096,
        },
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        response_data = response.json()

        # Parse the JSON string output from Ollama
        final_answer = json.loads(response_data["response"])

        # Safety Check: Ensure the LLM returned a valid string from the key if marked correct
        if (
            final_answer.get("is_correct")
            and final_answer.get("matched_answer") not in valid_answers
        ):
            final_answer["is_correct"] = False
            final_answer["matched_answer"] = None
            final_answer["reasoning"] += (
                " (Overridden: matched_answer was not in answer key)"
            )

        print(final_answer)
        return final_answer

    except Exception as e:
        print(f"Error querying model: {e}")
        return {"is_correct": False, "matched_answer": None, "reasoning": str(e)}


# Execute evaluation
#query2(answer_key, user_answer)