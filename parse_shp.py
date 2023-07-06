import plotly
import json
import geopandas as gp
import plotly.express as px


# def convertSHPtoJSON(filename:str):

    
def parseMap(filename:str):
    geopdf=gp.read_file(filename)
    tmpfile=filename+"__geojson"
    print(geopdf.head(5))
    print(geopdf["geometry"])
    #for p in geopdf["geometry"]:
    #geopdf["geometry"]=geopdf["geometry"].translate(xoff=-380_000, yoff=-5_810_000)

    geopdf.set_crs(epsg=25833, inplace=True)
    geopdf.to_crs(epsg=4326, inplace = True)
    print(geopdf.head(5))
    geopdf.to_file(tmpfile, driver="GeoJSON",mode="w")
    # return tmpfile
    with open(tmpfile) as geofile:
        j_file=json.load(geofile)
        for feature in j_file["features"]:
            feature["id"]=feature["properties"]["SCHLUESSEL"]
        print(j_file["features"][0])
    #geopdf.to_crs("EPSG25833")
        fig = px.choropleth_mapbox(data_frame=geopdf,geojson=j_file,# color=,
                        #    color_continuous_scale="Viridis",
                            #range_color=(0, 12),
                            mapbox_style="white-bg",
                        #    zoom=3,
                            featureidkey=feature.id,
                            center = {"lat":13 , "lon": 52},
                            opacity=1,
                        #    labels={'unemp':'unemployment rate'}
                          )
        #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()





if __name__=="__main__":
    parseMap(("src/PLR Vector Data/Planungsraum_EPSG_25833.shp"))
