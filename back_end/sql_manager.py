import sqlite3

DB_NAME = "shrimply.db"


def get_connection():
    """Returns a new connection configured with foreign key support."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Initializes schema if tables do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            q_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_body TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            a_id INTEGER PRIMARY KEY AUTOINCREMENT,
            q_id INTEGER NOT NULL,
            answer_body TEXT NOT NULL,
            rarity_score INTEGER,
            FOREIGN KEY (q_id) REFERENCES questions (q_id) ON DELETE CASCADE
        )
        """)
        conn.commit()


def process_entry(dirty_entry):
    """Inserts a question and its answers within an active database connection."""
    question_text = dirty_entry["question"]
    answers_list = dirty_entry["answers"]

    # Open connection for this specific write operation
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Insert question
        cursor.execute(
            "INSERT INTO questions (question_body) VALUES (?)",
            (question_text,)
        )
        q_id = cursor.lastrowid

        # 2. Batch insert answers
        answer_records = [
            (q_id, ans.get("answer"), ans.get("rarity_score"))
            for ans in answers_list
        ]
        
        if answer_records:
            cursor.executemany(
                "INSERT INTO answers (q_id, answer_body, rarity_score) VALUES (?, ?, ?)",
                answer_records
            )

        conn.commit()
        print(f"Successfully saved Question ID {q_id} with {len(answer_records)} answers.")

        # Print current tables for verification
        cursor.execute("SELECT * FROM questions")
        print("Questions:", cursor.fetchall())
        
        cursor.execute("SELECT * FROM answers")
        print("Answers:", cursor.fetchall())

def print_database_contents():
    """Prints all records currently stored in the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM questions")
        print("\n--- Questions ---")
        print(cursor.fetchall())

        cursor.execute("SELECT * FROM answers")
        print("\n--- Answers ---")
        print(cursor.fetchall())

def get_question_and_answers(q_id):
    """
    Fetches question text and answer list by q_id.
    Returns: (question_body_string, list_of_answers)
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Fetch Question string
        cursor.execute(
            "SELECT question_body FROM questions WHERE q_id = ?", 
            (q_id,)
        )
        q_row = cursor.fetchone()

        if not q_row:
            return None, []  # Return empty if question doesn't exist

        question_str = q_row[0]

        # 2. Fetch Answers list
        cursor.execute(
            """
            SELECT answer_body, rarity_score 
            FROM answers 
            WHERE q_id = ? 
            ORDER BY rarity_score DESC
            """, 
            (q_id,)
        )
        
        # Format as list of dicts: [{'answer': 'Yuzu', 'rarity_score': 100}, ...]
        answers_list = [
            {"answer": row[0], "rarity_score": row[1]} 
            for row in cursor.fetchall()
        ]

        return question_str, answers_list

# Ensure tables exist when module is imported
init_db()