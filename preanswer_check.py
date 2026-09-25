from fuzzywuzzy import fuzz
from fuzzywuzzy import process


test_answers = ["Bacon","Burgers","Fries","Salmon","Tostada"]
guess_answer = "Bakon"



def check_answer(answer_key, string):
    for answer in answer_key:
        if fuzz.ratio(answer["answer"], string) >= 80:
            print(f"MATCH!{answer}")
            return True, answer["answer"], answer["rarity_score"]

    print("No Answers Matched")
    return False, string, 0