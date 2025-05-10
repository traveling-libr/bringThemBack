# Import general libraries
import numpy as np
import pandas as pd

# Import geospatial libraries
import geopandas as gpd

# import local libraries
import modules.functions as func

# Read data files
src_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/sources.csv')
loc_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/locations.csv')
prison_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/the_prisons.csv')
men_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/the_men.csv')
text_df = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/app_text.csv')

# Read references files
men_references = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/men_references.csv')
prison_references = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/prison_references.csv')
references = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/references.csv')
text_references = pd.read_csv('https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/text_references.csv')

# Colors
time_color = '#cc3300'
alert_color = '#e67300'
title_bg = '#004d39'
title_color = '#ffffff'
marker_color = '#00e7a9'

# Define variable for geoDataFrame
elslpath = 'https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/geoBoundaries-SLV-ADM0.geojson'
elsl_geo = gpd.read_file(elslpath)

# Create iframe for bibliography
bibrefs = ''

for idx, row in references.iterrows():
    bibrefs = bibrefs +  '<p><a href="' + row['URL'] + '" rel="noopener noreferrer" target="_blank">[' + str(row['Reference']) + ']</a> ' +  row['Bibliographic Reference'] + '</p>'

"""# Create a dictionary of IDs and formatted bibliographic References related to list of IDs
def get_ref_dict(df):
    df_sorted = df.sort_values(['ID', 'Reference']).copy()
    ref_dict = {}
    for idx, row in df_sorted.iterrows():
        if row['ID'] not in ref_dict:
            ref_dict[row['ID']] = '[' + str(row['Reference']) + ']'
        else:
            ref_dict[row['ID']] = ref_dict[row['ID']] + ',[' + str(row['Reference']) + ']'
    return ref_dict

def get_report(df):
    report_list = df['Report'].tolist()
    ref_list = df['Reference'].tolist()

    report_strings=[]
    for i in range(0, len(report_list)):
        report_strings.append(report_list[i] + str(ref_list[i]))
        
    return report_strings"""

# Create new variables for the men
men_ref_dict = func.get_ref_dict(men_references.copy())
men_df['Reference'] = [np.nan if str(x)=='nan' else men_ref_dict[x] for x in men_df['ID']]
men_df['Age Group'] = ['0-4' if x <= 4 else '5-14' if x <= 14 else '15-24' if x <= 24 else '25-34' if x <= 34 else '35-44' if x <= 44 else '45-54' if x <= 54 else '55-64' if x <= 64 else 'Unknown' for x in men_df['Age at Deportation'] ]
men_df['Full Name'] = [i + ' ' + j for (i, j) in zip(men_df['First Name'], men_df['Last Name'])]
