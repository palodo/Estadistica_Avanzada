#Carga de librerias

from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import timedelta



#Carga funciones

from scrapping import *
from procesar import *


def main():
    url_feb = "https://baloncestoenvivo.feb.es/resultados/ligaeba/8/2024"
    equipos = obtener_equipos(url_feb)
    nombre_seleccionado, url_equipo = mostrar_menu(equipos)
    print(f"Has seleccionado: {nombre_seleccionado}")
    print(f"URL del equipo: {url_equipo}")

    id_equipo = obtener_id(url_equipo)
    url_estadisticas = f"https://baloncestoenvivo.feb.es/estadisticasacumuladas/{id_equipo}"
    estadisticas=obtener_estadisticas(url_estadisticas)
    print("Estadisticas obtenidas")
    #display(estadisticas) para mostrarla en un entorno jupyter
    #print(estadisticas)

    # Extraer la última fila como los totales del equipo
    totales_equipo = estadisticas.iloc[-1]
    estadisticas = estadisticas.iloc[:-1]

    
   


    # Convertir a un diccionario de valores clave
    estadisticas_totales = {
        'FGA': int(totales_equipo['T2'].split('/')[1]) + int(totales_equipo['T3'].split('/')[1]),
        'FTA': int(totales_equipo['TL'].split('/')[1]),
        'TOV': int(totales_equipo['BP']),
        'Minutos': 4400 #Para esto, se me ocurre coger en el web scrapping los partidos jugados del equipo(se puede ver en la
        #clasificación ) y multiplicarlo por 200.
    }
    #print(estadisticas_totales)
    estadisticas['Minutos_decimal'] = estadisticas['Minutos'].apply(convertir_a_minutos_decimales) #Creamos una columna llamada Minutos_decimal para
                                                                                                #tener el valor numérico
    estadisticas_avanzadas=calcular_usage_rate(estadisticas, estadisticas_totales)
    print("\n\n")
    print(estadisticas_avanzadas)




if __name__ == "__main__":
    main()