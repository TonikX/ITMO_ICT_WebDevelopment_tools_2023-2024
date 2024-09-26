import sqlite3


def create_database():
    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            balance TEXT
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
