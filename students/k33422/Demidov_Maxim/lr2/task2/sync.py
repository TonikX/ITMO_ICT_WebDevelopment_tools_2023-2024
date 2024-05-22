import threading

from task2.handlers import (parse_and_save_tasks,
                            parse_and_save_projects,
                            parse_and_save_users,
                            parse_and_save_products,
                            parse_and_save_teams,
                            parse_and_save_carts,
                            parse_and_save_userprofiles,
                            parse_all_urls,
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
