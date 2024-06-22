import subprocess
import pandas as pd
import sys

def run_program(command, urls):
    try:
        result = subprocess.run(command + urls, capture_output=True, text=True, check=True)
        output = result.stdout.strip().split("\n")
        print(f"{command}: {result.stdout}")
        if "занял" not in output[-1]:
            print(f"Ошибка: {result.stdout}")
            return None
        time_taken = float(output[-1].split(": ")[1].split(" ")[0])
        return time_taken
    except subprocess.CalledProcessError as e:
        print(f"Ошибка запуска команды: {command}: {e.stderr}")
        return None

def main(urls):
    methods = {
        "Threading": ["python3", "threadingCode.py"],
        "Multiprocessing": ["python3", "multiprocessingCode.py"],
        "Async/await": ["python3", "asyncCode.py"]
    }
    
    results = []
    
    for method, command in methods.items():
        time_taken = run_program(command, urls)
        if time_taken is not None:
            results.append([method, time_taken])
    
    df = pd.DataFrame(results, columns=["Method", "Time Taken (s)"])
    print(df)

if __name__ == "__main__":
    urls = sys.argv[1:]  # Список URL для парсинга
    if not urls:
        urls = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.youtube.com",
    "https://www.amazon.com",
    "https://www.wikipedia.org",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.netflix.com",
    "https://www.github.com"
        ]
        print("Выбран дефолтный набор URL", urls)
    main(urls)