import multiprocessing
from datetime import datetime
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import random
import logging
import psycopg2

css_elements = {
    "https://status.msk.cloud.vk.com/incidents": {
        "incident_container": ".Incident_main__3YJVa",
        "title": ".Incident_title__ypk3E",
        "description": ".Incident_reactMarkdown__2t1b9",
        "status": ".Incident_label__BSSWu",
        "date": ".Incident_date__lqPM_",
        "time_range": ".Incident_humanizedTime__3gxDb",
    },
    "https://status.yandex.cloud/ru/timeline": {
        "incident_container": ".mc-incident-item__container",
        "title": ".mc-incident-item__title",
        "description": ".mc-incident-comment__content",
        "status": ".mc-incident-comment__type",
        "deadline": ".mc-incident-date__date",
    },
}

host = "localhost"
database = "web"
username = "postgres"
password = "2512"
port = 5432

conn = psycopg2.connect(
    host=host, database=database, user=username, password=password, port=port
)

cur = conn.cursor()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_data(url):
    logging.info(f"Started scraping site {url}")
    s = Service(
        "C:\\Users\\a.makunina\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    )
    driver = webdriver.Chrome(service=s)

    driver.get(url)
    driver.implicitly_wait(10)
    elements = css_elements[url]

    incidents = driver.find_elements(By.CSS_SELECTOR, elements["incident_container"])

    data = []
    successful_additions = 0

    if not incidents:
        logging.info("No incidents found on the page.")

    for incident in incidents:
        try:
            title = incident.find_element(By.CSS_SELECTOR, elements["title"]).text
            logging.info(f"Found title: {title}")

            try:
                description_tag = incident.find_element(
                    By.CSS_SELECTOR, elements["description"]
                )
                description = description_tag.text
            except NoSuchElementException:
                description = "Description not found"

            logging.info(f"Found description: {description[:30]}...")

            status_tag = incident.find_element(By.CSS_SELECTOR, elements["status"])
            status = status_tag.text.strip() if status_tag else ""
            priority = "LOW" if status == "Resolved" else "HIGH"
            status = "COMPLETED"

            logging.info(f"Found status: {status}, priority: {priority}")

            if url == "https://status.msk.cloud.vk.com/incidents":
                date = incident.find_element(
                    By.CSS_SELECTOR, ".Incident_date__lqPM_"
                ).text
                time_range = incident.find_element(
                    By.CSS_SELECTOR, ".Incident_humanizedTime__3gxDb"
                ).text

                months_mapping = {
                    "января": "01",
                    "февраля": "02",
                    "марта": "03",
                    "апреля": "04",
                    "мая": "05",
                    "июня": "06",
                    "июля": "07",
                    "августа": "08",
                    "сентября": "09",
                    "октября": "10",
                    "ноября": "11",
                    "декабря": "12",
                }

                date_parts = date.split()
                day = date_parts[0]
                month = months_mapping[date_parts[1]]
                if "в" in time_range:
                    start_time, end_time = time_range.split("в")
                    end_time = end_time.strip()
                else:
                    end_time = time_range.strip()
                end_time = end_time[:5].strip()
                year = "2024"
                formatted_date_time = f"{year}-{month}-{day} {end_time}:00.000"
                deadline = datetime.strptime(
                    formatted_date_time, "%Y-%m-%d %H:%M:%S.%f"
                )
                logging.info(f"Converted date and time: {formatted_date_time}")
            else:
                deadline = incident.find_element(
                    By.CSS_SELECTOR, elements["deadline"]
                ).get_attribute("datetime")
                logging.info(f"Found deadline: {deadline}")

            user_id = random.randint(1, 3)
            logging.info(f"Random user ID: {user_id}")
            try:
                data.append(
                    {
                        "title": title,
                        "description": description,
                        "priority": priority,
                        "deadline": deadline,
                        "user_id": user_id,
                        "status": status,
                    }
                )
                successful_additions += 1
                if successful_additions >= 10:
                    break
            except Exception as e:
                logging.error(f"Error processing incident: {e}")
        except Exception as e:
            logging.error(f"Error processing incident: {e}")

    try:
        for row in data:
            logging.info(f"Processing {row}")
            cur.execute(
                """
                INSERT INTO task (title, description, priority, deadline, user_id, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
            """,
                (
                    row["title"],
                    row["description"],
                    row["priority"],
                    row["deadline"],
                    row["user_id"],
                    row["status"],
                ),
            )
        conn.commit()
        logging.info(f"Record inserted.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting data into database: {e}")

    driver.quit()


urls = [
    "https://status.msk.cloud.vk.com/incidents",
    "https://status.yandex.cloud/ru/timeline",
]


def parse_data_in_parallel(urls):
    with multiprocessing.Pool(processes=2) as pool:
        pool.map(parse_data, urls)


if __name__ == "__main__":
    start_time = datetime.now()
    parse_data_in_parallel(urls)
    end_time = datetime.now()
    logging.info(f"All URLs parsed in {end_time - start_time}")
