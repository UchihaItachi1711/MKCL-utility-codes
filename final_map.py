# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 17:53:21 2020

@author: digvijayp
"""

import mysql.connector as mc
import geopandas as gpd
from matplotlib_scalebar.scalebar import ScaleBar
from math import cos, asin, sqrt, pi
import math


db=mc.connect(host= "10.15.20.100",database="MAHAVAN_GIS_PROD", user= "digvijayp" , passwd= "Digv1j@yP##")

cursor = db.cursor()
query="SELECT ST_AsGeoJSON((g.gisdata)) AS dt FROM gisrecords g WHERE g.`applicationId` IN ('NI47409600015')"


cursor.execute(query)
records = cursor.fetchall()
p1=records[0]
p11=p1[0]
p=gpd.read_file(p11)
bounds=p.total_bounds


def distance(bo):
    for b in bo:
        avg=(bo[1]+bo[3])/2
        p = pi/180
        a = 0.5 - cos((avg-avg)*p)/2 + cos(avg*p) * cos(avg*p) * (1-cos(((bo[0]+1)-bo[0])*p))/2
    return  12742 * asin(sqrt(a))

metres=distance(bounds)*1000
xmin, ymin, xmax, ymax = bounds
difx= (xmax-xmin)/3
dify= (ymax-ymin)/3
xmid=(xmin+xmax)/2
xm4=(xmax+difx)
xm3=(xmin-difx)
ym3=(ymin-dify)
ym4=(ymax+dify)
ymid=(ymin+ymax)/2


#%%
gc=p.plot(facecolor="none",edgecolor='black', lw=2 )
gc.get_xaxis().get_major_formatter().set_useOffset(False)
gc.get_yaxis().get_major_formatter().set_useOffset(False)





gc.set_xticks((xmin,xmid,xmax)) 
gc.set_yticks((ymin,ymid, ymax))




gc.set_xlabel('Longitude' )
gc.set_ylabel('Latitude',rotation = 90)


gc.grid('on', which='major',linestyle=':', linewidth='0.4', color='#ff726f')
#gc.gridlines(draw_labels=True, dms=True)
gc.grid(True)
gc.tick_params(bottom= True,top= True, right = True, left = True)
gc.tick_params(labelbottom = True,labeltop = True,labelright = True,labelleft = True)

scale_bar = ScaleBar(metres,units="m",box_color='#D3D3D3')
gc.add_artist(scale_bar)
gc.set_frame_on(False)
gc.figure

#%%
def dd2dms(dd):
    dms=[]
    for d in dd:
        if d <= 40:
    	    appendix = 'N'
        else:
            appendix = 'E'
        minutes = d%1.0*60
        seconds = minutes%1.0*60
        dms.append( """{0}°{1}'{2:2.0f}"{3}""".format(int(math.floor(d)), int(math.floor(minutes)), seconds, appendix))
       
    return dms


lat=[n.get_text() for n in gc.get_yticklabels()]
lon=[m.get_text() for m in gc.get_xticklabels()]
latitude=[float(i) for i in lat]
longitude=[float(j) for j in lon]
Lati= dd2dms(latitude)
Longi= dd2dms(longitude)

gc.set_yticklabels(Lati,rotation=0)
gc.set_xticklabels(Longi)
gc.tick_params(labelsize=5, pad= 10)
gc.figure
#gc.figure.savefig('frame.png',dpi=500)
#%%

