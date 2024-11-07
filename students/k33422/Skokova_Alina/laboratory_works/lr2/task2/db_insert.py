import psycopg2
from config import load_config
import bcrypt
from datetime import datetime

def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_pwd.decode('utf-8')

def insert_data(new_data):
    config = load_config()
    for entry in new_data:
        print(f'{entry} is processing')
        new_username, new_email, new_password, new_library_name, new_book_name, new_book_author, new_book_condition = entry
        pass_hashed = hash_password(new_password)
        sql_user = f"""INSERT INTO public."user" (username, email, password, created_at)
                    VALUES ('{new_username}', '{new_email}', '{pass_hashed}', '{datetime.now()}') RETURNING user_id;"""
        try:
            with  psycopg2.connect(**config) as conn:
                with  conn.cursor() as cur:
                    cur.execute(sql_user) 
                    # get the generated id back
                    rows = cur.fetchone() 
                    if rows:
                        new_user_id = rows[0]
                    print('Added new row to User table')

                    sql_lib = f"""INSERT INTO public.library (user_id, library_name) 
                    VALUES ('{new_user_id}', '{new_library_name}') RETURNING library_id;"""
                    cur.execute(sql_lib)
                    rows = cur.fetchone()
                    if rows:
                        new_library_id = rows[0]
                    print('Added new row to Library table')

                    sql_book = f"""INSERT INTO public.book (book_name, book_author, book_condition, library_id) 
                    VALUES ('{new_book_name}', '{new_book_author}', '{new_book_condition}', '{new_library_id}') RETURNING book_id;"""
                    cur.execute(sql_book)
                    print('Added new row to Book table')
                    conn.commit() # commit the changes to the database
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# if __name__ == '__main__':
#     data = [
#         ('user9', 'user9@example.com', 'password9', 'library9', 'book3', 'author3', 'excellent'),
#         ('user8', 'user8@example.com', 'password8', 'library8', 'book2', 'author2', 'excellent')
#     ]
#     insert_data(data)
