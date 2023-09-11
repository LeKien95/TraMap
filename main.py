import TraMap_functions

# Set up DataFrame with all data
locations, world = TraMap_functions.set_up_map_and_data()

# Get data from numbeo
costs_data = TraMap_functions.get_numbeo_data()

# Merge both data sets
master = TraMap_functions.merge_data(locations, costs_data)

# Draw the map in a browser
TraMap_functions.draw_map(world, master)
