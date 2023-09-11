# folium Version: 0.14.0

from Map import world
from Merge_Data import master
import webbrowser
import os
import folium

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