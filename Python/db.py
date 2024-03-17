import urllib.request
import urllib.parse


def get_html():
    url = "http://16.171.31.115/bkup_db"
    values = {'city': 'Tel Aviv'}
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')  # Data should be bytes
    req = urllib.request.Request(url, data)

    with urllib.request.urlopen(req) as response:
        response_text = response.read().decode('utf-8')
        print(response_text)


get_html()
