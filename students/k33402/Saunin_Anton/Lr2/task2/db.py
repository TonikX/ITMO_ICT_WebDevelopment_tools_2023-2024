import asyncpg
import os

async def init_db():
    conn = await asyncpg.connect(os.getenv("DB_URL"))
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS site (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                process_type TEXT NOT NULL
            )
        ''')
    finally:
        await conn.close()