# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
from local.content import app_text
import local.design as bbd

dash.register_page(__name__, name="About", path="/about", order=2)

layout = html.Div([
            dbc.Row(dbc.Col(html.Br())),

            dbc.Row(dbc.Col([html.Div(app_text['about_intro'], id='names_intro'),
            html.Div(app_text['about_const'], id='names_intro')], width={'size': 11, 'offsetr': 1}), justify="center"),

        dbc.Row(dbc.Col(html.Br())),
    ], style={'color':bbd.text_color, 'background-color':bbd.div_bg2, 'textAlign':'center'})
