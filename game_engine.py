sample = {
    'target_count': 25, 
    'actual_count_generated': 25, 
    'question': 'Name a Fruit', 
    'answers': 
        [
            {'answer': 'Apple', 'rarity_score': 10}, 
            {'answer': 'Banana', 'rarity_score': 10}, 
            {'answer': 'Orange', 'rarity_score': 10}, 
            {'answer': 'Grape', 'rarity_score': 10}, 
            {'answer': 'Strawberry', 'rarity_score': 10}, 
            {'answer': 'Watermelon', 'rarity_score': 10}, 
            {'answer': 'Mango', 'rarity_score': 30}, 
            {'answer': 'Pineapple', 'rarity_score': 30}, 
            {'answer': 'Blueberry', 'rarity_score': 30}, 
            {'answer': 'Peach', 'rarity_score': 30}, 
            {'answer': 'Kiwi', 'rarity_score': 60}, 
            {'answer': 'Pomegranate', 'rarity_score': 60}, 
            {'answer': 'Lychee', 'rarity_score': 60}, 
            {'answer': 'Dragon Fruit', 'rarity_score': 60}, 
            {'answer': 'Passion Fruit', 'rarity_score': 100}, 
            {'answer': 'Durian', 'rarity_score': 100}, 
            {'answer': 'Star Fruit', 'rarity_score': 100}, 
            {'answer': 'Guava', 'rarity_score': 100}, 
            {'answer': 'Jackfruit', 'rarity_score': 100}, 
            {'answer': 'Rambutan', 'rarity_score': 100}, 
            {'answer': 'Mangosteen', 'rarity_score': 100}, 
            {'answer': 'Papaya', 'rarity_score': 100}, 
            {'answer': 'Persimmon', 'rarity_score': 100}
        ]
    }




def serve_question():
    question = sample["question"]
    answers = sample["answers"]
    for answer in answers:
        print(answer["answer"])
    
    return question, answers