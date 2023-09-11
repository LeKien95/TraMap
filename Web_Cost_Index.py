
# beautifulsoup4 Version: 4.11.1
# NÃ¤here Infos unter: https://www.freecodecamp.org/news/how-to-scrape-websites-with-python-2/

import requests #Allows to send HTTP requests using Python. The HTTP request returns a Response Object with all the response data (content, encoding, status, etc).
from bs4 import BeautifulSoup #Beautiful Soup is a Python library that is used for web scraping purposes to pull the data out of HTML and XML files
import pandas as pd #Library für Datenmanagement (DataFrames)

#location = str(input("Wo wohnst du?\n"))

page = requests.get('https://de.numbeo.com/lebenshaltungskosten/aktuelles-ranking') # Getting page HTML through request
soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup; Parsing: Code wird analysiert und in geeignetes Format umgewandelt

#Solution under: https://www.youtube.com/watch?v=G8ZJwhOsmTw&ab_channel=Learnerea

#Tabelle wird aus HTML-Code genommen
table = soup.find("table", {"id": "t2"})

#Alle Überschriften werden in einer Series gespeichert
headers = []
for x in table.find_all("th"):
    headers.append(x.text)

#Alle Tabellenelemente werden in ein Dataframe gespeichert
values = []
#Es wird durch alle tabellenzeilen iterriert
for x in table.find_all("tr")[1:]: #außer erste zeiler, da header
    td_tags = x.find_all("td")
    td_val = [y.text for y in td_tags]
    values.append(td_val)

#Aus den Daten und Überschriften wird ein DataFrame erstellt
data = pd.DataFrame(values, columns = headers)
del data["Platz"] #Platz/Ranking Spalte wird gelöscht

#Spalte Stadt wird bereinigt, nur erstes Wort bleibt (ohne Land dahinter)
data['Stadt'] = data['Stadt'].str.split(',').str[0]
data['Stadt'] = data['Stadt'].str.split('(').str[0]
data['Stadt'] = data['Stadt'].str.strip()
#Werte werden auf umwandlung zu float vorbereitet
data = data.replace(',','.', regex=True)
#alle Werte ab Spalte 2 werden in floats umgewandelt
data_tofloat = data.iloc[: , 1:].astype(float)

#Fertiges DataFrame mit Werte als float soll wieder erstellt werden
data = data["Stadt"]
data = pd.concat([data, data_tofloat], axis=1)



# search for solution on https://www.crummy.com/software/BeautifulSoup/bs4/doc/

#Funktioniert
# city = soup.find("td", class_="cityOrCountryInIndicesTable")

#Weitere Suche nach > div id="page_container" ergibt nur leere Rückgabe
#val = soup.select("body > div.innerWidth")

# Ausgabe = None
# val = soup.find("div", {"id": "t2_wrapper"})

#Funktioniert nicht und gibt leeren Wert aus. Warum funktioniert hier nicht, aber für "cityOrCountryInIndicesTable"?
#val = soup.find("td", class_= "sorting_1")

#Funktioniert nicht mit CSS selector
#val = soup.find("t2 > tbody > tr:nth-child(1) > td.sorting_1")

#Funktioniert nicht
# val = soup.find("td", attrs={"class": "sorting_1"})

#Funktioniert nicht
# val = soup.find_all(lambda tag: tag.name=="td" and
# 			tag.get("style")=="text-align: right" and 
# 			tag.get("class") == "sorting_1")

#Nimmt das erste td und den Inhalt davon
#val = soup.body.td





