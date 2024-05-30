import datetime
import json
import multiprocessing
import time

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.expanduser('~/Desktop/ITMO_ICT_WebDevelopment_tools_2023-2024/students/k33421/aleksei_bezgin/lab1/hack_lab/app/db'))
sys.path.append(os.path.expanduser('~/Desktop/ITMO_ICT_WebDevelopment_tools_2023-2024/students/k33421/aleksei_bezgin/lab1/hack_lab/app'))

from connection import engine
from models import Hackathon, Task



def add_hackathon(hack_info):
    hack_name, hack_link = hack_info['name'], hack_info['link']
    # спарсили данные про кейс
    inner_page = requests.get(hack_link)
    soup_in = BeautifulSoup(inner_page.text, 'html.parser')
    paragraphs = list(map(lambda x: x.text, soup_in.find_all('p')))
    hack_case = '\n'.join(paragraphs)
    case_title = paragraphs[0]

    with Session(engine) as session:
        hackathon = Hackathon(
            name=hack_name,
            start_date=datetime.datetime.now(),
            # пусть все хакатоны длятся неделю
            end_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        session.add(hackathon)
        session.commit()
        session.refresh(hackathon)

        task = Task(
            title=case_title,
            description=hack_case,
            requirements="Be cool",
            evaluation_criteria="Accuracy",
            hackathon_id=hackathon.id  # Assign the hackathon_id to establish the relationship
        )
        session.add(task)
        session.commit()
        session.refresh(task)


def add_hackathon_list(hack_info_list):
    for hack_info in hack_info_list:
        add_hackathon(hack_info)


def main():
    hack_data = json.load(open('hack_links.json'))

    # используем несколько потоков
    num_threads = 5
    step = len(hack_data) // num_threads
    processes = []

    time_start = time.time()
    for i in range(num_threads):
        process = multiprocessing.Process(target=add_hackathon_list, args=(hack_data[i * step: (i + 1) * step], ))
        process.start()
        processes.append(process)

    for p in processes:
        p.join()

    print(f'scraped info about {len(hack_data)} events')
    print(f'done in {time.time() - time_start} seconds')

if __name__ == "__main__":
    main()