import threading
import time

import httpx


from db import Session
from enums import ParseMethod
from models import Title


def parse_and_save(url: str) -> None:
    with httpx.Client() as client:
        response = client.get(url)

    title = response.text.split("<title>")[1].split("</title>")[0].strip()
    title_model = Title(parse_method=ParseMethod.THREADING, url=url, title=title)

    with Session() as session:
        session.add(title_model)
        session.commit()


def start_parsing() -> None:
    start_time = time.time()

    urls = [
        "https://student.itmo.ru/ru/repeat_interim_exams/",
        "https://student.itmo.ru/ru/expulsion_student_initiative/",
        "https://student.itmo.ru/ru/transfer/",
    ]

    threads = [threading.Thread(target=parse_and_save, args=(url,)) for url in urls]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Время: {time.time() - start_time}")


if __name__ == "__main__":
    start_parsing()