import requests


def test_parse(key: str):
    endpoint = "http://127.0.0.1:8000/parse_async"
    headers = {'accept': 'application/json'}
    data = {"key": key}
    response = requests.post(endpoint, headers=headers, params=data)
    return response.json()


if __name__ == '__main__':
    keys = ["planes", "cruises", "trains", "airbnb", "hotels", "hostels"]
    for k in keys:
        print(test_parse(k))