# Import dash libraries
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#import plotly libraries
import plotly.express as px

# Import utility libraries
import numpy as np
import pandas as pd
from datetime import datetime as dt

# Import local libraries
import modules.header as hdr
import modules.functions as func
import modules.chart_summary_prep as sp
import modules.about_the_prisons_prep as pp


app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SUPERHERO])
#app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

page_links = [dcc.Link(page['name'], href=page['relative_path'], className="nav-link")
            for page in dash.page_registry.values()]
"""[dcc.Link(page['name']+"  |  ", style={'fontSize':20, 'textAlign':'center'}, href=page['path'])
            for page in dash.page_registry.values()], id='navBar'),"""


app.layout = html.Div(
    [
        # main app framework
        html.Div("Cruel. Unusual. Indefensible.", style={'fontSize':90, 'textAlign':'center', 'background-color':hdr.title_bg, 'color':hdr.title_color}),
        html.Nav(children=[
            html.Div([
            html.Div(page_links, className="navbar-nav")
            ], className="container-fluid"),
        ], className="navbar navbar-expand-lg bg-dark", **{"data-bs-theme": "dark"}),
        #html.Hr(),

        # content of each page
        dash.page_container
    ]
)

# Connect the Plotly graphs with Dash Components

# Define callback for bar chart summary
stat_dict = sp.stat_dict
age_dict = sp.age_dict
rec_dict = sp.rec_dict
men_df = sp.men_df.loc[sp.men_df['SourceIDs'].notna()].copy()

@app.callback(
    [Output(component_id='stat_output_container', component_property='children'),
    Output(component_id='age_output_container', component_property='children'),
    Output(component_id='rec_output_container', component_property='children'),
     Output(component_id='bar_chart', component_property='figure')],
    [Input(component_id='slct_stat', component_property='value'),
     Input(component_id='slct_age', component_property='value'),
     Input(component_id='slct_rec', component_property='value')]
)
def get_chart_specs(stat_slctd, age_slctd, rec_slctd):

    stat_cntr = "Selected location: {}".format(stat_slctd)
    age_cntr = "Selected location: {}".format(age_slctd)
    rec_cntr = "Selected location: {}".format(rec_slctd)

    dff_init = pd.DataFrame()

    if stat_slctd == 'All':
        dff_init = men_df.copy()
    else:
        dff_init = men_df.loc[men_df['Immigration Status']==stat_slctd].copy()
    
    if age_slctd == 'All':
        dff_init2 = dff_init.copy()
    else:
        dff_init2 = dff_init.loc[dff_init['Age Group']==age_slctd].copy()
    
    if rec_slctd == 'All':
        dff = dff_init2.copy()
    else:
        dff = dff_init2.loc[dff_init2['Criminal Record']==rec_slctd].copy()

    # Create countplot
    fig = px.bar(dff
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
             ,color_discrete_sequence=px.colors.qualitative.Set3
             ,category_orders={"Immigration Assignment": ["Asylum", "Withholding of Removal", "Temporary Protected Status", "Deportation to VE"]}
            )
    customdata = np.stack((dff['Full Name'], dff['Age at Deportation'], dff['Immigration Status'], dff['Criminal Record'], dff['Reference']), axis=-1)

    fig.update_traces(
        customdata=customdata,
        hovertemplate="<b>%{customdata[0]}</b><br>Age: %{customdata[1]}<br>Assignment: %{x}<br>Status: %{customdata[2]}<br>Criminal History: %{customdata[3]}<br>Sources: %{customdata[4]}<extra></extra>"
    )
 
    #fig.update_layout(title='Count of Men Imprisoned in CECOT by Immigration Assignment', showlegend=False)
    fig.update_layout(showlegend=False)

    return stat_cntr, age_cntr, rec_cntr, fig

# Define callback for El Salvador map
loc_list = pp.loc_list.copy()
loc_df = pp.loc_df.copy()
map_content_df = pp.map_content_df.copy()
elsl_gdf = pp.elsl_gdf

@app.callback(
    [Output(component_id='loc_output_container', component_property='children'),
     Output(component_id='map_text', component_property='children'),
     Output(component_id='elsl_map', component_property='figure')],
    [Input(component_id='slct_loc', component_property='value')]
)
def get_map_specs(loc_slctd):

    container = "Selected location: {}".format(loc_slctd)

    dff = loc_df.copy()
    if loc_slctd == 'All':
        lat_=pp.lat_init
        lon_=pp.lon_init
        loc_zoom=8
    else:
        lat_ = dff[dff["Location"] == loc_slctd]['Latitude'].values[0]
        lon_ = dff[dff["Location"] == loc_slctd]['Longitude'].values[0]
        loc_zoom=12

    fig = px.scatter_mapbox(dff, lat='Latitude'
        , lon='Longitude'
        ,text='Location'
        ,mapbox_style="open-street-map"
        #,mapbox_style="satellite-streets"
        ,hover_name="Location"
        ,hover_data=["City", "Department"]
    )

    # Update layout to set zoom and center
    fig.update_layout(
        #mapbox_style='satellite-streets'
        mapbox_zoom=loc_zoom
        ,mapbox_center={"lat": lat_, "lon": lon_}
        ,margin=dict(l=20, r=20, t=20, b=20)
    )

    fig.update_traces(marker=dict(size=20,
                                  color=hdr.marker_color,
                                  opacity=0.5),
                  selector=dict(mode='markers+text'))

    dff2 = map_content_df.copy()
    dff2 = dff2[dff2["Location"] == loc_slctd]

    report_strings = func.get_report(dff2)

    loc_text = []
    for p in report_strings:
        loc_text.append(html.P(p, style={'fontSize':18, 'textAlign':'left'}))

    return container, loc_text, fig

# Set the start date as the deportation date
deportation_string = "2025-03-15 00:00:00"
format_string = "%Y-%m-%d %H:%M:%S"

deportation_time = dt.strptime(deportation_string, format_string)
start_time = deportation_time

# Define callback for time counter
@app.callback(Output('time-counter', 'children'),
              Input('interval-component', 'n_intervals'))
def update_time(n):
    current_time = dt.now()
    elapsed_time = current_time - start_time
    
    days = elapsed_time.days
    hours, remainder = divmod(elapsed_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    time_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    #return html.Span(f"Elapsed time: {time_str}")
    #return html.Span(f"{time_str}")
    return html.H1(f"{time_str}", style={'fontSize':60, 'textAlign':'center', 'color':hdr.time_color})

"""if __name__ == "__main__":
    app.run(debug=True)"""