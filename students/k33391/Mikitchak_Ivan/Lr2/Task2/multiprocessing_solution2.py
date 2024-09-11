import multiprocessing
import requests
import psycopg2
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import time

# URL for fetching generated user data
URL = "https://randomuser.me/api/?format=json"

# Utility for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

log_lock = multiprocessing.Lock()

def log(msg):
    """Logs a message to the console in a thread-safe manner.

    Args:
        msg: The message to be printed to the console.
    """
    with log_lock:
        print(msg)

def hash_password(password: str) -> str:
    """Hashes a given password using bcrypt.

    Args:
        password: The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def fetch_data(session):
    """Fetches random user data from a public API using the provided session.

    Args:
        session: A requests.Session object used to make the HTTP request.

    Returns:
        dict: The fetched user data as a dictionary, or None if an error occurs.

    Raises:
        Exception: If an error occurs while fetching or decoding the response.
    """
    try:
        response = session.get(URL)
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except Exception as e:
                print(f"An error occurred while decoding JSON: {e}")
                return None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def extract_user(data):
    """Extracts user information from the API response data.

    Args:
        data: A dictionary containing user data fetched from the API.

    Returns:
        dict: A dictionary containing extracted user information (email, hashed password, first name, last name), or None if an error occurs.

    Raises:
        Exception: If an error occurs while extracting user information.
    """
    try:
        user = {
            "email": data["results"][0]["email"],
            "hashed_password": hash_password(data["results"][0]["login"]["password"]),
            "first_name": data["results"][0]["name"]["first"],
            "last_name": data["results"][0]["name"]["last"]
        }
        return user
    except Exception as e:
        print(f"An error occurred while extracting user: {e}")
        return None

def store_user(user):
    """Stores user data into the PostgreSQL database.

    Args:
        user: A dictionary containing user information to be stored in the database.

    Raises:
        Exception: If an error occurs while connecting to the database or storing user data.
    """
    try:
        with psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME2"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO app_user (email, hashed_password, first_name, last_name) VALUES (%s, %s, %s, %s)",
                    (user["email"], user["hashed_password"], user["first_name"], user["last_name"])
                )
                conn.commit()
    except Exception as e:
        print(f"An error occurred while storing user: {e}")

def parse_and_save(session):
    """Fetches user data, extracts the user information, and stores it in the database.

    Args:
        session: A requests.Session object used to make the HTTP request.
    """
    data = fetch_data(session)
    if data is None:
        return
    user = extract_user(data)
    if user is None:
        return
    store_user(user)
    log(user)

def main():
    """Main function that initializes environment variables and starts multiple processes to fetch and store user data concurrently."""
    load_dotenv()

    n_tasks = 4
    with requests.Session() as session:
        processes = []
        for _ in range(n_tasks):
            process = multiprocessing.Process(target=parse_and_save, args=(session,))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

if __name__ == "__main__":
    start = time.time()
    main()
    finish = time.time()
    print(f"Time: {finish - start}")
