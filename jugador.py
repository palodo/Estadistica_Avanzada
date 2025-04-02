import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup

# Archivo para persistir el caché
CACHE_FILE = "partidos_cache.json"

# Cargar caché desde archivo si existe
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

# Guardar caché en archivo
def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

# Caché en memoria
partidos_cache = load_cache()

def obtener_link_partido(equipo_nombre, jornada_numero):
    """
    Busca el link del partido de un equipo en una jornada específica del grupo E-A, usando caché si está disponible.
    
    Parámetros:
    - equipo_nombre (str): Nombre del equipo a buscar.
    - jornada_numero (int): Número de la jornada a buscar.

    Retorna:
    - tuple: (URL del partido, equipo (0 o 1)) si se encuentra, (None, None) si no se encuentra.
    """
    # Crear clave única para el caché
    cache_key = f"{equipo_nombre}_{jornada_numero}"

    # Verificar si el dato está en el caché
    if cache_key in partidos_cache:
        print(f"✅ Encontrado en caché: {cache_key}")
        return partidos_cache[cache_key]["url"], partidos_cache[cache_key]["team"]

    # Si no está en caché, realizar la consulta
    driver = webdriver.Chrome()
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
    driver.quit()

    # Procesar con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    jornada_texto = f"Jornada {jornada_numero}"

    jornada_element = None
    for titulo in soup.find_all("h1", class_="titulo-modulo"):
        if jornada_texto in titulo.text:
            jornada_element = titulo
            break

    if not jornada_element:
        print(f"❌ No se encontró la {jornada_texto}")
        return None, None

    tabla_partidos = jornada_element.find_next("table")
    partidos = tabla_partidos.find_all("tr")
    team = None

    for partido in partidos:
        equipo_local = partido.find("td", class_="equipo local")
        equipo_visitante = partido.find("td", class_="equipo visitante")

        nombre_local = equipo_local.text.strip() if equipo_local else ""
        nombre_visitante = equipo_visitante.text.strip() if equipo_visitante else ""
        if nombre_local == equipo_nombre:
            team = 0
        if nombre_visitante == equipo_nombre:
            team = 1

        if equipo_nombre in [nombre_local, nombre_visitante]:
            resultado = partido.find("td", class_="resultado")
            link_resultado = resultado.find("a")["href"]
            url_partido = f"{link_resultado}"

            # Guardar en caché
            partidos_cache[cache_key] = {"url": url_partido, "team": team}
            save_cache(partidos_cache)  # Persistir el caché
            print(f"✅ Añadido al caché: {cache_key}")
            return url_partido, team

    print(f"❌ No se encontró ningún partido para {equipo_nombre} en {jornada_texto}")
    return None, None