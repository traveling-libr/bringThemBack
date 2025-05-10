# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
import modules.header as hdr

dash.register_page(__name__)

layout = html.Div([
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.Div(
        dcc.Markdown(
        dangerously_allow_html=True,
        children=hdr.bibrefs,
        )
    ), width={'size': 11, 'offsetr': 0.5}), justify="center")
])

