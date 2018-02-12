# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:33:51 2017

@author: carlos

Recoge las direcciones completas de los excell de subastas y obtiene las
coordenadas a traves de la api de google maps
"""
"""
API Google coordenadas
Api key :AIzaSyAZLVrqkl-GTpXsmLKvAAWJ-LSpe3Fnqz8
API Google distancias
AIzaSyDHxvAePZj_9u0QakWue59HB9xfnMzzv0c
"""

import pandas as pd
import numpy as np
from pandas import ExcelFile
import json
import googlemaps

# Replace the API key below with a valid API key.
gmaps = googlemaps.Client(key='AIzaSyAZLVrqkl-GTpXsmLKvAAWJ-LSpe3Fnqz8')

file="C:/Users/carlos/Desktop/Proyecto_CICE/subastas_12-12-16.xlsx"

fichero=pd.read_excel(file)

Dir=fichero[["b_Dirección","b_Localidad","b_Provincia"]]

b_latitud=[]
b_longitud=[]
#cadena=Dir.iloc[0][0]+','+Dir.iloc[0][1]+','+Dir.iloc[0][2]
n=0
c_ok=0
for d in Dir.values:
    if Dir.iloc[n][2]=='Madrid':
        
        cadena=str(Dir.iloc[n][0])+','+str(Dir.iloc[n][1])+','+str(Dir.iloc[n][2])
    
        print(cadena)
        geocode_result = gmaps.geocode(cadena)
        if len(geocode_result)==0:
            b_latitud.append(0)    
            b_longitud.append(0)
        else:
            b_latitud.append(geocode_result[0]['geometry']['location']['lat'])
            b_longitud.append(geocode_result[0]['geometry']['location']['lng'])
            c_ok=c_ok+1
        
    else:
        b_latitud.append(0)    
        b_longitud.append(0)
    n=n+1

print("Se han tratado "+str(n)+" direcciones")
print(" - Se han recuperado "+str(c_ok)+" coordenadas.")
print(" - Sin éxito "+str(n-c_ok))

fichero['b_longitud']=b_longitud
fichero['b_latitud']=b_latitud
fichero.to_excel("C:/Users/carlos/Desktop/Proyecto_CICE/subastas_12-12-16_2.xlsx")

def LLevaraMongoSubastas():
    import pymongo
    from pymongo import MongoClient
    import pandas as pd
    file="C:/Users/carlos/Desktop/Proyecto_CICE/subastas_12-12-16_2.xlsx"

    fichero=pd.read_excel(file)
    fichero['Type']="auctions"
    Tabla=fichero[["Identificador","Type","b_Dirección","b_latitud","b_longitud"]]
    TSalida=pd.DataFrame(data=Tabla.values,columns=['cod_id','Type','address','latitude','longitude'])
        
    
    # get a handle to the school database
        
    connection = MongoClient("mongodb://localhost")
    db = connection.Idealistas
    GeoMadrid = db.GeoTmp
    claves=['cod_id','Type','address','latitude','longitude']
    #people_to_insert = [andrew, richard]
    try:
        i=0
        for e in TSalida.values:
            GeoMadrid.insert_one(dict(zip(claves,e)))
            i=i+1
    except Exception as e:
        print( "insert- Unexpected error:", type(e), e)
    print ("Se insertaron "+str(i)+" documentos en GeoMadrid")

# Geocoding and address
#geocode_result = gmaps.geocode(cadena)

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
#now = datetime.now()
#directions_result = gmaps.directions("Sydney Town Hall",
#                                     "Parramatta, NSW",
#                                     mode="transit",
#                                     departure_time=now)