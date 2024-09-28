# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown para seleccionar el sitio de lanzamiento
    dcc.Dropdown(id="site-dropdown",
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                 ],
                 value="ALL",
                 placeholder="Select a site",
                 searchable=True),
    
    html.Br(),
    dcc.Graph(id='success-pie-chart'),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider', 
                    min=0,max=10000,step=1000,
                    value=[min_payload,max_payload]),

                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(selected_site):

    if selected_site == 'ALL':  
        filtered_df = spacex_df.groupby('Launch Site')['class'].value_counts().reset_index(name='counts')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_counts = filtered_df['class'].value_counts().reset_index(name='counts')
        

    if selected_site == 'ALL':
        fig = px.pie(filtered_df, 
                     names='Launch Site', 
                     values='counts', 
                     title='Success vs. Failed Launches for All Sites')
    else:
        fig = px.pie(success_counts, 
                     names='class', 
                     values='counts', 
                     title=f'Success vs. Failed Launches for {selected_site}')
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"),Input(component_id='site-dropdown', component_property='value')]
)

def scatterchart(input2,input3,selected_site):
    rangedf = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= input3[0]) & 
        (spacex_df["Payload Mass (kg)"] <= input3[1])]

    if input2 == 'ALL': 
        fig= px.scatter(rangedf,
                        y="class",
                        x="Payload Mass (kg)" )
    else:
        filtered_df = rangedf[rangedf['Launch Site'] == selected_site]
        fig= px.scatter(filtered_df,
                        y="class",
                        x="Payload Mass (kg)" )
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server(port=8080)
    
