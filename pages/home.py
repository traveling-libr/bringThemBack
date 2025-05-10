# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
import modules.header as hdr
import modules.functions as func
import modules.app_text_prep as txt

home_df = txt.home_df.copy()
report_strings = func.get_report(home_df)

app_text = []
for p in report_strings:
    app_text.append(html.P(p, style={'fontSize':24, 'textAlign':'left'}))

dash.register_page(__name__, path='/')

layout = html.Div([

        dbc.Row(dbc.Col(html.Br())),

        dbc.Row(dbc.Col(html.H1(children='Time in CECOT...', 
            style={'fontSize':36, 'textAlign':'center'}), 
            width={'size': 12})
            ),

        dbc.Row(dbc.Col(html.Br())),
    
        html.Div(id='time-counter'),
        dbc.Row(dbc.Col(dcc.Interval(
            id='interval-component',
            interval=1000,  # Update every second (1000 ms)
            n_intervals=0
        ), width={'size': 8, 'offsetr': 2}), justify="center"),

        dbc.Row(dbc.Col(html.Br())),

        dbc.Row(dbc.Col(html.H1(children='Over 200 men imprisoned by Donald Trump.', 
            style={'fontSize':36, 'textAlign':'center'}), 
            width={'size': 12})
            ),
        dbc.Row(dbc.Col(html.H1(children='No due process. Inhumane conditions.', 
            style={'fontSize':36, 'textAlign':'center', 'color':hdr.alert_color}), 
            width={'size': 12})
            ),
        
        dbc.Row(dbc.Col(html.Br())),

        dbc.Row(dbc.Col(app_text, width={'size': 11, 'offsetr': 1}), justify="center"),

        dbc.Row(dbc.Col(html.Br()))
])

"""dbc.Row(dbc.Col(dcc.Markdown(
        dangerously_allow_html=True,
        children="CECOT. Inhumane conditions and treatment."
        ), width={'size': 8, 'offsetr': 2}), justify="center"),
"""
"""dbc.Row(dbc.Col(html.Div(
            dcc.Markdown(
            dangerously_allow_html=True,
            children=txt.intro_text
        )
    ), width={'size': 12}), justify="center"),"""

