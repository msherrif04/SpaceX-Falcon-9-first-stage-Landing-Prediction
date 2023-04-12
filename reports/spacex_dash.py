# Import required libraries
import pandas as pd
import dash
# import dash_html_components as html
from dash import html
# import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


url = r'C:\Users\Sherrif\Desktop\Everything\Projects\Code\falcon9-ds-project\SpaceX-Falcon-9-first-stage-Landing-Prediction\data\external\spacex_launch_dash.csv'
spacex_df = pd.read_csv(url)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
  
marks = {}
for n in range(0,11000,1000):
    marks[n]=str(n)


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                                'font-size': 40}),
                                
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label':'All Sites', 'value':'ALL'},
                                                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                    {'label':'KSC LC-39A  ', 'value':'KSC LC-39A'},
                                                    {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                                    {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}],
                                            value="ALL",
                                            placeholder='select launch site',
                                            searchable=True
                                            ),
                                html.Br(),

                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                marks=marks,
                                                value=[min_payload,max_payload]),

                                
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df=spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site =='ALL':
        fig=px.pie(spacex_df, values='class', names='Launch Site', title='Launch Success rates by Site')
        return fig
    else:
        fig=px.pie(filtered_df, names='class', title= f'Success rate of {entered_site}')
        return fig
        

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site,payload_mass):
    if entered_site=='ALL':
        scatter_data= spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1], 'both')]
        fig = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        scatter_data = spacex_df[(spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1], 'both'))& (spacex_df['Launch Site']==entered_site)]
        fig = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
