import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Importar funciones de los módulos originales
from scrapping import obtener_equipos, obtener_pc_pj, obtener_id, obtener_estadisticas
from procesar import calcular_avanzadas, calcular_rendimiento_equipo, convertir_a_minutos_decimales

def main():
    st.title('🏀 Análisis de Estadísticas de Baloncesto')
    
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
        
        # Mostrar resultados
        st.header(f'Estadísticas del Equipo: {equipo_seleccionado}')
        
        # Pestaña de estadísticas de jugadores
        tab1, tab2, tab3 = st.tabs(['Estadísticas de Jugadores', 'Estadísticas Avanzadas', 'Rendimiento del Equipo'])
        
        with tab1:
            st.subheader('Estadísticas Individuales')
            st.dataframe(estadisticas_mostrar)
        
        with tab2:
            st.subheader('Estadísticas Avanzadas de Jugadores')
            # Crear un nuevo DataFrame solo con las columnas que queremos mostrar
            df_avanzadas = pd.DataFrame({
                'Jugador': estadisticas_avanzadas['Jugador'],
                'USG%': estadisticas_avanzadas['USG%'],
                'eFG%': estadisticas_avanzadas['eFG%'],
                'eTL': estadisticas_avanzadas['eTL'],
                'eT2': estadisticas_avanzadas['eT2'],
                'eT3': estadisticas_avanzadas['eT3']
            })
            st.dataframe(df_avanzadas)
        
        with tab3:
            st.subheader('Métricas de Rendimiento del Equipo')
            st.write(estadisticas_rendimiento)

if __name__ == "__main__":
    main()