# Import general libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#import plotly libraries
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

# Import local libraries
import modules.header as hdr

# Create dataframes from local libraries
men_df = hdr.men_df.loc[hdr.men_df['SourceIDs'].notna()].copy()

# Initialize variables for page chart_summary.py
stat_init = 'All'
stat_dict = {'All':'All'}
for e in sorted(men_df['Immigration Status'].unique().tolist()):
    stat_dict[e] = e

age_init = 'All'
age_dict = {'All':'All'}
for e in sorted(men_df['Age Group'].unique().tolist()):
    age_dict[e] = e

rec_init = 'All'
rec_dict = {'All':'All'}
for e in sorted(men_df['Criminal Record'].unique().tolist()):
    rec_dict[e] = e

# Define colors for cat chart
cat1 = '#fbafe4'
cat2 = '#ece133'
cat3 = '#56b4e9'
cat4 = '#cc78bc'
cat5 = '#949494'
cat6 = '#0173b2'
cat7 = '#029e73'
cat8 = '#d55e00'

fig1 = px.strip(men_df, 
                x="Immigration Assignment", y="Criminal Record", color="Age Group", 
                labels={
                     "Immigration Status": "Status",
                     "Age at Deportation": "Age",
                     "Immigration Assignment": "Immigration Assignment",
                     "Criminal Record": "Criminal Record",
                     "Age Group":'Age Group',
                     "Reference":'Sources'
                 },
                category_orders={"Immigration Assignment": ["Asylum", "Withholding of Removal", "Temporary Protected Status", "Deportation to VE"],
                              "Age at Deportation": ["Age"],
                              "Criminal Record": ["No record"],
                              "Age Group": ["0-4", "5-14", "15-24", "25-34", "35-44", "45-54", "55-64", "Unknown"]},
                color_discrete_map={"0-4":cat1, "5-14":cat2, 
                            "15-24":cat3, "25-34":cat4, 
                            "35-44":cat5, "45-54":cat6, 
                            "55-64":cat7, "Unknown":cat8},
                hover_name='Full Name',
                hover_data={'Age at Deportation':True,
                            'Immigration Status':True,
                            'Reference':True,
                            'Age Group':False,
                            'Immigration Assignment':False,
                            'Criminal Record':False},
                title="Men Imprisoned in CECOT", 
                stripmode = "group"  # Select between "group" or "overlay" mode
)    

fig1.update_traces(marker=dict(size=10))

#fig1.show()

"""# Create countplot
fig = px.bar(men_df
             ,x='Immigration Assignment'
             ,text='Full Name'
             ,labels={
                     "Full Name": "Name",
                     "Age at Deportation": "Age",
                     "Immigration Assignment": "Immigration Assignment",
                     "Immigration Status": "Status of Assignment",
                     "Criminal Record": "Criminal History",
                     "Reference":'Sources'
                 }
             ,category_orders={"Immigration Assignment": ["Asylum", "Withholding of Removal", "Temporary Protected Status", "Deportation to VE"]}
            )
customdata = np.stack((men_df['Full Name'], men_df['Age at Deportation'], men_df['Immigration Status'], men_df['Criminal Record'], men_df['Reference']), axis=-1)

fig.update_traces(
    customdata=customdata,
    hovertemplate="<b>%{customdata[0]}</b><br>Age: %{customdata[1]}<br>Assignment: %{x}<br>Status: %{customdata[2]}<br>Criminal History: %{customdata[3]}<br>Sources: %{customdata[4]}<extra></extra>"
)
 
fig.update_layout(title='Count of Men Imprisoned in CECOT by Immigration Assignment', showlegend=False)"""

#fig.show()
