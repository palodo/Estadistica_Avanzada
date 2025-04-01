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

def obtener_tiros(equipo, enlace_jugador, url="https://baloncestoenvivo.feb.es/partido/2415141"):
    """
    Obtiene una lista de tiros para un equipo y jugador específico usando su enlace como ID.
    
    Parámetros:
    - equipo (int): 0 para Equipo 0 (t0), 1 para Equipo 1 (t1).
    - enlace_jugador (str): URL del jugador como identificador único.
    - url (str): URL del partido (por defecto: https://baloncestoenvivo.feb.es/partido/2415141).
    
    Devuelve:
    - list: Lista de diccionarios con los tiros (posición, resultado, cuarto).
    """
    driver = webdriver.Chrome()
    driver.get(url)
    equipo_str = f"t{equipo}"

    # Paso 1: Obtener el dorsal desde la tabla
    try:
        fila_jugador = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[@class='nombre jugador']/a[@href='" + enlace_jugador + "']/../.."))
        )
        dorsal = fila_jugador.find_element(By.XPATH, "./td[@class='dorsal']").text
        dorsal_str = f"p-{dorsal}"
        print(f"Dorsal encontrado: {dorsal_str}")
    except Exception as e:
        print(f"No se pudo obtener el dorsal para el enlace {enlace_jugador}: {e}")
        driver.quit()
        return []

    # Paso 2: Ir al "Gráfico de Tiro"
    try:
        shot_chart_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='btn-tab'][@data-action='shotchart']"))
        )
        try:
            shot_chart_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", shot_chart_button)
        print(f"Buscando tiros para {equipo_str}, dorsal {dorsal_str}...")
    except Exception as e:
        print("No se pudo encontrar o clicar el botón 'Gráfico de Tiro':", e)
        driver.quit()
        return []

    # Esperar a que el gráfico cargue
    driver.implicitly_wait(2)

    # Extraer todos los elementos "shoot"
    shoots = driver.find_elements(By.CLASS_NAME, "shoot")
    tiros = []

    # Filtrar y procesar los tiros
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

    driver.quit()
    return tiros

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
    ax.set_title("Gráfico de Tiros")

    # Guardar el gráfico como imagen
    plt.savefig(output_file, bbox_inches='tight')
    plt.close(fig)  # Cerrar la figura para liberar memoria
    print(f"Gráfico guardado como {output_file}")

# Ejemplo de uso
if __name__ == "__main__":
    equipo = 0  # Equipo 0 (t0)
    enlace_jugador = "https://baloncestoenvivo.feb.es/Jugador.aspx?i=951964&c=1901880&med=0"  # P. LOPEZ DOMINGUEZ
    url_partido = "https://baloncestoenvivo.feb.es/partido/2415141"
    
    # Obtener los tiros
    lista_tiros = obtener_tiros(equipo, enlace_jugador, url_partido)
    
    if lista_tiros:
        print(f"Tiros encontrados para Equipo {equipo}, Jugador con enlace {enlace_jugador}:")
        for tiro in lista_tiros:
            print(f"Posición: {tiro['posicion']}, Resultado: {tiro['resultado']}, Cuarto: {tiro['cuarto']}")
        
        # Dibujar los tiros en la cancha y guardar el gráfico
        dibujar_tiros(lista_tiros, "court.png", "shot_chart.png")
    else:
        print("No se encontraron tiros o hubo un error.")



