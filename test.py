import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Importar funciones de los módulos originales
from scrapping import obtener_equipos, obtener_pc_pj, obtener_id, obtener_estadisticas
from procesar import calcular_avanzadas, calcular_rendimiento_equipo, convertir_a_minutos_decimales, ranking_minutos, ranking_jugadores_mas_usados
from funcionesGUI import *
from jugador import *
from tiros_jugador import *

#st.set_page_config(page_title="Mi App", layout="wide") # Configuración de la página de Streamlit

def main():
    st.title('🏀 Estadística avanzada Tercera Feb')
    st.subheader("Desarrollado por Pablo López Domínguez")

    
    # URL base para la liga
    url_feb = "https://baloncestoenvivo.feb.es/resultados/ligaeba/8/2024"
    
    # Obtener equipos
    equipos = obtener_equipos(url_feb)
    
    # Menú de selección de equipo
    nombres_equipos = [equipo[0] for equipo in equipos]
    equipo_seleccionado = st.selectbox('Selecciona un equipo', [''] + nombres_equipos)
    
    # Solo mostrar resultados si se ha seleccionado un equipo
    if equipo_seleccionado:
        # Encontrar la URL del equipo seleccionado
        url_equipo = next(url for nombre, url in equipos if nombre == equipo_seleccionado)
        
        # Obtener puntos permitidos y partidos jugados
        puntos_permitidos, partidos_jugados = obtener_pc_pj(url_feb, equipo_seleccionado)
        
        # Obtener ID del equipo
        id_equipo = obtener_id(url_equipo)
        
        # URL de estadísticas
        url_estadisticas = f"https://baloncestoenvivo.feb.es/estadisticasacumuladas/{id_equipo}"
        
        # Obtener estadísticas
        estadisticas = obtener_estadisticas(url_estadisticas)
        estadisticas_mostrar= estadisticas.drop(columns=["Enlace"])
        
        # Extraer la última fila como los totales del equipo
        totales_equipo = estadisticas.iloc[-1]
        estadisticas = estadisticas.iloc[:-1]
        
        # Preparar estadísticas totales del equipo
        estadisticas_totales = {
            'FGA': int(totales_equipo['T2'].split('/')[1]) + int(totales_equipo['T3'].split('/')[1]),
            'FTA': int(totales_equipo['TL'].split('/')[1]),
            'TOV': int(totales_equipo['BP']),
            'RT': int(totales_equipo['RT']),
            'AS': int(totales_equipo['AS']),
            'BR': int(totales_equipo['BR']),
            'PT': int(totales_equipo['Puntos']),
            'Minutos': partidos_jugados * 200
        }
        
        # Agregar columna de minutos decimales
        estadisticas['Minutos_decimal'] = estadisticas['Minutos'].apply(convertir_a_minutos_decimales)
        
        # Calcular estadísticas avanzadas
        estadisticas_avanzadas = calcular_avanzadas(estadisticas.copy(), estadisticas_totales)
        
        # Calcular rendimiento del equipo
        estadisticas_rendimiento = calcular_rendimiento_equipo(estadisticas_totales, puntos_permitidos)
        #CREAMOS promedios
    

        estadisticas["Partidos"] = pd.to_numeric(estadisticas["Partidos"], errors="coerce")

        promedio = estadisticas.copy()
        # Seleccionar las columnas que queremos dividir
        columnas_a_dividir = promedio.columns.difference(["Jugador","Minutos", "Enlace", "Fase", "Partidos"])

        # Convertir esas columnas a numérico
        promedio[columnas_a_dividir] = promedio[columnas_a_dividir].apply(pd.to_numeric, errors='coerce')

        #print(promedio.dtypes)

        # Crear un nuevo DataFrame llamado 'promedio' con los valores divididos
        
        promedio[columnas_a_dividir] = promedio[columnas_a_dividir].div(promedio["Partidos"], axis=0)

        #Calcular rankings

        r_minutos=ranking_minutos(promedio.copy()).head(5)
        r_uso=ranking_jugadores_mas_usados(estadisticas_avanzadas.copy(), promedio).head(5)
        
        # Mostrar resultados
        st.header(f'Estadísticas del Equipo: {equipo_seleccionado}')
        
        # Pestaña de estadísticas de jugadores
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Estadísticas de Jugadores', 'Estadísticas Avanzadas', 'Rendimiento del Equipo', 'Rankings', "foto"])
        
        with tab1:
            st.subheader('Estadísticas Individuales')
            st.dataframe(estadisticas_mostrar, hide_index=True,use_container_width=True, column_config={
            "Jugador": st.column_config.Column(pinned="left")  # Fijar la columna "Jugador"
        }) 
        
        with tab2:
            st.subheader('Estadísticas Avanzadas de Jugadores')
            # Usar la nueva función en lugar del código original
            show_advanced_stats(estadisticas_avanzadas)
        
        with tab3:
            st.subheader('Métricas de Rendimiento del Equipo')
            st.write(estadisticas_rendimiento)

        with tab4:
            st.subheader('Rankings')
    
            # Título para la primera tabla
            st.write('🕒 **Ranking por minutos jugados**')
            # o también puedes usar: st.subheader('Ranking por minutos jugados')
            st.dataframe(r_minutos,hide_index=True,use_container_width=True, column_config={
            "Jugador": st.column_config.Column(pinned="left")  # Fijar la columna "Jugador"
        })
    
            
            # Espaciador opcional
            st.write('')  # Añade un poco de espacio entre tablas
            
            # Título para la segunda tabla
            st.write('📊 **Ranking por porcentaje de uso (USG%)**')
            # o también puedes usar: st.subheader('Ranking por porcentaje de uso (USG%)')
            st.dataframe(r_uso,hide_index=True,use_container_width=True, column_config={
            "Jugador": st.column_config.Column(pinned="left")  # Fijar la columna "Jugador"
        })
            jugador1 = r_uso.iloc[0]['Jugador'] #jugador seleccionado
            print(jugador1)
            enlace_jugador_uso = estadisticas[estadisticas['Jugador'] == jugador1]['Enlace'].iloc[0]
            enlace_jugador_uso=convertir_enlace_jugador(enlace_jugador_uso)#Le añado el &med=0
            print(enlace_jugador_uso)
            jornada_uso=partidos_jugados
            lista_tiros_uso=[]

            with st.spinner('Generando gráfico de tiros del jugador con más %USG...'):
                for i in range(jornada_uso-2,jornada_uso+1):
                    #print(i)
                    enlace_partido_uso,numero_equipo_uso = obtener_link_partido(equipo_seleccionado, i)
                    enlace_partido_uso=convertir_enlace_partido(enlace_partido_uso)
                    if enlace_partido_uso:
                        # Obtener los tiros del jugador
                        lista_tiros_uso += obtener_tiros(numero_equipo_uso, enlace_jugador_uso, enlace_partido_uso)

                if lista_tiros_uso:
                    
                    # Generar el gráfico de tiros
                    output_file = f"graficos_tiros/shot_chart_uso.png"
                    dibujar_tiros(lista_tiros_uso, "court.png", output_file)

                    # Mostrar el gráfico en Streamlit
                    st.image(output_file, caption=f"Gráfico de Tiros - {jugador1}")
                    st.success("Gráfico generado correctamente.")
                else:
                    st.error("No se encontraron tiros para este jugador.")


        with tab5:
            st.subheader('Gráfico de Tiros del Jugador')
            st.write("Selecciona un jugador y una jornada para ver su gráfico de tiros")

            # Obtener el nombre del jugador seleccionado
            jugador_seleccionado = st.selectbox('Selecciona un jugador', estadisticas['Jugador'].tolist())

            # Obtener el enlace del jugador seleccionado
            enlace_jugador = estadisticas[estadisticas['Jugador'] == jugador_seleccionado]['Enlace'].iloc[0]
            enlace_jugador=convertir_enlace_jugador(enlace_jugador)#Le añado el &med=0
            #print(enlace_jugador)
            # Seleccionar la jornada
            jornada = st.slider('Selecciona la jornada', min_value=1, max_value=22, value=22)

            # Botón para generar el gráfico
            if st.button('Generar Gráfico de Tiros'):
                with st.spinner('Generando gráfico de tiros...'):
                    # Obtener el enlace del partido para la jornada seleccionada
                    
                    enlace_partido,numero_equipo = obtener_link_partido(equipo_seleccionado, jornada)
                    enlace_partido=convertir_enlace_partido(enlace_partido)
                    if enlace_partido:
                        # Obtener los tiros del jugador
                        lista_tiros = obtener_tiros(numero_equipo, enlace_jugador, enlace_partido)

                        if lista_tiros:
                            # Generar el gráfico de tiros
                            output_file = f"graficos_tiros/shot_chart_{jugador_seleccionado}_{jornada}.png"
                            dibujar_tiros(lista_tiros, "court.png", output_file)

                            # Mostrar el gráfico en Streamlit
                            st.image(output_file, caption=f"Gráfico de Tiros - {jugador_seleccionado} (Jornada {jornada})")
                            st.success("Gráfico generado correctamente.")
                        else:
                            st.error("No se encontraron tiros para este jugador en esta jornada.")
                    else:
                        st.error("No se pudo obtener el enlace del partido para la jornada seleccionada.")

    

if __name__ == "__main__":
    main()