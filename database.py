
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('film_recommendations.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS recommendations (
                                    user_id INTEGER,
                                    recommendation TEXT
                                );''')

    def save_recommendation(self, user_id, recommendation):
        with self.conn:
            self.conn.execute("INSERT INTO recommendations (user_id, recommendation) VALUES (?, ?)", (user_id, recommendation))

    def get_recommendations(self, user_id):
        cursor = self.conn.execute("SELECT recommendation FROM recommendations WHERE user_id = ?", (user_id,))
        return [row[0] for row in cursor.fetchall()]
