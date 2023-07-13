from datetime import date
from dash import Dash, dcc, html, Input, Output
from sqlalchemy import create_engine
import plotly.graph_objects as go
import json
import geopandas as gp
import pandas as pd

from sqlGenerator import SQLGenerator

sql=SQLGenerator()

engine = create_engine(
    'postgresql+psycopg2://pm:admindb@localhost:5432/bikes')
conn = engine.raw_connection()

gdf=gp.read_file("src/PLR Vector Data/lor_plr.shp")

gdf.set_crs(epsg=25833, inplace=True)
gdf.to_crs(epsg=4326, inplace = True)

gdf.to_file("src/PARSEDGEOJSON", driver="GeoJSON",mode="w")

gjson=open("src/PARSEDGEOJSON")
jon=json.load(gjson)
i=1
for feature in jon["features"]:
        feature ['id'] = feature["properties"]["PLR_ID"]
        i += 1

def format_numbers(num):
    if type(num)==int:
        return f'{num:08d}'
    else:
        return num

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Fahrraddiebstahl in Berlin'),
    html.P("Filter:"),
    
    dcc.DatePickerRange(
        display_format=("DD/MM/YYYY"),
        min_date_allowed=date(2022, 1, 1),
        max_date_allowed=date(2023, 6, 10),
        initial_visible_month=date(2023, 6, 10),
        end_date=date(2023, 6, 10),
        start_date=date(2022,1,1),
        id='Datum'),
    dcc.Checklist(
        ['Tag', 'Nacht'],
        inline=True,
        id='Tageszeit'),
    dcc.Checklist(
        ['Versuchter Diebstahl', 'Erfolgreicher Diebstahl'],
        inline=True,
        id='Versuch'),
    dcc.Dropdown(
        ['Reinickendorf', 'Charlottenburg-Wilmersdorf', 'Treptow-Köpenick', 'Pankow', 'Neukölln', 'Lichtenberg', 'Marzahn-Hellersdorf', 'Spandau', 'Steglitz-Zehlendorf', 'Mitte', 'Friedrichshain-Kreuzberg', 'Tempelhof-Schöneberg'],
        multi=True,
        placeholder= 'Bezirk',
        id = 'Bezirk'),

    dcc.Dropdown(
        ['Damenfahrrad', 'Lastenfahrrad', 'Fahrrad', 'Herrenfahrrad', 'diverse Fahrräder', 'Kinderfahrrad', 'Mountainbike', 'Rennrad'],
        multi=True,
        placeholder='Art des Fahrrads',
        id='ArtdesFahrrads'),
    dcc.Dropdown(
        ['open-street-map', 'white-bg'],
        multi=False,
        placeholder= 'Map Style',
        id = 'style'),
    
    dcc.Graph(id="graph", style={'width': '90vw', 'height': '90vh'} ),
    html.P("Map data provided by \"Amt für Statistik Berlin-Brandenburg\"")
])


@app.callback(
    Output("graph", "figure"), 
    Input("Bezirk", "value"),
    Input("Tageszeit", "value"),
    Input("ArtdesFahrrads", "value"),
    Input("Versuch", "value"),
    Input("Datum", "start_date"),
    Input("Datum", "end_date"),
    Input("style","value"))
def create_map(Bezirk, Tageszeit, ArtdesFahrrads, Versuch, startDatum, endDatum, style):
    print(startDatum, endDatum)
    query=sql.update_handler(Bezirk,ArtdesFahrrads, Tageszeit, Versuch, startDatum, endDatum)

    countdf = pd.read_sql_query(query, conn)       # Create dataframe with Query 

    countdf=countdf.applymap(format_numbers)

    print(countdf.head())

    trace = go.Choroplethmapbox(
        geojson=jon,  # GeoJSON data or DataFrame with geographical data
        locations=countdf["PLR_ID"],  # List of locations or region identifiers
        z=countdf['count'],  # Values to be mapped to colors
        colorscale=[[0, 'rgb(255,255,255)'],[1, 'rgb(255,0,0)']],  # Choose a colorscale
        zmin=0,  # Set the minimum value for color mapping
        zmax=350,  # Set the maximum value for color mapping
        marker_opacity=0.5,  # Set the opacity of the markers
        marker_line_width=1,  # Set the width of marker lines
        colorbar=dict(title='Anzahl Diebstähle'), # Set title of bar on the right
        hoverinfo="none", 
        customdata=countdf,
        hovertemplate="Bezirk: %{customdata[3]}"+"<br>Planungsraum: %{customdata[2]}"+"<br>Fahrraddiebstähle: %{z}<extra></extra>"
        )
    if style==None:
        style="open-street-map"
    print("\n")
    print(style)
    print("\n")
    layout = go.Layout(
        mapbox_style=style,#'carto-positron',  # Choose a mapbox style
        mapbox_zoom=9,  # Set the initial zoom level
        mapbox_center= {"lat": 52.516208190476227, "lon": 13.376648940623779}  # Set the initial center of the map
        )


    fig = go.Figure(data=trace, layout=layout)
    return fig


app.run(debug=True)