# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

#import plotly libraries
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

# Import geospatial libraries
import geopandas as gpd

# Import local libraries
import modules.header as hdr
import modules.about_the_prisons_prep as pp

loc_list = ['All'] + pp.loc_list
loc_ = pp.loc_init

dash.register_page(__name__)

layout = html.Div([
            dbc.Row(dbc.Col(html.Br())),

            dbc.Row(dbc.Col(html.H3(children='The El Salvador Prison System'), width={'size': 11, 'offsetr': 1}), justify="center"),

            dbc.Row(dbc.Col(html.Br())),

            dbc.Row(dbc.Col(dcc.RadioItems(id='slct_loc', options=loc_list, value=loc_, inline=True, style={'accent-color':hdr.title_bg}, inputStyle={"margin-left":"20px", "margin-right":"5px"}), width={'size': 11, 'offsetr': 1}), justify="center"),

            dbc.Row(dbc.Col(html.Div(id='loc_output_container', children=[]), style={"margin-left":"40px"}, width={'size': 11, 'offsetr': 1}), justify="center"),

            dbc.Row([dbc.Col(dcc.Graph(id='elsl_map', figure={}, config={'scrollZoom': True}), width={'size': 6, 'offsetr': 1}),
                dbc.Col(id='map_text', children=[], width={'size': 5, 'offsetr': 1})], justify="center"),
            
            dbc.Row(dbc.Col(html.Br()))

        ])