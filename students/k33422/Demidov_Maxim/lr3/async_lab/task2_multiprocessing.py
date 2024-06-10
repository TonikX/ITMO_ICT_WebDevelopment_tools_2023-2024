import multiprocessing
from handlers import parse_all_urls, data_handlers

def parse_and_save():
    # Создаем процессы для обработки каждого URL
    processes = []
    for category, handler_func in data_handlers.items():
        url = f"https://async-lab.tiiny.site/{category}"
        print(url)
        process = multiprocessing.Process(target=parse_all_urls, args=(handler_func, url, 5))
        processes.append(process)
        process.start()

    # Ждем завершения всех процессов
    for process in processes:
        process.join()

if __name__ == "__main__":
    import time

    start_time = time.time()
    parse_and_save()
    print("Execution time:", time.time() - start_time)
