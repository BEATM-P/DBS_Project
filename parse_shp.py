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
        # for feature in j_file["features"]:
        #     feature["id"]=feature["properties"]["SCHLUESSEL"]
        i=1
        for feature in j_file["features"]:
            feature ['id'] = str(i).zfill(2)
            i += 1
        
        print(j_file["features"][0])
    #geopdf.to_crs("EPSG25833")
        gdf = gp.GeoDataFrame.from_features(j_file)
        point = (13, 52)

        fig=px.choropleth_mapbox(center = {"lat": 52.516208190476227, "lon": 13.376648940623779}).update_layout(
            mapbox={
                "style": "white-bg",
                "zoom": 9.5,
                "layers": [
                    {
                    "source": json.loads(gdf.geometry.to_json()),
                    "below": "traces",
                    "type": "line",
                    "color": "purple",
                    "line": {"width": 1.5},
                    }
                    ],
                    },
             margin={"l": 0, "r": 0, "t": 0, "b": 0},
            )

        #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()





if __name__=="__main__":
    parseMap(("src/PLR Vector Data/Planungsraum_EPSG_25833.shp"))
