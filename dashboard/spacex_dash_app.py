# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv", index_col=0)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = spacex_df["Launch Site"].unique().tolist()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                   
                                dcc.Dropdown(id='site-dropdown', 
                                             options=[{'label': 'All Sites', 'value': 'ALL'}
                                                     ] + [{'label': site, 'value': site} for site in launch_sites]),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                        min=min_payload, max=max_payload, step=500,
                                        value=[min_payload, max_payload]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', 
              component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              )
def get_pie_chart(input_site):
    print(input_site)
    if input_site == "ALL":
        fig = px.pie(spacex_df, values='class', 
        names="Launch Site", 
        title='Total success launches by site')
        return fig    
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == input_site]
        fig = px.pie(filtered_df,
                     names="class",
                     title=f'Total success launches site: {input_site}')
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', 
                     component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(input_site, pay_load):
    print(pay_load)
    if input_site == "ALL":
        fig = px.scatter(spacex_df, x="Payload Mass (kg)", 
                         y="class", 
                         color="Booster Version Category"
                         )
        return fig
    else:
        filtered_df = spacex_df[(spacex_df["Launch Site"] == input_site) & 
                                (spacex_df["Payload Mass (kg)"] >= pay_load[0]) & 
                                (spacex_df["Payload Mass (kg)"] <= pay_load[1])]
        print(filtered_df)

        fig = px.scatter(filtered_df, x="Payload Mass (kg)", 
                         y="class", 
                         color="Booster Version Category"
                         )
    
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
