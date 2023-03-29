import requests
from pprint import pprint

url = "https://imdb8.p.rapidapi.com/title/get-reviews"

querystring = {"tconst":"tt0944947","currentCountry":"US","purchaseCountry":"US"}

headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "411acad0f6msh89f79ce5b1dd281p15bca3jsn01460b677827"
        }

response = requests.request("GET", url, headers=headers, params=querystring)

pprint(response.text)