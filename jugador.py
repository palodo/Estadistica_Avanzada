from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup

def obtener_link_partido(equipo_nombre, jornada_numero):
    """
    Busca el link del partido de un equipo en una jornada específica del grupo E-A.
    
    Parámetros:
    - equipo_nombre (str): Nombre del equipo a buscar.
    - jornada_numero (int): Número de la jornada a buscar.

    Retorna:
    - str: URL del partido si se encuentra, None si no se encuentra.
    """

    # ------------------------
    # 🚀 Obtener el HTML con Selenium
    # ------------------------
    driver = webdriver.Chrome()

    # Página del calendario de la FEB
    url = "https://baloncestoenvivo.feb.es/calendario/tercerafeb/3/2024"
    driver.get(url)
    time.sleep(3)  # Esperar a que cargue la página

    # Seleccionar el grupo "E-A"
    select_element = driver.find_element(By.ID, "_ctl0_MainContentPlaceHolderMaster_gruposDropDownList")
    select = Select(select_element)
    select.select_by_value("86387")  # Código del grupo "E-A"
    time.sleep(3)  # Esperar la actualización

    # Obtener el HTML después de la selección
    html = driver.page_source

    # Cerrar Selenium, ya no lo necesitamos
    driver.quit()

    # ------------------------
    # 🔍 Procesar con BeautifulSoup
    # ------------------------

    # Cargar el HTML en BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Buscar la jornada específica
    jornada_texto = f"Jornada {jornada_numero}"
    jornada_element = None

    for titulo in soup.find_all("h1", class_="titulo-modulo"):
        if jornada_texto in titulo.text:
            jornada_element = titulo
            break

    if not jornada_element:
        print(f"❌ No se encontró la {jornada_texto}")
        return None

    # Encontrar la tabla de partidos justo después de la jornada encontrada
    tabla_partidos = jornada_element.find_next("table")

    # Buscar el equipo en la jornada
    partidos = tabla_partidos.find_all("tr")

    for partido in partidos:
        equipo_local = partido.find("td", class_="equipo local")
        equipo_visitante = partido.find("td", class_="equipo visitante")

        nombre_local = equipo_local.text.strip() if equipo_local else ""
        nombre_visitante = equipo_visitante.text.strip() if equipo_visitante else ""

        if equipo_nombre in [nombre_local, nombre_visitante]:
            resultado = partido.find("td", class_="resultado")
            link_resultado = resultado.find("a")["href"]
            url_partido = f"{link_resultado}"
            return url_partido

    print(f"❌ No se encontró ningún partido para {equipo_nombre} en {jornada_texto}")
    return None

# ------------------------
# 🎯 Prueba de la función
# ------------------------

equipo = "NB TORRENT"
jornada = 22

link = obtener_link_partido(equipo, jornada)
if link:
    print(f"✅ Link del partido: {link}")
