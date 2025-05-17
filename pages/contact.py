import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, name="Contact", path="/contact", order=7)

layout = html.Div([
    dbc.Row(dbc.Col([html.H1("Contact Us"),
    html.P("If you have any information to share for this site, please send the resource links along with your message."),
    html.Div([
        html.Label("Name:"),
        dcc.Input(id="name", type="text", placeholder="Your name"),
    ], style={'margin-bottom': '10px'}),
    html.Div([
        html.Label("Email:"),
        dcc.Input(id="email", type="email", placeholder="Your email"),
    ], style={'margin-bottom': '10px'}),
    html.Div([
        html.Label("Message:"),
        dcc.Textarea(id="message", placeholder="Your message", style={'height': '100px', 'width': '100%'}),
    ], style={'margin-bottom': '10px'}),
    html.Button("Submit", id="submit-button", n_clicks=0),
    html.Div(id="output-state")], width={'size': 11, 'offsetr': 1}), justify='center'
    )
])
