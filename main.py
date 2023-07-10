# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

from show_map import 

# Initialize the app - incorporate css
app = Dash(__name__, external_stylesheets)

# App layout
app.layout = html.Div([
    html.Div(className='row', children='My First App with Data, Graph, and Controls',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                       value='lifeExp',
                       inline=True,
                       id='my-radio-buttons-final')
    ]),
    html.Div(className='row', children=[
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                    value='lifeExp',
                    inline=True,
                    id='my-radio-buttons-final')])
    html.Div(className='six columns', children=[
          dcc.Graph(figure=, id='histo-chart-final')]
    
    ))

# Add controls to build the interaction
@callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
