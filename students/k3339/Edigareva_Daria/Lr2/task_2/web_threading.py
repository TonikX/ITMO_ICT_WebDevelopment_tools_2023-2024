import threading
import sqlite3
import requests
import time

URLS = [
    "https://httpbin.org",
    "https://www.python.org",
    "https://habr.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
]

results = []  # список (url, title)

def fetch_title(url: str):
    try:
        response = requests.get(url, timeout=5)
        html = response.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return
    title = "N/A"
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        title = html[start + len("<title>"):end].strip()
    results.append((url, title))
    print(f"[Thread] Fetched title for {url}")

if __name__ == "__main__":
    start_time = time.time()
    threads = []
    for url in URLS:
        t = threading.Thread(target=fetch_title, args=(url,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    conn = sqlite3.connect("pages.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pages (url TEXT, title TEXT)")
    cur.executemany("INSERT INTO pages (url, title) VALUES (?, ?)", results)
    conn.commit()
    conn.close()
    elapsed = time.time() - start_time
    print(f"Saved {len(results)} records to SQLite.")
    print(f"Completed in {elapsed:.2f} seconds")
