# -*- coding: utf-8 -*-
"""
Petición a Idealista
""" 
import datetime
import requests
import requests.auth
import base64
import pandas as pd
import pymongo
from pymongo import MongoClient
import json

#fecha de log
fech_log=datetime.datetime.now()
fech_log='{:%Y%m%d}'.format(fech_log)
# log file. Lo defino de modo escritura con posicionamiento final
file="C:/Users/carlos/Desktop/Proyecto_CICE/log_"+str(fech_log)+".txt"
log_file=open(file,'a')   

#Códigos proporcionados por Idealista

def Recoger_claves(User):
    
    connection = MongoClient("mongodb://localhost")
    
    # get a handle to the school database
    db = connection.Idealistas
    Usuarios = db.Usuarios
    
    
    try:
        doc=Usuarios.find({'User':User})
    except Exception as e:
        print( "Recoger_claves - Unexpected error:", type(e), e)
    
    if doc.count()>0:
        Lista=[doc[0]['nombre'],doc[0]['ApiKey'],doc[0]['Secret']]
    else: 
        Lista=[0,0,0]

    return Lista        



""" ARGANZUELA
arg1 'center':"40.396,-3.689" 1350m
arg2 'center':"40.402,-3.710" 500m
arg3 'center':"40.407,-3.719" 400m
"""


#concateno apikey y secret y convierto a base 64 según indicado por Idealista
#Asigno ContentType y GrantType según indicado por Idealista

ContentType='application/x-www-form-urlencoded'
grant_type='client_credentials&scope=write'


cont_peticiones=0

def Iniciar_Idealista(Apikey,Secret):
        
#Asigno variables para petición del Token
    Authorization=base64.b64decode(Apikey+':'+ Secret)
    
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
400 -Invalid value. Accepted values for operation are: sale, rent 
400 -operation is required 
404 -the locationId doesn't exist 
500 -server error 
"""

def Hacer_Peticion(r,pagina,centro,dist):
#paso headers y parámetros para petición get
    headerst={"Authorization":'bearer %s' %r.json()['access_token']}
    
    #obligatorios: country, operation, propertyType, locationId, distance ynnnnnnnnnnnn Center
    payload={'country':'es', 'operation':'sale', 'propertyType':'homes', 'numPage':1,
             'locationId':'0-EU-ES-28', 'center':"40.407,-3.719",'distance':400,'maxItems':50}
    
    payload['numPage']=pagina
    payload['center']=centro
    payload['distance']=dist
    #payload=ValidarParam(parametros)
            
#Hago petición
    resget=requests.post('https://api.idealista.com/3.5/es/search?', params=payload, headers=headerst)
    sc_peticion=resget.status_code#Recibo status 200
    
    if sc_peticion==200:
            
        datos=resget.json()
        #return datos
        log_file.write("Coordenadas de entrada... "+centro)
        log_file.write("Radio de busqueda........  "+str(dist))
        Resultados(datos)
        return datos
    else:
        print("Error ",sc_peticion," en la petición a la API")
        log_file.write("Error "+str(sc_peticion)+" en la petición a la API\n")
        return sc_peticion

        
def Resultados(datos):
    print(" **RESULTADOS LLAMADA**")    
    log_file.write(" **RESULTADOS LLAMADA**")
    e="Páginas devueltas: "+str(datos['totalPages'])
    print(e)
    log_file.write(e+'\n')  
    e="Elementos en total: "+str(datos['total'])
    print(e)
    log_file.write(e+'\n')    
    e=str(datos['itemsPerPage'])+ "elementos de la página "+str(datos['actualPage'])
    print(e )
    log_file.write(e+'\n')        

        
def insert_many(elementos):
    
    connection = MongoClient("mongodb://localhost")
    
    # get a handle to the school database
    db = connection.Idealistas
    Madrid = db.Madrid
    
    #formateamos la fecha el sistema
    fech_hora=datetime.datetime.now()
    fech_hora='{:%Y-%m-%d %H:%M:%S}'.format(fech_hora)
    #añadimos la fecha al documento
    for e in elementos:
        e['date']=fech_hora

    print (fech_hora,": Insertamos ", len(elementos)," elementos en " , Madrid)
    #people_to_insert = [andrew, richard]
    try:
        Madrid.insert_many(elementos, ordered=False)
    except Exception as e:
        print( "insert_many - Unexpected error:", type(e), e)

def insert_peticiones(user,n):
    connection = MongoClient("mongodb://localhost")
    
    # get a handle to the school database
    db = connection.Idealistas
    Pet = db.LogPeticion
    
    #formateamos la fecha el sistema
    fech_hora=datetime.datetime.now()
    fech_hora='{:%Y-%m-%d %H:%M:%S}'.format(fech_hora)
    #añadimos la fecha al documento
    element={'user':user,'date':fech_hora,'num_request':n}
    
    print (fech_hora,": Insertamos ", element," peticiones en LogPeticion")
    log_file.write(fech_hora+": Insertamos "+ str(element)+" peticiones en LogPeticion\n")
     
    try:
        Pet.insert_one(element)
        print('Llevas ',n,' peticiones.')
    except Exception as e:
        print( "insert_peticiones - Unexpected error:", type(e), e)


def LeerPeticiones(user):
   
    connection = MongoClient("mongodb://localhost")
    
    # get a handle to the school database
    db = connection.Idealistas
    Peticiones = db.LogPeticion
    
    try:
        p=Peticiones.find({'user':user}).sort('date',pymongo.DESCENDING).limit(1)
        print(p.count())
        if p.count()==0:
            print("Nuevo Usuario :",user)
            log_file.write("Nuevo Usuario :"+user)
            insert_peticiones(user,0)
            return 0
        
        else:
            return p[0]['num_request']
    except Exception as e:
        print( "LeerPeticiones - Unexpected error:", type(e), e)
        

def fecha():
     fech_hora=datetime.datetime.now()
     fech_hora='{:%Y-%m-%d %H:%M:%S}'.format(fech_hora)
     
     return fech_hora
     
      
   
"""PRINCIPAL"""
""" Cada peticion devuelve una página, luego habrá que solicitar la numPage hasta llegar a totalPages
    Es decir, una petición por página
