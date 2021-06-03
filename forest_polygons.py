# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:45:18 2020

@author: digvijayp
"""

import mysql.connector as mc
import geopandas as gpd
import geojson,subprocess
import pandas as pd
from shapely.geometry import shape




db=mc.connect(host= "10.15.20.100",database="MAHAVAN_FOREST", user= "digvijayp" , passwd= "Digv1j@yP##")

#query data

cur = db.cursor()



poly=('''select `applicationId`,`area`,`DISTRICT_NAME_en`,ST_AsGeoJSON (`gisdata`)
from `approved_applications_15May`;''' )

cur.execute(poly)
#save the returned data
polygons = cur.fetchall()
df=pd.DataFrame({'ID':[None],'Area':[None],'District':[None],'geometry':[None]})
columns=list(df)
data=[]
for r in range (len(polygons)):
            #print(r)
            r1=polygons[r]
            r10=r1[0]
            r11=r1[1]
            r12=r1[2]
            r13=r1[3]
        
            
            t1=geojson.loads(r13)
            t2=shape(t1)
            values=[r10,r11,r12,t2]
            zipped = zip(columns, values)
            d=dict(zipped)
            data.append(d)
        
df = df.append(data) 
gdf = gpd.GeoDataFrame(df, crs= {'init': 'EPSG:4326'} , geometry=df.geometry)
gdf.to_file("approvde_app15may.geojson", driver="GeoJSON", encoding = 'utf-8')

















    