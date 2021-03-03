
import geopandas as gpd 
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set(style = "darkgrid")
height = [62, 64, 69, 75, 66, 68]
weight = [120, 136, 148, 175, 154, 143]
sns.scatterplot(x=height, y=weight)

usa = gpd.read_file("visuals/map_files/States_shapefile.shp")

usa_plot = usa[usa.State_Code == "TX"].plot()

