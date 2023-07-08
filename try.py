import plotly
import json
import geopandas as gp
import plotly.express as px
import pandas as pd
import psycopg2
from config import config
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql+psycopg2://pm:admindb@localhost:5432/bikes')
params = config('database.ini')
conn = engine.raw_connection()
cur = conn.cursor()
# params = config(config_db = 'database.ini')
# #print(params)
# engine = psycopg2.connect(**params)


sql = '''
        select count("LOR") , "PLR_NAME" as "BEZIRKSREG", "LOR"
        from fahrraddiebstahl, lor_pl
        where "LOR" = "PLR_ID"
        group by "LOR", "BEZIRKSREG"
        order by count;
'''
countdf = pd.read_sql_query(sql, engine)        
print(countdf['BEZIRKSREG'])

with open("src/lor_bezirksregionen.geojson") as lor_geo:
    lor_data = json.load(lor_geo)
    #print(lor_data.dtype)
    gdf = gp.GeoDataFrame.from_features(lor_data)
    #gdf= gdf.set_geometry("geometry")
    #print(gdf.head())
    #temp = json.loads(gdf.geometry.to_json())


    fig = px.choropleth_mapbox(gdf, geojson = gdf.geometry, locations= countdf['BEZIRKSREG'], color= countdf['BEZIRKSREG'], 
                                        color_continuous_scale="Viridis",
                                        range_color=(1, 318),
                                        mapbox_style= "open-street-map",
                                        zoom= 9.5, center = {"lat": 52.516208190476227, "lon": 13.376648940623779},
                                        opacity = 0.5, 
                                        labels = {'count':'Anzahl Diebstähle'},
                                        featureidkey="properties.bezirksreg"
                                        )#.update_layout(
                                        # mapbox={"layers": [
                                        # {
                                        # "source": lor_data,
                                        # "below": "traces",
                                        # "type": "line",
                                        # "color": "purple",
                                        # "line": {"width": 1.5}}
                                        # ]
                                        # }
                                        # )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

conn.commit()
cur.close()
conn.close()



# import plotly
# import json
# import geopandas as gp
# import plotly.express as px
# import pandas as pd
# import psycopg2
# from config import config


# # Connect to PSQL Database
# params = config(config_db = 'database.ini')
# #print(params)
# engine = psycopg2.connect(**params)

# sql = '''
#         select count("LOR") , "PLR_NAME", "LOR"
#         from table_name, lor_pl
#         where "LOR" = "PLR_ID"
#         group by "LOR", "PLR_NAME"
#         order by count;
# '''

# countdf = pd.read_sql_query(sql, engine)
                      
# #print(countdf)
# # def convertSHPtoJSON(filename:str):

    
# def parseMap(filename:str):
#     geopdf=gp.read_file(filename)
#     tmpfile=filename+"__geojson"
#     #print(geopdf.head(5))
#     #print(geopdf["geometry"])
#     #for p in geopdf["geometry"]:
#     #geopdf["geometry"]=geopdf["geometry"].translate(xoff=-380_000, yoff=-5_810_000)

#     geopdf.set_crs(epsg=25833, inplace=True)
#     geopdf.to_crs(epsg=4326, inplace = True)
#     #print(geopdf.head(5))
#     geopdf.to_file(tmpfile, driver="GeoJSON",mode="w")
#     # return tmpfile
#     with open(tmpfile) as geofile:
#         j_file=json.load(geofile)
#         # for feature in j_file["features"]:
#         #     feature["id"]=feature["properties"]["SCHLUESSEL"]
#         i=1
#         for feature in j_file["features"]:
#             feature ['id'] = str(i).zfill(2)
#             i += 1
        
#         #print(j_file["features"][0])
#     #geopdf.to_crs("EPSG25833")
#         gdf = gp.GeoDataFrame.from_features(j_file)
#         point = (13, 52)
#         #df = pd.DataFrame(json.loads(gdf.geometry.to_json()))
#         #print(df.head())
#         # fig=px.choropleth_mapbox(countdf, locations= 'LOR', color= 'count', color_continuous_scale="Viridis", range_color=(1, 318),
#         #                          center = {"lat": 52.516208190476227, "lon": 13.376648940623779},
#         #                          labels = {'count':'Anzahl Diebstähle'}, opacity = 0.5).update_layout(
#         #     mapbox={
#         #         "style": "white-bg",
#         #         "zoom": 9.5,
#         #         "layers": [
#         #             {
#         #             "source": json.loads(gdf.geometry.to_json()),
#         #             "below": "traces",
#         #             "type": "line",
#         #             "color": "purple",
#         #             "line": {"width": 1.5},
#         #             }
#         #             ],
#         #             },
#         #      margin={"l": 0, "r": 0, "t": 0, "b": 0},
#         #     )
#         # df = json.loads(gdf.geometry.to_json())
#         fig = px.choropleth_mapbox(countdf, geojson = json.loads(gdf.geometry.to_json()), locations= 'PLR_NAME', color= 'count', 
#                                     color_continuous_scale="Viridis",
#                                     range_color=(1, 318),
#                                     mapbox_style= "carto-positron",
#                                     zoom= 9.5, center = {"lat": 52.516208190476227, "lon": 13.376648940623779},
#                                     opacity = 0.5, 
#                                     labels = {'count':'Anzahl Diebstähle'}).update_layout(
#                                     mapbox={"layers": [
#                                     {
#                                     "source": json.loads(gdf.geometry.to_json()),
#                                     "below": "traces",
#                                     "type": "line",
#                                     "color": "purple",
#                                     "line": {"width": 1.5}}
#                                     ]
#                                     }
#                                     )

#         # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#         fig.show()





# if __name__=="__main__":
#     parseMap(("src/PLR Vector Data/Planungsraum_EPSG_25833.shp"))

# engine.close()