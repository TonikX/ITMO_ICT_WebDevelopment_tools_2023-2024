import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname='web_data',
        user='postgres',
        password='Bakugan102!',
        host='localhost',
        port='5432'
    )

def insert_data(url, title):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''INSERT INTO "site" ( url, title ) VALUES (%s, %s)
    ''', (url, title))
    conn.commit()
    cur.close()
    conn.close()
