import requests


def get_content(url, params=None):
    print(requests.get(url, params=params).url)
    response = requests.get(url, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(url)
        print(f"Http статус: {response.status_code} ('{response.reason}')")
        exit()
    return response
