import multiprocessing as mp
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

def fetch_title(url: str) -> tuple:
    try:
        resp = requests.get(url, timeout=5)
        html = resp.text
    except Exception as e:
        print(f"Process: failed to fetch {url}: {e}")
        return url, "ERROR"

    title = "N/A"
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        title = html[start + len("<title>"):end].strip()

    print(f"[Process] Fetched title for {url}")
    return url, title

if __name__ == "__main__":
    start_time = time.time()
    with mp.Pool(processes=len(URLS)) as pool:
        results = pool.map(fetch_title, URLS)

    conn = sqlite3.connect("pages.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pages (url TEXT, title TEXT)")
    cur.executemany("INSERT INTO pages (url, title) VALUES (?, ?)", results)
    conn.commit()
    conn.close()
    elapsed = time.time() - start_time
    print(f"Saved {len(results)} records to SQLite.")
    print(f"Completed in {elapsed:.2f} seconds")
