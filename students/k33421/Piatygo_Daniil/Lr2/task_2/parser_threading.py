from Lr2.mark_time import mark_time
from parser_naive import *
from threading import Thread


def create_participants(token, data, n_threads=5):
    def task(batch):
        for row in batch:
            create_participant(token, row)

    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    batch_size = len(data) // n_threads + (len(data) % n_threads > 0)
    batches = list(chunks(data, batch_size))

    threads = []
    for batch in batches:
        thread = Thread(target=task, args=(batch,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def add_participants_to_teams(
    token, data, team_mapping, participants_mapping, n_threads=5
):
    def task(batch):
        for row in batch:
            team_id = team_mapping[row["Команда"]]
            participant_id = participants_mapping[row["Никнейм"]]
            add_participant_to_team(token, team_id, participant_id)

    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    batch_size = len(data) // n_threads + (len(data) % n_threads > 0)
    batches = list(chunks(data, batch_size))

    threads = []
    for batch in batches:
        thread = Thread(target=task, args=(batch,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


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
