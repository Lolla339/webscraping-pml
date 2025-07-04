import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
from urllib.parse import urljoin





base_url = "https://realpython.com/tutorials/"
max_pages = 3

h2_titles = []
a_titles = []
links = []
###############################################################################


# Завантаження і парсинг сторінок
for page_num in range(1, max_pages + 1):
    if page_num == 1:
        url = base_url
    else:
        url = f"{base_url}page/{page_num}/"
    response = requests.get(url)
    if response.status_code != 200:
        break
    soup = BeautifulSoup(response.text, "html.parser")
    


###############################################################################

    for tag in soup.find_all(["h2", "a"]):
        text = tag.get_text(strip=True)
        if text:
            if tag.name == "h2":
                h2_titles.append(text)
            elif tag.name == "a":
                a_titles.append(text)
        if tag.name == "a" and tag.has_attr("href"):
            links.append(urljoin(base_url, tag["href"]))




###############################################################################

with open("titel.txt", "w", encoding="utf-8") as file:
    for title in h2_titles + a_titles:
        file.write(title + "\n")


###############################################################################

# У csv файл

with open('webscrape.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['h2', 'a'])
    for h2, a in zip_longest(h2_titles, a_titles, fillvalue=""):
        csv_writer.writerow([h2, a])


# посиланя
with open("links.txt", "w", encoding="utf-8") as file:
    for link in links:
        file.write(link + "\n")



# Пошук ключових слів
schlagwoerter = ["KI", "Python", "Technologie"]
gefundene_schlagwoerter = []

for title in h2_titles + a_titles:
    for wort in schlagwoerter:
        if wort.lower() in title.lower():
            gefundene_schlagwoerter.append((wort, title))


# Вивід
for wort, title in gefundene_schlagwoerter:
    print(f"{wort} знайдено у: {title}")
