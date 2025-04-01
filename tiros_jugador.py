from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

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
    # Configurar el navegador
    driver = webdriver.Chrome()
    driver.get(url)
    equipo_str = f"t{equipo}"

    # Paso 1: Obtener el dorsal desde la tabla (sin clic, asumiendo que "Ficha" es por defecto)
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
                top = float(style.split("top: ")[1].split("%")[0])  # Posición Y
                left = float(style.split("left: ")[1].split("%")[0])  # Posición X
                success = "Anotado" if "success1" in classes else "Fallado"
                quarter = next((c for c in classes if c.startswith("q-")), "Desconocido")

                tiros.append({
                    "posicion": (left, top),
                    "resultado": success,
                    "cuarto": quarter
                })

    driver.quit()
    return tiros

# Ejemplo de uso
if __name__ == "__main__":
    equipo = 0  # Equipo 0 (t0)
    enlace_jugador = "https://baloncestoenvivo.feb.es/Jugador.aspx?i=951964&c=1901880&med=0"  # P. LOPEZ DOMINGUEZ
    url_partido = "https://baloncestoenvivo.feb.es/partido/2415141"
    
    lista_tiros = obtener_tiros(equipo, enlace_jugador, url_partido)
    
    if lista_tiros:
        print(f"Tiros encontrados para Equipo {equipo}, Jugador con enlace {enlace_jugador}:")
        for tiro in lista_tiros:
            print(f"Posición: {tiro['posicion']}, Resultado: {tiro['resultado']}, Cuarto: {tiro['cuarto']}")
    else:
        print("No se encontraron tiros o hubo un error.")