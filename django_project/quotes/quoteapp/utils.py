import requests
from bs4 import BeautifulSoup
from .models import Author

def scrape_authors():
    url = "http://127.0.0.1:8000/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    authors_data = []


    for author_div in soup.find_all('div', class_='author'):
        name = author_div.find('h2').text
        biography = author_div.find('p', class_='biography').text
        authors_data.append({'name': name, 'biography': biography})


    for data in authors_data:
        if not Author.objects.filter(name=data['name']).exists():
            Author.objects.create(name=data['name'], biography=data['biography'])