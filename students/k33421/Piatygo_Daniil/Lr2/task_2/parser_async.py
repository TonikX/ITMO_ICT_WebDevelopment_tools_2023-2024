import aiohttp
import asyncio
from parser_naive import *
from Lr2.mark_time import mark_time


async def create_participant(session, token, participant):
    url = "http://localhost:8000/participants/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = parse_participant(participant)
    async with session.post(url, json=data, headers=headers) as response:
        return await response.json(), response.status


async def create_participants(token, data):
    async with aiohttp.ClientSession() as session:
        tasks = [
            create_participant(session, token, participant) for participant in data
        ]
        await asyncio.gather(*tasks)


async def add_participant_to_team(session, token, team_id, participant_id):
    url = f"http://localhost:8000/teams/{team_id}/participants/"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"participant_id": participant_id}
    async with session.patch(url, params=params, headers=headers) as response:
        return await response.json(), response.status


async def add_participants_to_teams(token, data, team_mapping, participants_mapping):
    async with aiohttp.ClientSession() as session:
        tasks = [
            add_participant_to_team(
                session,
                token,
                team_mapping[row["Команда"]],
                participants_mapping[row["Никнейм"]],
            )
            for row in data
        ]
        await asyncio.gather(*tasks)


async def parse_and_save():
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

    await create_participants(token, data)

    participants = get_participants(token)
    participants_mapping = {
        participant["nickname"]: participant["id"] for participant in participants
    }

    await add_participants_to_teams(token, data, team_mapping, participants_mapping)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(parse_and_save())
    print(f"Общее время выполнения: {time.time() - start_time} секунд.")
