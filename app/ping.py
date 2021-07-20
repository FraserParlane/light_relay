import requests


def make_request():
    url = 'http://192.168.86.30:5000/command'
    result = requests.post(
        url=url,
        data={'data': {'a': 'b'}}
    )


if __name__ == '__main__':
    make_request()
