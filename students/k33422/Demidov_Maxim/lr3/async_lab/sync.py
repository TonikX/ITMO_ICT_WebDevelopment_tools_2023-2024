from handlers import (parse_all_urls,
                      data_handlers)


def main():
    # Создаем потоки для обработки каждого URL
    threads = []
    for category, handler_func in data_handlers.items():
        parse_all_urls(handler_func, f"https://async-lab.tiiny.site/{category}", 5)


if __name__ == "__main__":
    import time

    start_time = time.time()
    main()
    print("Execution time:", time.time() - start_time)
