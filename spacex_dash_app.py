# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

option = [
    {'label': i, 'value': i} for i in spacex_df['Launch Site'].value_counts().index
]
option.append({
    'label': "All site", 'value': "All"
})
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=option,
                                             value='All',
                                             placeholder="Select a Launch Site here", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload], marks={
                                    2500: {'label': '2500 (Kg)'}, 5000: {'label': '5000 (Kg)'}, 7500: {'label': '7500 (Kg)'}}),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
              )
def pie_chart(inp):
    if inp == 'All':
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Total Success Launches by Site')
    else:
        df = spacex_df[spacex_df["Launch Site"] == inp]
        df = df.groupby(['Launch Site', "class"]
                        ).size().reset_index(name='count')
        fig = px.pie(df, values='count', names='class',
                     title='Total Success Launches for ' + inp)
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), Input(
                  component_id='payload-slider', component_property='value')
              )
def scatter(site, payload):
    df = spacex_df[spacex_df['Payload Mass (kg)'].between(
        payload[0], payload[1])]
    if site == 'All':
        fig2 = px.scatter(df, y="class", x="Payload Mass (kg)",
                          color="Booster Version Category")
    else:
        fig2 = px.scatter(df[df['Launch Site'] == site], y="class", x="Payload Mass (kg)",
                          color="Booster Version Category")
    return fig2


# Run the app
if __name__ == '__main__':
    app.run_server()
