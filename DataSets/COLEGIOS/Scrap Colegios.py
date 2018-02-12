# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 19:25:02 2017

Obtenemos los datos estadisticos de cada centro, contenidos en los elementos
tablaDatos.grafica1(numero de alumnos) y tablaDatos.grafica3(Admision)
Y los datos ACADEMICOS contenidos en los elementos
tablaDatos.grafica6(Generales) y tablaDatos.grafica8 (ingles)

@author: carlos
"""

from selenium import webdriver
import pandas as pd
import time
#codigo = 28063751

#file="C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Madrid_Capital_TODOS_temp.xlsx"
file="C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Madrid_Municipios_TODOS.xlsx"
#file="C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Listado_BACHILLERATO_Madrid_Capital.xlsx"
fichero=pd.read_excel(file)

        
general=open('C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Notas_general.txt','w')
generalESO=open('C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Notas_generalESO.txt','w')
ingles=open('C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Notas_Idiomas.txt','w')
centro=[]
alumnos=open('C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Alumnos.txt','w')
admision=open('C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Admision.txt','w')
universidad=open('C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Universidad.txt','w')
driver = webdriver.Firefox()
for codigo in fichero['CODIGO CENTRO']:
    centro.append(codigo)


    driver.get('http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm?cdCentro='+str(codigo))


# Accedemos a la pestaña de datos ESTADISTICOS
    try:
        tab = driver.find_element_by_id( "solapastab1" )
        tab.click()
    except Exception as err:
        print('Error en tab Estadisticos',err)


    try:
        #NÚMERO DE ALUMNOS
        tablaA = driver.find_element_by_id('tablaDatos.grafica1').text
        alumnos.write(str(codigo)+";")
        alumnos.write(tablaA.replace('\n',';'))
        alumnos.write(";\n")
        #time.sleep(5)
        """for x in tablaA.split('\n'):
            print(tabla)
            if "Total" in x: 
                notas=x.split()
                alumnos.append([codigo,[notas[1],notas[2],notas[3],notas[4],notas[5]]])
         """                   
    except Exception as e:
        print("Error en notas generales ",e,".Continuo.")
    
    try:
        #PROCESO DE ADMISIÓN (solicitudes presentadas, admitidas, no admitidas
        tablaAd = driver.find_element_by_id('tablaDatos.grafica3').text
        admision.write(str(codigo)+";")
        admision.write(tablaAd.replace('\n',';'))
        admision.write(";\n")
       
                
    except Exception as e:
        print("Error en notas generales ",e,".Continuo.")


#Accedemos a la pestaña de datos ACADEMICOS
    try:
        tab = driver.find_element_by_id( "solapastab2" )
        tab.click()
    except Exception as err:
        print('Error en tab Academicos',err)

    try:
        #TITULACIÓN EN EDUCACIÓN SECUNDARIA
        tablaESO = driver.find_element_by_id('tablaDatos.grafica5').text
        generalESO.write(str(codigo)+";")
        generalESO.write(tablaESO.replace('\n',';'))
        generalESO.write(";\n")
        #time.sleep(5)
       
    except Exception as e:
        print("Error en notas generales ",e,".Continuo.")

    try:
        #PRUEBA DE CONOCIMIENTOS Y DESTREZAS INDISPENSABLES (CDI)
        tabla = driver.find_element_by_id('tablaDatos.grafica6').text
        general.write(str(codigo)+";")
        general.write(tabla.replace('\n',';'))
        general.write(";\n")
         
    except Exception as e:
        print("Error en notas generales ",e,".Continuo.")
    
    try:
        #PRUEBA EXTERNA EN CENTROS BILINGÜES
        tablaing= driver.find_element_by_id('tablaDatos.grafica8').text
        ingles.write(str(codigo)+";")
        ingles.write(tablaing.replace('\n',';'))
        ingles.write(";\n")
       
    except Exception as e:
        print("Error en notas Ingles ",e,".Continuo.")
    
    try:
        #PRUEBA DE ACCESO A LA UNIVERSIDAD (PAU)
        tablauni= driver.find_element_by_id('tablaDatos.grafica9').text
        universidad.write(str(codigo)+";")
        universidad.write(tablauni.replace('\n',';'))
        universidad.write(";\n")
       
    except Exception as e:
        print("Error en notas Acceso Universidad ",e,".Continuo.")
#print(tabla.split('\n'))

driver.quit()
general.close()
generalESO.close()
ingles.close()
alumnos.close()
admision.close()
universidad.close()


  cabeceras=['10-11','11-12','12-13','13-14','14-15']
  cabeceras=['12-13','13-14','14-15','15-16','16-17']
def grabar(lista,cabeceras):
    
    ind=[]
    val=[]
    for a in lista:
        ind.append(list(a.keys())[0])
        val.append(list(a.values())[0])
    
    return pd.DataFrame(val,index=ind,columns=cabeceras)

def Cruza():
    f1="C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Listado_PRIMARIA_Madrid.xlsx"
    f2="C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Notas_PRIMARIA.xlsx"
    f3="C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/Notas_ingles_PRIMARIA.xlsx"
    fichero1=pd.read_excel(f1,)
    fichero2=pd.read_excel(f2)
    fichero3=pd.read_excel(f3)
    
    salida=pd.merge(fichero1,fichero2,how='left',on='Centro')
    salida=pd.merge(salida,fichero3,how='left',on='Centro')
    
    salida.to_excel("C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/ConNotas.xlsx")
    
        
    
def GeolocalizaColegios(file):

    import googlemaps
    import pandas as pd
    
# Replace the API key below with a valid API key.
    gmaps = googlemaps.Client(key='AIzaSyAZLVrqkl-GTpXsmLKvAAWJ-LSpe3Fnqz8')

    file="C:/Users/carlos/Desktop/Proyecto_CICE/COLEGIOS/"+file

    fichero=pd.read_excel(file)

    Dir=fichero[["DOMICILIO","MUNICIPIO","b_latitud","b_longitud"]]

    b_latitud=[]
    b_longitud=[]
#cadena=Dir.iloc[0][0]+','+Dir.iloc[0][1]+','+Dir.iloc[0][2]
    n=0
    c_ok=0
    for d in Dir.values:
        cadena=str(Dir.iloc[n][0])+','+str(Dir.iloc[n][1])

        print(cadena)
        try:
            geocode_result = gmaps.geocode(cadena)
            if len(geocode_result)==0:
                b_latitud.append(0)    
                b_longitud.append(0)
                print("vacio")
            else:
                b_latitud.append(geocode_result[0]['geometry']['location']['lat'])
                b_longitud.append(geocode_result[0]['geometry']['location']['lng'])
                c_ok=c_ok+1

            n=n+1
        except Exception as e:
            print ("error ", e)
            fichero['b_latitud']=b_latitud  
            fichero['b_longitud']=b_longitud
    
            fichero.to_excel(file)

    print("Se han tratado "+str(n)+" direcciones")
    print(" - Se han recuperado "+str(c_ok)+" coordenadas.")
    print(" - Sin éxito "+str(n-c_ok))
    fichero['b_latitud']=b_latitud  
    fichero['b_longitud']=b_longitud
    
    fichero.to_excel(file)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
