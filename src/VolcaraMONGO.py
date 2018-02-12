# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 23:16:59 2017

@author: carlos
"""

def LLevarServicios():
    import pymongo
    from pymongo import MongoClient
    import pandas as pd
    
    fich="C:/Users/carlos/Desktop/Proyecto_CICE/Servicios/Todos.xlsx"

    fichero=pd.read_excel(fich)

    claves=['cod_id','Type','Subtype','address','municipality','latitude','longitude']
    fichero['Type']="services"
    fichero['DIRECCION']=fichero["CLASE-VIAL"]+" "+fichero["NOMBRE-VIA"] 
    
    T=fichero[["PK","Type","NOMBRE","DIRECCION","LOCALIDAD","LATITUD","LONGITUD"]]
    TSalida=pd.DataFrame(data=T.values,columns=claves)
        
    # get a handle to the school database
        
    connection = MongoClient("mongodb://localhost")
    db = connection.Idealistas
    GeoMadrid = db.GeoTmp
    
    try:
        i=0
        for e in TSalida.values:
            GeoMadrid.insert_one(dict(zip(claves,e)))
            i=i+1
    except Exception as e:
        print( "insert- Unexpected error:", type(e), e)
    print ("Se insertaron "+str(i)+" documentos en GeoMadrid")    

def LLevaraColegios(file):
    import pymongo
    from pymongo import MongoClient
    import pandas as pd
    
    fich="C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/"+file

    fichero=pd.read_excel(fich)

    claves=['cod_id','Type','address','municipality','latitude','longitude']
        
    T=fichero[["CODIGO CENTRO","TIPO DE CENTRO","DOMICILIO","MUNICIPIO","b_latitud","b_longitud"]]
    TSalida=pd.DataFrame(data=T.values,columns=claves)
        
    # get a handle to the school database
        
    connection = MongoClient("mongodb://localhost")
    db = connection.Idealistas
    GeoMadrid = db.GeoTmp
    
    try:
        i=0
        for e in TSalida.values:
            GeoMadrid.insert_one(dict(zip(claves,e)))
            i=i+1
    except Exception as e:
        print( "insert- Unexpected error:", type(e), e)
    print ("Se insertaron "+str(i)+" documentos en GeoMadrid")    
    
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