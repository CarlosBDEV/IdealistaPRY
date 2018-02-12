# -*- coding: utf-8 -*-
"""
Editor de Spyder

Scrape Idealista
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

url1 = 'https://www.idealista.com/alquiler-viviendas/madrid-madrid/mapa'
url2='https://www.idealista.com/venta-viviendas/madrid-madrid/mapa'
url3='https://www.idealista.com/venta-viviendas/madrid/zona-noroeste/mapa'
url4='https://www.idealista.com/venta-viviendas/madrid/zona-norte/mapa'
url5='https://www.idealista.com/venta-viviendas/madrid/zona-sur/mapa'
url6='https://www.idealista.com/venta-viviendas/madrid/corredor-del-henares/mapa'
url7='https://www.idealista.com/venta-viviendas/madrid/cuenca-del-alberche-guadarrama/mapa'
url8='https://www.idealista.com/venta-viviendas/madrid/cuenca-del-tajo-tajuna/mapa'

# Scrape the HTML at the url
def Scrapear(url):
    
    r = requests.get(url)
    r.status_code
    r.text

    soup = BeautifulSoup(r.text, 'html.parser')

    subdiv=soup.find_all(id='subdivisions')

    import re

    result=[]
    for i in re.findall(r'mapa">(.*?)</a>', str(subdiv)):
        o=i.split(' (')
        o[1]=o[1].replace(')','')
        o.append(re.findall('<h4>(.*?)</h4>',str(subdiv))[0])
        o.append('Venta')
        result.append(o)
    return result

Madrid=pd.DataFrame(Scrapear(url1), columns=['Distrito','Viviendas','Provincia', 'Tipo']) 
MadridTaj_v=pd.DataFrame(Scrapear(url8), columns=['Distrito','Viviendas','Provincia', 'Tipo']) 
MadridGua_v=pd.DataFrame(Scrapear(url7), columns=['Distrito','Viviendas','Provincia', 'Tipo']) 
MadridHe_v=pd.DataFrame(Scrapear(url6), columns=['Distrito','Viviendas','Provincia', 'Tipo']) 
MadridS_v=pd.DataFrame(Scrapear(url5), columns=['Distrito','Viviendas','Provincia', 'Tipo'])     
MadridN_v=pd.DataFrame(Scrapear(url4), columns=['Distrito','Viviendas','Provincia', 'Tipo'])      
MadridNE_v=pd.DataFrame(Scrapear(url3), columns=['Distrito','Viviendas','Provincia', 'Tipo'])     
Madrid_v=pd.DataFrame(Scrapear(url2), columns=['Distrito','Viviendas','Provincia', 'Tipo'])      


Idealista=pd.concat([Madrid,Madrid_v,MadridNE_v,MadridN_v,MadridS_v,MadridHe_v,MadridGua_v,MadridTaj_v]) 

from pandas import ExcelWriter

HojaEx=ExcelWriter('C:/Users/carlos/Desktop/Proyecto_CICE/ListaViviendasCM.xlsx')
Idealista.to_excel(HojaEx)
HojaEx.save()




