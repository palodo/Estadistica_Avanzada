from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import matplotlib
matplotlib.use('Agg')  # Usar backend Agg (no GUI)
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import time

def obtener_tiros(equipo, enlace_jugador, url):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        equipo_str = f"t{equipo}"

        fila_jugador = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[@class='nombre jugador']/a[@href='" + enlace_jugador + "']/../.."))
        )
        dorsal = fila_jugador.find_element(By.XPATH, "./td[@class='dorsal']").text
        dorsal_str = f"p-{dorsal}"
        print(f"Dorsal encontrado: {dorsal_str}")

        shot_chart_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='btn-tab'][@data-action='shotchart']"))
        )
        try:
            shot_chart_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", shot_chart_button)
        print(f"Buscando tiros para {equipo_str}, dorsal {dorsal_str}...")

        driver.implicitly_wait(2)
        shoots = driver.find_elements(By.CLASS_NAME, "shoot")
        tiros = []

        for shoot in shoots:
            if shoot.value_of_css_property("display") == "block":
                classes = shoot.get_attribute("class").split()
                if equipo_str in classes and dorsal_str in classes:
                    style = shoot.get_attribute("style")
                    top = float(style.split("top: ")[1].split("%")[0])
                    left = float(style.split("left: ")[1].split("%")[0])
                    success = "Anotado" if "success1" in classes else "Fallado"
                    quarter = next((c for c in classes if c.startswith("q-")), "Desconocido")
                    tiros.append({
                        "posicion": (left, top),
                        "resultado": success,
                        "cuarto": quarter
                    })
        print("Tiros obtenidos")
        return tiros
    finally:
        driver.quit()

def dibujar_tiros(tiros, imagen_cancha="court.png", output_file="shot_chart.png"):
    """
    Dibuja los tiros en una imagen de una cancha de baloncesto y guarda el resultado.
    
    Parámetros:
    - tiros (list): Lista de diccionarios con los tiros (posición, resultado, cuarto).
    - imagen_cancha (str): Ruta a la imagen de la cancha.
    - output_file (str): Nombre del archivo donde se guardará el gráfico.
    """
    # Cargar la imagen de la cancha
    img = Image.open(imagen_cancha)
    img_array = np.array(img)

    # Crear una figura con matplotlib
    fig, ax = plt.subplots()
    ax.imshow(img_array)

    # Obtener las dimensiones de la imagen
    height, width, _ = img_array.shape

    # Dibujar cada tiro
    for tiro in tiros:
        left, top = tiro["posicion"]
        resultado = tiro["resultado"]

        # Convertir porcentajes a píxeles
        x = (left / 100) * width
        y = (top / 100) * height

        # Color según el resultado
        color = 'green' if resultado == "Anotado" else 'red'
        marker = 'o' if resultado == "Anotado" else 'x'

        # Dibujar el punto
        ax.plot(x, y, marker=marker, color=color, markersize=10, markeredgewidth=2)

    # Configurar el gráfico
    ax.set_xticks([])
    ax.set_yticks([])

    # Guardar el gráfico como imagen
    plt.savefig(output_file, bbox_inches='tight')
    plt.close(fig)  # Cerrar la figura para liberar memoria
    print(f"Gráfico guardado como {output_file}")



def convertir_enlace_jugador(enlace):
    """
    Convierte un enlace de jugador del formato 'https://baloncestoenvivo.feb.es/Jugador.aspx?i=951964&c=2165978'
    al formato 'https://baloncestoenvivo.feb.es/Jugador.aspx?i=951964&c=2165978&med=0'.
    
    Parámetros:
    - enlace (str): Enlace en el formato original.
    
    Devuelve:
    - str: Enlace en el formato esperado.
    """
    
        
    # Construir el nuevo enlace
    nuevo_enlace = f"{enlace}&med=0"
    return nuevo_enlace
    
    
def convertir_enlace_partido(enlace):
    """
    Convierte un enlace de partido del formato 'https://baloncestoenvivo.feb.es/Partido.aspx?p=2415141'
    al formato 'https://baloncestoenvivo.feb.es/partido/2415141'.
    
    Parámetros:
    - enlace (str): Enlace en el formato original.
    
    Devuelve:
    - str: Enlace en el formato esperado.
    """
    try:
        # Extraer el valor de 'p' del enlace
        id_partido = enlace.split('?p=')[1]
        
        # Construir el nuevo enlace
        nuevo_enlace = f"https://baloncestoenvivo.feb.es/partido/{id_partido}"
        return nuevo_enlace
    except Exception as e:
        print(f"Error al convertir el enlace del partido {enlace}: {e}")
        return enlace  # Devolver el enlace original si hay un error
    

    