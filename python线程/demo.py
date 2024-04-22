import requests


def test():
    url = r"http://127.0.0.1:5000/"
    headers = {'Content-Type': 'text/event-stream'}
    response = requests.get(url, headers=headers, stream=True)
    for chunk in response.iter_content():
        print(chunk)


if __name__ == '__main__':
    test()