"""  
def Main(centro,dist,usu):
     
 
    Tot_dat=[]
    ListaCLV=[]
    
    ListaCLV=Recoger_claves(usu)
    print(len(ListaCLV))
    Usuario=ListaCLV[0]
    ApiKey=ListaCLV[1]
    Secret=ListaCLV[2]    
    
    if Usuario==0:
        print("USUARIO INCORRECTO")
      
    else:
        #Si no existe el usuario lo inserta con 0 peticiones
        num_p=LeerPeticiones(Usuario)
        print('Usuario ',Usuario,' tiene ' ,num_p,' peticiones.')
        log_file.write('Usuario '+Usuario+' tiene ' +str(num_p)+' peticiones.\n')

        resp=Iniciar_Idealista(ApiKey,Secret)

#Primera petcicion para saber el numero de páginas

        datos=Hacer_Peticion(resp,1,centro,dist)
        num_p=num_p+1

        if datos==999:
            print("Error al realizar primera peticion. Se aborta")
            log_file.write("Error al realizar primera peticion. Se aborta\n")
        else:
    
            insert_many(datos['elementList'])

            total=0
            pag=2

            while datos['totalPages'] >= pag:
                
                datos=Hacer_Peticion(resp,pag,centro,dist)
                num_p=num_p+1
        
                if datos==500:
                    print(usu," llegó al limite de peticiones.Se inicializa")
                    log_file.write(usu+" llegó al limite de peticiones.Se inicializa\n")
                    insert_peticiones(Usuario,0)
                    break
                elif type(datos) != int:
            
                    insert_many(datos['elementList'])
                    pag=pag+1
                    total=total+len(datos['elementList'])
                else:
                    print(datos,".Error en peticiones.Se aborta")
                    log_file.write(str(datos)+".Error en peticiones.Se aborta\n")
                    insert_peticiones(Usuario,num_p)
                    break

            print("Elementos insertados ", total)
            log_file.write("Elementos insertados: "+ str(total)+"\n")
            insert_peticiones(Usuario,num_p)
    

def BorraDuplicados(distrito):
    
    connection = MongoClient("mongodb://localhost")
    
    # get a handle to the school database
    db = connection.Idealistas
    Madrid = db.Madrid
    r=0
    try:
        pisos=Madrid.aggregate([
         {'$match':{'district':distrito}},
         {'$group':{'_id':"$propertyCode",'num':{'$sum':1}}},
         {'$sort':{'num':-1}}])
        if pisos.alive:
            
            for p in pisos:
                #print(p)
                if p['num']>1:
                    print("repes ",p['_id'])
                    r=r+1
                    Madrid.delete_one({'propertyCode':p['_id']})
    
            print(" Borrados ",r," pisos duplicados")
        else:
            print("No hay datos que borrar")                    
    except Exception as e:
        print( "Unexpected error:", type(e), e)
        
def ExportarACSV():
    connection = MongoClient("mongodb://localhost")
    
    # get a handle to the school database
    db = connection.Idealistas
    Madrid = db.Madrid
    Ideal=pd.DataFrame()
    dict={}
    try:
        datos=Madrid.find({'operation':'sale'})
        
        for d in datos:
            print(d)
            Ideal=Ideal.append(d,ignore_index=True)
             
        Ideal.to_csv("C:/Users/carlos/Desktop/Proyecto_CICE/Descarga_venta.csv")
       
    except Exception as e:
        print( "Unexpected error:", type(e), e)


"""def AccesoATLAS():
     from bson.son import SON
     #esta lib se carga para poder utilizar maxDistance con el Near
    conection = MongoClient("mongodb://CarlosBA:resacas@cluster1-shard-00-00-gv1zu.mongodb.net:27017,cluster1-shard-00-01-gv1zu.mongodb.net:27017,cluster1-shard-00-02-gv1zu.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster1-shard-0&authSource=admin")
    
    db = conection.Idealistas
    Madrid=db.GeoMadrid
    Ideal=pd.DataFrame()
    dict={}
    query = {"location.coordinates": SON([("$near", [40.42739,-3.64379]),("$maxDistance", 0.001)])}
    try:
        datos=Madrid.find(query)
        for d in datos:
            #print(d)
            Ideal=Ideal.append(d,ignore_index=True)
             
        Ideal.to_csv("C:/Users/carlos/Desktop/Proyecto_CICE/Descarga_venta.csv")
       
    except Exception as e:
        print( "Unexpected error:", type(e), e)

"""   
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
    
