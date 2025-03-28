#Carga de librerias

from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import timedelta


#Carga funciones

from scrapping import *


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


    

if __name__ == "__main__":
    main()