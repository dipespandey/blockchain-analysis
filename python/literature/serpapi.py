import requests

private_key = ''
url = f'https://serpapi.com/search.json?engine=google_scholar&q=biology&api_key={private_key}'


output = requests.get(url).json()
