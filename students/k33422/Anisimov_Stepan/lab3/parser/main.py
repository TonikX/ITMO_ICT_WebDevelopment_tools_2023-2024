from fastapi import FastAPI
import requests


parser = FastAPI()

@parser.get("/parse")
def parse(url: str):
    with requests.Session() as session:
        response = session.get(url=url, headers={'User-Agent': 'Mozilla/129.0.2'}).json()

    hackathons = []

    for post in response['posts']:
        hackathon = {}

        title = post['title']
        descr = post['descr'].replace("<br />", "").replace("&nbsp;", " ")

        hackathon['name'] = title
        hackathon['description'] = descr

        hackathons.append(hackathon)
    
    return hackathons