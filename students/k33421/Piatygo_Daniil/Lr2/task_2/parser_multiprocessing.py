from Lr2.mark_time import mark_time
from parser_naive import *
import multiprocessing


def process_participants(token, batch):
    for row in batch:
        create_participant(token, row)


def create_participants(token, data, n_processes=5):
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    batch_size = len(data) // n_processes + (len(data) % n_processes > 0)
    batches = list(chunks(data, batch_size))

    with multiprocessing.Pool(n_processes) as pool:
        pool.starmap(process_participants, [(token, batch) for batch in batches])


def process_teams(token, batch, team_mapping, participants_mapping):
    for row in batch:
        team_id = team_mapping[row["Команда"]]
        participant_id = participants_mapping[row["Никнейм"]]
        add_participant_to_team(token, team_id, participant_id)


def add_participants_to_teams(
    token, data, team_mapping, participants_mapping, n_processes=5
):
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    batch_size = len(data) // n_processes + (len(data) % n_processes > 0)
    batches = list(chunks(data, batch_size))

    with multiprocessing.Pool(n_processes) as pool:
        pool.starmap(
            process_teams,
            [(token, batch, team_mapping, participants_mapping) for batch in batches],
        )


@mark_time
def parse_and_save():
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

    create_participants(token, data)

    participants = get_participants(token)
    participants_mapping = {
        participant["nickname"]: participant["id"] for participant in participants
    }

    add_participants_to_teams(token, data, team_mapping, participants_mapping)


if __name__ == "__main__":
    parse_and_save()
