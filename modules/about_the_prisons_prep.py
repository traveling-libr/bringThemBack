# Import general libraries
import pandas as pd

# Import geospatial libraries
import geopandas as gpd
import plotly.express as px
from shapely.geometry import Point, LineString, Polygon

# Import visualization and hdrity libraries
import matplotlib.pyplot as plt
import numpy as np
import json

# Import local libraries
import modules.header as hdr
import modules.functions as func

# Create dataframes from local libraries
loc_df = hdr.loc_df.rename(columns={'SourceID':'locID'}).copy()
prison_df = hdr.prison_df.copy()
elsl_geo = hdr.elsl_geo.copy()

# Create reference variable
prison_ref_dict = func.get_ref_dict(hdr.prison_references)
prison_df['Reference'] = [prison_ref_dict[x] for x in prison_df['ID']]

# Merge prison_df with loc_df to get geographic data
map_init = pd.merge(prison_df, loc_df, on='Location', how='left').copy()

# Select stories only if prison is in loc_df
# Sort by LOCATION ad ORDER to display paragraphs in chosen order for each location
prisons = loc_df.Location.unique().tolist()
map_content_df = map_init.loc[map_init['Location'].isin(prisons)].sort_values(['Location','Order']).copy()

# Initialize variables for page about_the_prisons.py
loc_list = sorted(loc_df['Location'].unique().tolist())
loc_init = 'All'
lat_init = 13.6929
lon_init = -89.2182

# Prepare geographic data

# Load as JSON object
elsl_to_json = elsl_geo.to_json()
elsl_geojson = json.loads(elsl_to_json)

elsl_gdf = gpd.GeoDataFrame.from_features(elsl_geojson['features'])

# Define location text
for loc in map_content_df['Location'].unique().tolist():

    if loc=='CECOT':
        c = '#541f9f'
        cf = '#854ed2'
    else:
        c = '#0c546c'
        cf = '#0c7ca2'

#print(loc_df.loc[loc_df['report_string'].notna()])
