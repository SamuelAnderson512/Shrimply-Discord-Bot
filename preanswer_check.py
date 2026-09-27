from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import final_judge


test_answers = [
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
guess_answer = "Bakon"



def check_answer(answer_key, string):
    for answer in answer_key:
        if fuzz.ratio(answer["answer"], string) >= 90:
            print(f"MATCH!{answer}")
            return True, answer["answer"], answer["rarity_score"]

    print("No Answers Matched")
    temp_dict = final_judge.query2(answer_key,string)

    

    if temp_dict["is_correct"] == True:
        for x in test_answers:
                if x["answer"] == temp_dict["matched_answer"]:
                     points = x["rarity_score"]
                     break
        return True, temp_dict["matched_answer"], points
    else:
        return False, "None", 0

#check_answer(answer_key, guess_answer)