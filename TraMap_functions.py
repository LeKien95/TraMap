import pandas as pd
import geopandas # geopandas Version 0.12.2
from shapely.geometry import Point, Polygon
import requests #Allows to send HTTP requests using Python. The HTTP request returns a Response Object with all the response data (content, encoding, status, etc).
from bs4 import BeautifulSoup #beautifulsoup4 Version: 4.11.1 #Beautiful Soup is a Python library that is used for web scraping purposes to pull the data out of HTML and XML files
import webbrowser
import os
import folium # folium Version: 0.14.0


def set_up_map_and_data():
    
    '''
    Set up map and locations from csv files
    '''
    
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres')) #get map layout
    world = world.drop(columns=['pop_est', "iso_a3", "gdp_md_est"]) # delete unwanted data
    
    cities = pd.read_csv("input\Städte.csv", sep=',', encoding= 'unicode_escape') # read out my city data saved as csv
    cities["geometry"] = geopandas.GeoSeries.from_wkt(cities["geometry"]) # make DataFrame to GeoDataFrame by adding geometry column at the end
    
    regions = pd.read_csv("input\Regionen.csv", sep=',', encoding= 'unicode_escape') # read out data for regions
    regions = regions.astype({'Latitude':'float','Longitude':'float'}) # change data type of columns
    regions['geometry'] = regions.apply(lambda row: Point(row.Latitude, row.Longitude), axis=1) # combine longitude and latitude into one value
    regions.columns.values[0] = "Land"
    
    regions_clean = regions.drop(['Latitude', 'Longitude', "geometry"], axis=1) # delete unwanted columns to put in data the right way
    regions_clean["geometry"] = ""
    
    for name, group in regions.groupby('Stadt/Region'): # loop to iterrate through regions
        if len(group)> 1:
            for row_index, row in group.iterrows():
                regions_clean.loc[row_index, "geometry"] = Polygon(zip(group.Latitude,group.Longitude)) # regions with same name are grouped into one row element and their geometry data is zipped into the format for POLYGON forms in geopandas
    
    locations = pd.concat([regions_clean, cities], ignore_index=True, sort=False) # combine both DataFrames horizontally
    locations = locations.drop_duplicates(subset='Stadt/Region', keep="first")
    locations  = geopandas.GeoDataFrame(locations) # change all data into GeoDataFrame
    return locations, world


def get_numbeo_data():

    '''
    Webscrape cost data from numbeo
    '''
    
    page = requests.get('https://de.numbeo.com/lebenshaltungskosten/aktuelles-ranking') # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup; Parsing: Code wird analysiert und in geeignetes Format umgewandelt
    
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
    
    return data

def merge_data(master, data):
    
    '''
    Merge data
    '''
    
    # Spalten leere, da hier Daten von numbeo oder Abfrage rein sollen
    master['Kosten Food'] = 0
    master['Kosten Leben'] = 0
    master['Interesse'] = 0
    master['Score'] = 0

    for  index, row in master.iterrows():
        y = master.at[index, "Stadt/Region"]
        print(f"Put in your interest for location: {y}. (Score 1 to 10) ")
        x = input()
        master.at[index,'Interesse'] = float(x)

    data = data.set_index("Stadt")
    master = master.set_index("Stadt/Region")

    for index, row in master.iterrows(): # Füge die Spaltenwerte aus data in die entsprechenden Stellen in master ein
        try:
            master.at[index,'Kosten Food'] = data.loc[index, "Lebensmittel-Index"]
            master.at[index,'Kosten Leben'] = data.loc[index, "Lebenshaltungskosten-Index"]
        except(KeyError):
            pass

    for index, row in master.iterrows(): # Berechne einen Score
        if (row['Interesse'] != 0 and row["Kosten Food"] != 0 and row["Kosten Leben"] != 0):
           master.at[index,'Score'] = round(row['Interesse']/10*1/(row["Kosten Food"] + row["Kosten Leben"])*10000,2)
        else:
           master.at[index,'Score'] = 0


    #next up
    #1. Anhand meiner Interesseeingabe neuen Score berechnen und plotten DONE
    #2. Fragebogen für Interesse erstellen
    #3. Datensatz zu bisherigen Städten verbessern
    
    return master

def draw_map(world, master):
    
    '''
    Draw map in HTML
    '''
    
    m = world.explore(
         #column="name",  # make choropleth based on "BoroName" column
         #scheme="naturalbreaks",  # use mapclassify's natural breaks scheme
         #legend=True, # show legend
         #k=10, # use 10 bins
         #legend_kwds=dict(colorbar=False), # do not use colorbar
         color = "#BCC6CC"
         #name="Länder" # name of the layer in the map
    ) 
    
    master.explore(
         m=m, # pass the map object
         #color="blue", # use red color on all points
         column="Score",  # make choropleth based on "BoroName" column
         marker_kwds=dict(radius=3, fill=True), # make marker radius 10px with fill
         cmap='RdPu', # Ändert colorcode von Heatmap
         tooltip=True, # show "name" column in the tooltip/wenn True, dann werde alle Spalten angezeigt
         legend = True,
         vmin = 0,
         vmax = 100,
         #tooltip_kwds=dict(labels=False), # do not show column label in the tooltip
         name="Städte/Regionen" # name of the layer in the map
    )
    
    folium.TileLayer('Stamen Toner', control=True).add_to(m)  # use folium to add alternative tiles
    folium.LayerControl().add_to(m)  # use folium to add layer control
    
    m  # show map
    # and then we write the map to disk
    m.save('TraMap.html')
    
    # then open it
    webbrowser.open('file://' + os.path.realpath('TraMap.html'))
