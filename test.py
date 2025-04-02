import streamlit as st
import pandas as pd
from scrapping import obtener_equipos, obtener_pc_pj, obtener_id, obtener_estadisticas
from procesar import calcular_avanzadas, calcular_rendimiento_equipo, convertir_a_minutos_decimales, ranking_minutos, ranking_jugadores_mas_usados
from funcionesGUI import *
from jugador import *
from tiros_jugador import *

# Función para generar gráficos de tiros
def generar_grafico_tiros(lista_tiros, jugador, jornada=None, output_suffix=""):
    if lista_tiros:
        output_file = f"graficos_tiros/shot_chart_{jugador}{output_suffix}.png"
        dibujar_tiros(lista_tiros, "court.png", output_file)
        return output_file
    return None

def main():
    st.title('🏀 Estadística avanzada Tercera Feb')
    st.subheader("Desarrollado por Pablo López Domínguez")

    # Inicializar estado de sesión
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = None
    if 'uso_graph_generated' not in st.session_state:
        st.session_state.uso_graph_generated = False  # Bandera para controlar el gráfico de %USG

    url_feb = "https://baloncestoenvivo.feb.es/resultados/ligaeba/8/2024"
    equipos = obtener_equipos(url_feb)
    nombres_equipos = [equipo[0] for equipo in equipos]
    equipo_seleccionado = st.selectbox('Selecciona un equipo', [''] + nombres_equipos)

    if equipo_seleccionado:
        url_equipo = next(url for nombre, url in equipos if nombre == equipo_seleccionado)
        puntos_permitidos, partidos_jugados = obtener_pc_pj(url_feb, equipo_seleccionado)
        id_equipo = obtener_id(url_equipo)
        url_estadisticas = f"https://baloncestoenvivo.feb.es/estadisticasacumuladas/{id_equipo}"
        estadisticas = obtener_estadisticas(url_estadisticas)
        estadisticas_mostrar = estadisticas.drop(columns=["Enlace"])
        
        totales_equipo = estadisticas.iloc[-1]
        estadisticas = estadisticas.iloc[:-1]
        
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
        
        estadisticas['Minutos_decimal'] = estadisticas['Minutos'].apply(convertir_a_minutos_decimales)
        estadisticas_avanzadas = calcular_avanzadas(estadisticas.copy(), estadisticas_totales)
        estadisticas_rendimiento = calcular_rendimiento_equipo(estadisticas_totales, puntos_permitidos)

        estadisticas["Partidos"] = pd.to_numeric(estadisticas["Partidos"], errors="coerce")
        promedio = estadisticas.copy()
        columnas_a_dividir = promedio.columns.difference(["Jugador", "Minutos", "Enlace", "Fase", "Partidos"])
        promedio[columnas_a_dividir] = promedio[columnas_a_dividir].apply(pd.to_numeric, errors='coerce')
        promedio[columnas_a_dividir] = promedio[columnas_a_dividir].div(promedio["Partidos"], axis=0)

        r_minutos = ranking_minutos(promedio.copy()).head(5)
        r_uso = ranking_jugadores_mas_usados(estadisticas_avanzadas.copy(), promedio).head(5)

        st.header(f'Estadísticas del Equipo: {equipo_seleccionado}')
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Estadísticas de Jugadores', 'Estadísticas Avanzadas', 'Rendimiento del Equipo', 'Rankings', "Foto"])

        with tab1:
            st.subheader('Estadísticas Individuales')
            st.dataframe(estadisticas_mostrar, hide_index=True, use_container_width=True, column_config={
                "Jugador": st.column_config.Column(pinned="left")
            })

        with tab2:
            st.subheader('Estadísticas Avanzadas de Jugadores')
            show_advanced_stats(estadisticas_avanzadas)

        with tab3:
            st.subheader('Métricas de Rendimiento del Equipo')
            st.write(estadisticas_rendimiento)

        with tab4:
            st.subheader('Rankings')
            st.write('🕒 **Ranking por minutos jugados**')
            st.dataframe(r_minutos, hide_index=True, use_container_width=True, column_config={
                "Jugador": st.column_config.Column(pinned="left")
            })
            st.write('')
            st.write('📊 **Ranking por porcentaje de uso (USG%)**')
            st.dataframe(r_uso, hide_index=True, use_container_width=True, column_config={
                "Jugador": st.column_config.Column(pinned="left")
            })

            # Generar gráfico de %USG solo si no se ha generado antes y no estamos en tab5
            jugador1 = r_uso.iloc[0]['Jugador']
            enlace_jugador_uso = estadisticas[estadisticas['Jugador'] == jugador1]['Enlace'].iloc[0]
            enlace_jugador_uso = convertir_enlace_jugador(enlace_jugador_uso)
            jornada_uso = partidos_jugados

            if not st.session_state.uso_graph_generated and st.session_state.active_tab != "tab5":
                with st.spinner('Generando gráfico de tiros del jugador con más %USG...'):
                    lista_tiros_uso = []
                    for i in range(jornada_uso-2, jornada_uso+1):
                        enlace_partido_uso, numero_equipo_uso = obtener_link_partido(equipo_seleccionado, i)
                        enlace_partido_uso = convertir_enlace_partido(enlace_partido_uso)
                        if enlace_partido_uso:
                            lista_tiros_uso += obtener_tiros(numero_equipo_uso, enlace_jugador_uso, enlace_partido_uso)

                    output_file = generar_grafico_tiros(lista_tiros_uso, jugador1, output_suffix="_uso")
                    if output_file:
                        st.image(output_file, caption=f"Gráfico de Tiros - {jugador1}")
                        st.success("Gráfico generado correctamente.")
                        st.session_state.uso_graph_generated = True  # Marcar como generado
                    else:
                        st.error("No se encontraron tiros para este jugador.")
            elif st.session_state.uso_graph_generated:
                # Mostrar el gráfico ya generado sin recalcular
                output_file = f"graficos_tiros/shot_chart_{jugador1}_uso.png"
                st.image(output_file, caption=f"Gráfico de Tiros - {jugador1}")
                st.success("Gráfico cargado desde memoria.")

        with tab5:
            st.session_state.active_tab = "tab5"  # Marcar que estamos en tab5
            st.subheader('Gráfico de Tiros del Jugador')
            st.write("Selecciona un jugador y una jornada para ver su gráfico de tiros")

            jugador_seleccionado = st.selectbox('Selecciona un jugador', estadisticas['Jugador'].tolist())
            enlace_jugador = estadisticas[estadisticas['Jugador'] == jugador_seleccionado]['Enlace'].iloc[0]
            enlace_jugador = convertir_enlace_jugador(enlace_jugador)
            jornada = st.slider('Selecciona la jornada', min_value=1, max_value=22, value=22)

            if st.button('Generar Gráfico de Tiros'):
                with st.spinner('Generando gráfico de tiros...'):
                    enlace_partido, numero_equipo = obtener_link_partido(equipo_seleccionado, jornada)
                    enlace_partido = convertir_enlace_partido(enlace_partido)
                    if enlace_partido:
                        lista_tiros = obtener_tiros(numero_equipo, enlace_jugador, enlace_partido)
                        output_file = generar_grafico_tiros(lista_tiros, jugador_seleccionado, jornada)
                        if output_file:
                            st.image(output_file, caption=f"Gráfico de Tiros - {jugador_seleccionado} (Jornada {jornada})")
                            st.success("Gráfico generado correctamente.")
                        else:
                            st.error("No se encontraron tiros para este jugador en esta jornada.")
                    else:
                        st.error("No se pudo obtener el enlace del partido para la jornada seleccionada.")

if __name__ == "__main__":
    main()