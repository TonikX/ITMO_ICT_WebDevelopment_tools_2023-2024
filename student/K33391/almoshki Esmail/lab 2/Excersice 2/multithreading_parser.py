from bs4 import BeautifulSoup
import requests
from time import time
from connection import get_engine 
import threading
import mysql.connector
from urls import urls


def parse_and_save(url: str):
    try:
        
        cnx = get_engine()
        cursor = cnx.cursor()
        
        
        r = requests.get(url, timeout=10)
        html = BeautifulSoup(r.text, features="html.parser")
        title = html.title.string if html.title else "No title"
        
        
        query = """INSERT INTO urls (title, url) VALUES (%s, %s)"""
        cursor.execute(query, (title, url))
        cnx.commit()
        
        print(f"Saved: {title} from {url}")

    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
    except mysql.connector.Error as db_err:
        print(f"Database error for {url}: {db_err}")
    finally:
        
        cursor.close()
        cnx.close()


def main():
    start_time = time()

    
    threads = []
    

    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    
    for thread in threads:
        thread.join()

    print(f"Total time taken: {time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
