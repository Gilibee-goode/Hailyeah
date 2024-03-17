import requests


def test_access_localhost():
    response = requests.get("http://localhost:80")
    # Assert that the status code is in the 2xx range
    assert 200 <= response.status_code < 300, f"Expected a 2xx status, got {response.status_code}"
