import requests
domain = 'www.google.com'
url = 'https://whoisjsonapi.com/v1/'+domain
headers = {
    'Authorization': 'Bearer TvL6oFeiLyV2cmRlvg8NTbAGUC2G0F34ns2NuGLHkmv8Li8vIs6yDz6dqxRHYxf'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print(e)
