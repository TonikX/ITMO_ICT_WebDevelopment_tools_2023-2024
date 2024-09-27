import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname='lab1',
        user='postgres',
        password='admin',
        host='localhost',
    )

def insert_data(url, title):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''INSERT INTO "site" ( url, title ) VALUES (%s, %s)
    ''', (url, title))
    conn.commit()
    cur.close()
    conn.close()
