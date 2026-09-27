import json
import requests
import sql_manager
import random


TRIVIA_CATEGORIES = [
    # History & Geography
    "Modern History",
    "Ancient Civilizations",
    "World Leaders & Royalty",
    "Capital Cities & Landmarks",
    "Historic Exploration & Space Race",
    "Military History & Conflicts",
    # Pop Culture & Entertainment
    "Animated Movies & Shows",
    "90s & 2000s Nostalgia",
    "Sci-Fi & Fantasy Worlds",
    "Sitcoms & Comedy Series",
    "Box Office Blockbusters",
    "Celebrity & Pop Gossip",
    # Music & Performing Arts
    "Classic Rock & 80s Anthems",
    "Hip-Hop & R&B",
    "Broadway & Musical Theatre",
    "Chart-Topping Pop Hits",
    "Famous Album Covers & Lyrics",
    # Science & Nature
    "Space & Astronomy",
    "Marine Life & Oceanography",
    "Human Anatomy & Medical Curiosities",
    "Weather & Natural Disasters",
    "Animals & Wildlife",
    # Food, Drink & Lifestyle
    "World Cuisine & Signature Dishes",
    "Cocktails, Beer & Spirits",
    "Brand Logos & Slogans",
    "Fast Food & Candy Lore",
    "Fashion & Style Through the Decades",
    # Sports & Recreation
    "Olympic Games History",
    "World Cup & Global Football",
    "Championship Records & MVPs",
    "Board Games & Video Games",
]

URL = "http://localhost:11434/api/generate"


def query(prompt_topic):
    formatted_prompt = f"""
You are a trivia question answer generator for the game Shrimp.ly. The gameplay loop of shrimp.ly is the following:
A question is provided for the end user formatted as "Name a...". 
The user must then provide an answer that is seen as most obscure or rare for that category.
After an answer is given, the user will be given points based on the rarity of the answer.

TASK:
Generate a JSON object containing a question and up to 50 valid answers, each paired with its own rarity point score (ranging from 10 for very common to 100 for highly obscure).
If a question naturally has fewer valid answers (e.g., "Name a country that borders the United States"), provide only the correct total count.

EXAMPLE:
Input: "Create a question about agriculture"
Output:
{{
    "target_count": 25,
    "actual_count_generated": 23,
    "question": "Name a Fruit",
    "answers": [
        {{"answer": "Apple", "rarity_score": 10}},
        {{"answer": "Banana", "rarity_score": 10}},
        {{"answer": "Star Fruit", "rarity_score": 100}}
    ]
}}

NOW CREATE:
prompt_input: "{prompt_topic}"
"""

    generator_schema = {
        "type": "object",
        "properties": {
            "target_count": {"type": "integer"},
            "actual_count_generated": {"type": "integer"},
            "question": {"type": "string"},
            "answers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "answer": {"type": "string"},
                        "rarity_score": {"type": "integer"},
                    },
                    "required": ["answer", "rarity_score"],
                },
            },
        },
        "required": [
            "target_count",
            "actual_count_generated",
            "question",
            "answers",
        ],
    }

    payload = {
        "model": "gemma2:9b",
        "prompt": formatted_prompt,
        "format": generator_schema,
        "options": {
            "temperature": 0.4,
            "num_ctx": 4096,
        },
        "stream": False,
    }

    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        response_data = response.json()

        result = json.loads(response_data["response"])
        result["actual_count_generated"] = len(result.get("answers", []))

        # Pass parsed dict to sql_manager
        sql_manager.process_entry(result)
        sql_manager.print_database_contents()

        return result

    except Exception as e:
        print(f"Error generating question: {e}")
        return None


if __name__ == "__main__":

    for x in range(100):
        random_choice =  random.choice(TRIVIA_CATEGORIES)
        query(random_choice)