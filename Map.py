# geopandas Version 0.12.2

import pandas as pd
import geopandas
from shapely.geometry import Point, Polygon

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres')) #get map layout
world = world.drop(columns=['pop_est', "iso_a3", "gdp_md_est"]) # delete unwanted data

cities = pd.read_csv("Städte.csv", sep=',', encoding= 'unicode_escape') # read out my city data saved as csv
cities["geometry"] = geopandas.GeoSeries.from_wkt(cities["geometry"]) # make DataFrame to GeoDataFrame by adding geometry column at the end

regions = pd.read_csv("Regionen.csv", sep=',', encoding= 'unicode_escape') # read out data for regions
regions = regions.astype({'Latitude':'float','Longitude':'float'}) # change data type of columns
regions['geometry'] = regions.apply(lambda row: Point(row.Latitude, row.Longitude), axis=1) # combine longitude and latitude into one value
regions.columns.values[0] = "Land"

regions_clean = regions.drop(['Latitude', 'Longitude', "geometry"], axis=1) # delete unwanted columns to put in data the right way
regions_clean["geometry"] = ""

for name, group in regions.groupby('Stadt/Region'): # loop to iterrate through regions
    if len(group)> 1:
        for row_index, row in group.iterrows():
            regions_clean.loc[row_index, "geometry"] = Polygon(zip(group.Latitude,group.Longitude)) # regions with same name are grouped into one row element and their geometry data is zipped into the format for POLYGON forms in geopandas

master = pd.concat([regions_clean, cities], ignore_index=True, sort=False) # combine both DataFrames horizontally
master = master.drop_duplicates(subset='Stadt/Region', keep="first")
master  = geopandas.GeoDataFrame(master) # change all data into GeoDataFrame


