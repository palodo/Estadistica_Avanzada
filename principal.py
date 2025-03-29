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
    
    puntos_permitidos,partidos_jugados=obtener_pc_pj(url_feb,nombre_seleccionado)

    
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
        'FGA': int(totales_equipo['T2'].split('/')[1]) + int(totales_equipo['T3'].split('/')[1]), #podría haber cogido dirctmente de TC
        'FTA': int(totales_equipo['TL'].split('/')[1]),
        'TOV': int(totales_equipo['BP']),
        'RT':int(totales_equipo['RT']),
        'AS':int(totales_equipo['AS']),
        'BR':int(totales_equipo['BR']),
        'PT':int(totales_equipo['Puntos']),
        'Minutos': partidos_jugados*200 #Para esto, se me ocurre coger en el web scrapping los partidos jugados del equipo(se puede ver en la
        #clasificación ) y multiplicarlo por 200.
    }
    #print(estadisticas_totales)


    estadisticas['Minutos_decimal'] = estadisticas['Minutos'].apply(convertir_a_minutos_decimales) #Creamos una columna llamada Minutos_decimal para
                                                                                                #tener el valor numérico

    #CREAMOS promedios
    

    estadisticas["Partidos"] = pd.to_numeric(estadisticas["Partidos"], errors="coerce")

    promedio = estadisticas.copy()
    # Seleccionar las columnas que queremos dividir
    columnas_a_dividir = promedio.columns.difference(["Jugador","Minutos", "Enlace", "Fase", "Partidos"])

    # Convertir esas columnas a numérico
    promedio[columnas_a_dividir] = promedio[columnas_a_dividir].apply(pd.to_numeric, errors='coerce')

    print(promedio.dtypes)

    # Crear un nuevo DataFrame llamado 'promedio' con los valores divididos
    
    promedio[columnas_a_dividir] = promedio[columnas_a_dividir].div(promedio["Partidos"], axis=0)

    print(promedio)




    

    estadisticas_avanzadas=calcular_avanzadas(estadisticas, estadisticas_totales, min_partidos=partidos_jugados//3)#al menos han jugado 1/3 de los partidos
    print("\n\n")
    print(estadisticas_avanzadas)
    print("\n\n")

   
    estadisiticas_avanzadas_equipo=calcular_rendimiento_equipo(estadisticas_totales, puntos_permitidos)
    
    
    print(estadisiticas_avanzadas_equipo)



    r_minutos=ranking_minutos(promedio.copy()).head(5)
    r_uso=ranking_jugadores_mas_usados(estadisticas_avanzadas.copy(),promedio.copy()).head(5)
    print(r_uso)
    

    



if __name__ == "__main__":
    main()