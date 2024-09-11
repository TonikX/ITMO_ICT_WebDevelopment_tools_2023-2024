import asyncpg
import psycopg2


async def async_get_connection():
    return await asyncpg.connect(
        host='localhost',
        port=1212,
        database="postgres",
        user="postgres",
        password="postgres",
    )


async def async_insert_data_to_project(data: list):
    connection = await async_get_connection()

    await connection.execute(
        """
        INSERT INTO "project"
            (title, description, is_active, start_date)
        VALUES 
            ($1, $2, $3, $4)
        """,
        *data
    )


def get_connection():
    return psycopg2.connect(
        host='localhost',
        port=1212,
        database="postgres",
        user="postgres",
        password="postgres",
    )


def insert_data_to_project(data: list):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO "project"
            (title, description, is_active, start_date)
        VALUES 
            (%s, %s, %s, %s)
        """,
        data
    )

    connection.commit()
    cursor.close()
