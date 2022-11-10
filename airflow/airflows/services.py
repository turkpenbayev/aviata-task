import requests


def make_request(url: str):
    with requests.Session() as session:
        try:
            response = session.post(url=url, timeout=100)
            if response.status_code == 404:
                return None
            response.raise_for_status()
        except requests.RequestException as e:
            raise e

        return response.json()