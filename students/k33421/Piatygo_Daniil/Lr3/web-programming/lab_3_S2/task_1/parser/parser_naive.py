import time

import gspread
from google.oauth2.service_account import Credentials
import requests


def init_google_sheet(url, creds_path="creds.json"):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(url)
    return sh


def get_token(username="dptgo", password="iloveweb"):
    url = "http://web:8000/token/"
    response = requests.post(url, data={"username": username, "password": password})
    return response.json()["access_token"]


def get_teams(token):
    url = "http://web:8000/teams/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def get_participants(token):
    url = "http://web:8000/participants/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def create_team(token, team_name):
    url = "http://web:8000/teams/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"name": team_name, "approve_status": "Gathering"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print("Failed to create team:", response.status_code, response.json())
    return response.json()


def parse_participant(row):
    return {
        "full_name": row["ФИО"],
        "nickname": row["Никнейм"],
        "email": row["E-mail"],
        "phone": "+" + str(row["Номер телефона"]),
        "skill": row["Отметьте ваш главный навык"],
    }


def create_participant(token, participant):
    url = "http://web:8000/participants/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = parse_participant(participant)
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print("Failed to create participant:", response.status_code, response.json())
    return response.json()


def add_participant_to_team(token, team_id, participant_id):
    url = f"http://web:8000/teams/{team_id}/participants/"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"participant_id": participant_id}
    response = requests.patch(url, params=params, headers=headers)
    if response.status_code != 200:
        print(
            "Failed adding participant to team:", response.status_code, response.json()
        )
    return response.json()


if __name__ == "__main__":
    start_time = time.time()

    url = "https://docs.google.com/spreadsheets/d/1mQN3GROxytwL-8Y_Hi9Gxrf3XeP9Kqe7SzII6SajWSo"
    sh = init_google_sheet(url)
    worksheet = sh.sheet1
    data = worksheet.get_all_records()

    token = get_token()
    existing_teams = get_teams(token)
    team_names = set(row["Команда"] for row in data if row["Команда"])
    for team_name in team_names:
        if team_name not in [team["name"] for team in existing_teams]:
            create_team(token, team_name)

    teams = get_teams(token)
    team_mapping = {team["name"]: team["id"] for team in teams}

    for row in data:
        create_participant(token, row)

    participants = get_participants(token)
    participants_mapping = {
        participant["nickname"]: participant["id"] for participant in participants
    }
    for row in data:
        if row["Команда"]:
            add_participant_to_team(
                token,
                team_mapping[row["Команда"]],
                participants_mapping[row["Никнейм"]],
            )

    print(f"Общее время выполнения: {time.time() - start_time} секунд.")
