from fastapi import FastAPI
from celery.result import AsyncResult
from pydantic import BaseModel
from celery_config import celery_app
from celery import shared_task
import logging
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import random
import requests
from datetime import datetime


app = FastAPI()


class ParseRequest(BaseModel):
    url: str
    callback_url: str


@app.post("/parse/")
async def parse_url(request: ParseRequest):
    task = parse_url_task.delay(request.url, request.callback_url)
    return {"task_id": task.id}


@app.get("/result/{task_id}")
def get_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "SUCCESS":
        return {"status": result.state, "result": result.result}
    return {"status": result.state}


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

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_data(url):
    logging.info(f"Started scraping site {url}")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    driver.implicitly_wait(20)
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
                date = incident.find_element(By.CSS_SELECTOR, elements["date"]).text
                time_range = incident.find_element(
                    By.CSS_SELECTOR, elements["time_range"]
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
                    start_time, end_time = time_range.split("в")[-1].strip(), None
                else:
                    end_time = time_range.strip()
                end_time = end_time[:5].strip() if end_time else "00:00"
                year = "2024"
                formatted_date_time = f"{year}-{month}-{day} {end_time}:00.000"
                try:
                    deadline = datetime.strptime(
                        formatted_date_time, "%Y-%m-%d %H:%M:%S.%f"
                    )
                    formatted_date_time_str = deadline.strftime("%Y-%m-%d %H:%M:%S.%f")
                    logging.info(f"Converted date and time: {formatted_date_time}")
                except ValueError as e:
                    logging.error(
                        f"Error converting date and time: {formatted_date_time} - {e}"
                    )
                    continue
            else:
                deadline = incident.find_element(
                    By.CSS_SELECTOR, elements["deadline"]
                ).get_attribute("datetime")
                formatted_date_time_str = datetime.strptime(
                    deadline, "%Y-%m-%dT%H:%M:%S.%fZ"
                ).strftime("%Y-%m-%d %H:%M:%S.%f")
                logging.info(f"Found deadline: {deadline}")

            user_id = random.randint(1, 3)
            logging.info(f"Random user ID: {user_id}")
            try:
                data.append(
                    {
                        "title": title,
                        "description": description,
                        "priority": priority,
                        "deadline": formatted_date_time_str,
                        "user_id": user_id,
                        "status": status,
                    }
                )
                successful_additions += 1
                if successful_additions >= 5:
                    break
            except Exception as e:
                logging.error(f"Error processing incident: {e}")
        except Exception as e:
            logging.error(f"Error processing incident: {e}")

    driver.quit()
    return data


@shared_task
def parse_url_task(url, callback_url):
    logging.info(f"Starting task for URL: {url}")
    data = parse_data(url)
    response = requests.post(callback_url, json=data)
    if response.status_code != 200:
        logging.error(f"Failed to send data to callback URL: {callback_url}")
        return f"Failed to send data to callback URL: {callback_url}"
    logging.info(f"Task completed for URL: {url}")
    return "Parsing completed"
