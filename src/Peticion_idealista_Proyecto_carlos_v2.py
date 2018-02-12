# -*- coding: utf-8 -*-
"""
Petición a Idealista
""" 
import datetime
import requests
import requests.auth
import base64
import pandas as pd
from pymongo import MongoClient
import json


#Códigos proporcionados por Idealista
Apikey='xxxxxx'
Secret='xxxxxx'

#concateno apikey y secret y convierto a base 64 según indicado por Idealista
#Asigno ContentType y GrantType según indicado por Idealista
Authorization=base64.b64decode(Apikey+':'+ Secret)
ContentType='application/x-www-form-urlencoded'
grant_type='client_credentials&scope=write'

def Iniciar_Idealista():
        
#Asigno variables para petición del Token
    client_auth = requests.auth.HTTPBasicAuth(Apikey, Secret)
    post_data = {"grant_type":"client_credentials"}
    headers = {"Authorization": Authorization,'Content-Type':ContentType,'grant_type':grant_type}
    response = requests.post("https://api.idealista.com/oauth/token", auth=client_auth, data=post_data, headers=headers)
    response.status_code#Recibo status 200
    response.json()#respuesta
    response.json()['access_token']#Access Token
    return response


""" STATUS CODES API Idealistas
200 -OK
400 -Invalid value. Accepted values for operation are: sale, rent 400
400 -operation is required 400
404 -the locationId doesn't exist 404
500 -server error 500
"""

def Hacer_Peticion(r,pagina,centro):
#paso headers y parámetros para petición get
    headerst={"Authorization":'bearer %s' %r.json()['access_token']}
    #obligatorios: country, operation, propertyType, locationId, distance ynnnnnnnnnnnn Center
    payload={'country':'es', 'operation':'sale', 'propertyType':'homes', 'numPage':1,
             'locationId':'0-EU-ES-28', 'center':"40.741,-4.054",'distance':15000,'maxItems':50}
    
    payload['numPage']=pagina
    payload['center']=centro
    #payload=ValidarParam(parametros)
            
#Hago petición
    resget=requests.post('https://api.idealista.com/3.5/es/search?', params=payload, headers=headerst)
    sc_peticion=resget.status_code#Recibo status 200


    if sc_peticion == 200:

        datos = resget.json()
        # return datos
        print("Paramentros entrada: ", payload)
        Resultados(datos)
        return datos
    else:
        print("Error ", sc_peticion, " en la petición a la API")
        return 999


        
def Resultados(d):
    print("Páginas devueltas: ",datos['totalPages'])
    print("Elementos en total: ",datos['total'])
    print(datos['itemsPerPage'], "elementos de la página ",datos['actualPage'] )
            

        
def insert_many(elementos):
    connection = MongoClient("mongodb://localhost")
    
    # get a handle to the school database
    db = connection.Idealistas
    Madrid = db.MadridNorte
    
    #formateamos la fecha el sistema
    fech_hora=datetime.datetime.now()
    fech_hora='{:%Y-%m-%d %H:%M:%S}'.format(fech_hora)
    #añadimos la fecha al documento
    for e in elementos:
        e['date']=fech_hora

    print ("insertamos ", len(elementos)," elementos en " , Madrid)
    #people_to_insert = [andrew, richard]
    try:
        Madrid.insert_many(elementos, ordered=False)
    except Exception as e:
        print( "Unexpected error:", type(e), e)


"""PRINCIPAL"""

Tot_dat=[]
resp=Iniciar_Idealista()
centro="40.99181,-3.63716"
#Primera petcicion para saber el numero de páginas
datos=Hacer_Peticion(resp,1,centro)
if datos==999:
    print("Error al realizar primera peticion. Se aborta")
else:
    insert_many(datos['elementList'])


Tot_dat=Tot_dat.append(datos['elementList'])
""" Cada peticion devuelve una página, luego habrá que solicitar la numPage hasta llegar a totalPages
    Es decir, una petición por página
"""   
total=0
pag=2

while datos['totalPages'] > pag:
    
    datos=Hacer_Peticion(resp,pag,centro)
    if datos == 999:
        print("Error en peticiones.Se aborta")
        break
    else:

        insert_many(datos['elementList'])
        pag = pag + 1
        total = total + len(datos['elementList'])

print("Elementos insertados ", total)

"""
Idealista=pd.DataFrame()
#Idealista=pd.DataFrame.from_dict(datos['elementList'])
Idealista=Idealista.append(pd.DataFrame.from_dict(datos['elementList']))

#print(Idealista)

#Vuelca el JSON a un fichero
Idealista.to_json(path_or_buf="C:/Users/carlos/Desktop/BIGDATA/Python/IdealistaOffice3.json",orient="index")

# Para leer los json de ficheros en disco
casas=open("C:/Users/carlos/Desktop/BIGDATA/Python/Idealista.json").read()
casas_json=json.loads(casas)

"""
    
