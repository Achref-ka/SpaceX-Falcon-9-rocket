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

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',   # id='id'
                                             options=[
                                                 {'label': site, 'value': site} for site in ['All'] + list(spacex_df['Launch Site'].unique())
                                             ],
                                             value='All',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                 min=0, max=10000, step=250,
                                                 marks={0: '0', 1000: '1000'},
                                                 value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value')) 
         
def get_pie_chart(entered_site):
     if entered_site == 'All':
         # If ALL sites are selected, group the data by launch site and count successful missions
         site_success_counts = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').size().reset_index(name='Success Count')
 
         # Create a pie chart for the total successful launches for each launch site
         fig = px.pie(site_success_counts, values='Success Count', names='Launch Site', title='Total Success Launches for Each Launch Site')
         return fig
     else:
         # If a specific launch site is selected, filter the dataframe for the selected site
         filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
         
         # Render and return a pie chart for the success (class=1) and failed (class=0) count for the selected site
         fig = px.pie(filtered_df, names='class', title=f'Success vs Failed Launches for {entered_site}')
         return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
 
 
 
def get_scatter_chart(entered_site, payload_range):
     if entered_site.upper() == 'ALL':
         # 
         fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class',
                          color='Booster Version Category',
                          title='Payload vs. Launch Success (All Sites)')
     else:
         # 
         filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
         
         # 
         fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                          color='Booster Version Category',
                          title=f'Payload vs. Launch Success for {entered_site}')
     
     # 
     fig.update_layout(
         xaxis=dict(range=[payload_range[0], payload_range[1]]),
     )
     return fig

# Run the app
if __name__ == '__main__':
    app.run()
