from bs4 import BeautifulSoup
import requests
import pandas as pd

def obtener_equipos(url):
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    
    equipos = []
    for fila in soup.select('#_ctl0_MainContentPlaceHolderMaster_clasificacionDataGrid tr')[1:]:  #Vamos a la tabla de clasificación para obtener los equipos
        #print(fila)
        enlace = fila.find('a')
        if enlace:
            nombre = enlace.text.strip()
            url_equipo = enlace['href']
            equipos.append((nombre, url_equipo))
    return equipos

def obtener_pc_pj(url, nombre):
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    
    equipos = []
    for fila in soup.select('#_ctl0_MainContentPlaceHolderMaster_clasificacionDataGrid tr')[1:]:
        enlace = fila.find('a')
        nombre_equipo = enlace.get_text(strip=True)
        if nombre == nombre_equipo:
            celdas = fila.find_all('td')
            puntos_en_contra = int(celdas[6].text.strip())
            partidos_jugados = int(celdas[2].text.strip())
    return puntos_en_contra, partidos_jugados



def mostrar_menu(equipos):
    print("Selecciona un equipo para analizar:")
    for i, (nombre, _) in enumerate(equipos, start=1):
        print(f"{i}. {nombre}")
    
    eleccion = int(input("Ingresa el número del equipo: ")) - 1
    return equipos[eleccion]




def obtener_id(url_equipo):
    codigo_equipo = url_equipo.split("i=")[-1]
    return codigo_equipo


def obtener_estadisticas(url):
    # Realizamos la solicitud a la página
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Inicializamos una lista para almacenar los datos de los jugadores
        jugadores_data = []

        # Buscamos todas las filas de la tabla con las estadísticas (ignoramos la cabecera)
        rows = soup.find_all("tr")[2:]  # Omite las primeras filas (cabecera y otras)

        for row in rows:
            cols = row.find_all("td")

            if len(cols) > 0:  # Verifica que la fila tenga columnas
                nombre_jugador = cols[0].get_text(strip=True)
                enlace_jugador = cols[0].find("a")["href"] if cols[0].find("a") else None
                fase = cols[1].get_text(strip=True)
                partidos = cols[2].get_text(strip=True)
                minutos = cols[3].get_text(strip=True)
                puntos = cols[4].get_text(strip=True)
                tiros_dos = cols[5].get_text(strip=False).split()[0]
                tiros_tres = cols[6].get_text(strip=False).split()[0]
                tiros_campo = cols[7].get_text(strip=False).split()[0]
                tiros_libres = cols[8].get_text(strip=False).split()[0]
                rebotes_ofensivos = cols[9].get_text(strip=True)
                rebotes_defensivos = cols[10].get_text(strip=True)
                rebotes_totales = cols[11].get_text(strip=True)
                asistencias = cols[12].get_text(strip=True)
                recuperaciones = cols[13].get_text(strip=True)
                perdidas = cols[14].get_text(strip=True)
                tapones_favor = cols[15].get_text(strip=True)
                tapones_contra = cols[16].get_text(strip=True)
                mates = cols[17].get_text(strip=True)
                faltas_cometidas = cols[18].get_text(strip=True)
                faltas_recibidas = cols[19].get_text(strip=True)
                valoracion = cols[20].get_text(strip=True)

                # Añadimos los datos de la fila a la lista de jugadores
                jugadores_data.append([
                    nombre_jugador, 
                    enlace_jugador, 
                    fase, 
                    partidos, 
                    minutos, 
                    puntos, 
                    tiros_dos, 
                    tiros_tres, 
                    tiros_campo, 
                    tiros_libres, 
                    rebotes_ofensivos, 
                    rebotes_defensivos, 
                    rebotes_totales, 
                    asistencias, 
                    recuperaciones, 
                    perdidas, 
                    tapones_favor, 
                    tapones_contra, 
                    mates, 
                    faltas_cometidas, 
                    faltas_recibidas, 
                    valoracion
                ])

        # Creamos el DataFrame
        df = pd.DataFrame(jugadores_data, columns=[
            "Jugador", "Enlace", "Fase", "Partidos", "Minutos", "Puntos", "T2", "T3", "TC", "TL", 
            "RO", "RD", "RT", "AS", "BR", "BP", "TapF", "TapC", "MT", "FC", "FR", "Valoración"
        ])
        #print(df)
        return df

    else:
        print(f"Error al obtener las estadísticas: {response.status_code}")
        return None