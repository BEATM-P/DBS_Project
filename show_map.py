import plotly
import json
import geopandas as gp
import plotly.express as px
import pandas as pd
import psycopg2
from config import config
from sqlalchemy import create_engine
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def format_numbers(num):
    if type(num)==int:
        return f'{num:08d}'
    else:
        return num


def create_map():
    engine = create_engine(
        'postgresql+psycopg2://pm:admindb@localhost:5432/bikes')
    params = config('database.ini')
    conn = engine.raw_connection()
    cur = conn.cursor()



    sql = '''
            select count("LOR"), "PLR_NAME", "PLR_ID", "LOR", "Gemeinde_name"
            from fahrraddiebstahl, lor_pl, bezirksgrenzen
            where "LOR" = "PLR_ID"
            and "Gemeinde_schluessel" = "BEZ"
            group by "LOR", "PLR_ID", "PLR_NAME", "Gemeinde_name"
            ;
    '''
    countdf = pd.read_sql_query(sql, conn)        
    print(countdf.head())

    countdf=countdf.applymap(format_numbers)

    gdf=gp.read_file("src/PLR Vector Data/lor_plr.shp")

    gdf.set_crs(epsg=25833, inplace=True)
    gdf.to_crs(epsg=4326, inplace = True)

    gdf.to_file("src/PARSEDGEOJSON", driver="GeoJSON",mode="w")
    print(gdf.head())




    with open("src/PARSEDGEOJSON") as gjson:
        jon=json.load(gjson)
        i=1
        for feature in jon["features"]:
            feature ['id'] = feature["properties"]["PLR_ID"]
            i += 1

        bez = countdf["Gemeinde_name"].to_list()
        trace = go.Choroplethmapbox(
        geojson=jon,  # GeoJSON data or DataFrame with geographical data
        locations=countdf["PLR_ID"],  # List of locations or region identifiers
        z=countdf['count'],  # Values to be mapped to colors
        colorscale=[[0, 'rgb(255,255,255)'],[1, 'rgb(255,0,0)']],  # Choose a colorscale
        zmin=0,  # Set the minimum value for color mapping
        zmax=350,  # Set the maximum value for color mapping
        marker_opacity=0.7,  # Set the opacity of the markers
        marker_line_width=1,  # Set the width of marker lines
        colorbar=dict(title='Colorbar Title'),
        hoverinfo="none", 
        customdata=countdf,
        hovertemplate="Bezirk: %{customdata[4]}"+"<br>Planungsraum: %{customdata[1]}"+"<br>Fahrraddiebstähle: %{z}"
    )

        layout = go.Layout(
        mapbox_style='white-bg',#'carto-positron',  # Choose a mapbox style
        mapbox_zoom=9.3,  # Set the initial zoom level
        mapbox_center= {"lat": 52.516208190476227, "lon": 13.376648940623779},  # Set the initial center of the map
    )


        fig = go.Figure(data=trace, layout=layout)

        return fig

#fig.show()


