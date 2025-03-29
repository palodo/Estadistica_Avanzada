import streamlit as st
import pandas as pd
def show_team_metrics(estadisticas_rendimiento):
    """
    Muestra las métricas de rendimiento del equipo de forma estética con explicaciones.
    """
    # Crear columnas para mostrar las métricas en formato de tarjetas
    col1, col2, col3 = st.columns(3)
    
    # Definir colores para las métricas (hex codes)
    ritmo_color = "#3498db"  # Azul
    oer_color = "#2ecc71"    # Verde
    der_color = "#e74c3c"    # Rojo
    
    # Obtener valores redondeados
    ritmo = round(estadisticas_rendimiento['Ritmo'], 1)
    oer = round(estadisticas_rendimiento['OER'], 1)
    der = round(estadisticas_rendimiento['DER'], 1)
    
    # Métricas con estilo mejorado
    with col1:
        st.markdown(f"""
        <div style="background-color:{ritmo_color}20; padding:15px; border-radius:10px; border:1px solid {ritmo_color};">
            <h3 style="color:{ritmo_color}; text-align:center; margin:0;">{ritmo}</h3>
            <h4 style="text-align:center; margin:5px 0;">Ritmo (Pace)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size:0.9em; margin-top:8px;">
        Representa el número de posesiones que el equipo realiza por cada 100 minutos de juego. Un valor más alto indica un estilo de juego más rápido.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color:{oer_color}20; padding:15px; border-radius:10px; border:1px solid {oer_color};">
            <h3 style="color:{oer_color}; text-align:center; margin:0;">{oer}</h3>
            <h4 style="text-align:center; margin:5px 0;">OER (Ofensiva)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size:0.9em; margin-top:8px;">
        Eficiencia Ofensiva: puntos anotados por cada 100 posesiones. Mide la calidad del ataque del equipo independientemente del ritmo.
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color:{der_color}20; padding:15px; border-radius:10px; border:1px solid {der_color};">
            <h3 style="color:{der_color}; text-align:center; margin:0;">{der}</h3>
            <h4 style="text-align:center; margin:5px 0;">DER (Defensiva)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size:0.9em; margin-top:8px;">
        Eficiencia Defensiva: puntos permitidos por cada 100 posesiones. Valores más bajos indican mejor defensa.
        </div>
        """, unsafe_allow_html=True)
    
    # Añadir un separador
    st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)
    
    # Interpretación general
    st.markdown("""
    ### Interpretación de las métricas
    
    **Contexto de las métricas:**
    
    - **Ritmo (Pace)**: 
      - < 80: Equipo de ritmo lento
      - 80-95: Ritmo moderado
      - > 95: Equipo de ritmo rápido
    
    - **OER** (Ofensiva):
      - < 100: Ofensiva por debajo del promedio
      - 100-110: Ofensiva promedio
      - > 110: Ofensiva eficiente
    
    - **DER** (Defensiva):
      - < 100: Defensa eficiente
      - 100-110: Defensa promedio
      - > 110: Defensa por debajo del promedio
    
    *Nota: Un buen equipo generalmente tiene un OER alto y un DER bajo.*
    """)
    
    # Visualización comparativa con gráfica horizontal
    st.markdown("### Comparativa OER vs DER")
    
    # Diferencia neta (positiva es buena)
    net_rating = oer - der
    
    # Color según si el net rating es positivo o negativo
    net_color = "#2ecc71" if net_rating > 0 else "#e74c3c"
    
    # Mostrar el diferencial
    st.markdown(f"""
    <div style="display:flex; align-items:center; margin:10px 0;">
        <div style="width:120px;"><strong>Diferencial:</strong></div>
        <div style="background-color:{net_color}; color:white; padding:6px 15px; border-radius:5px; font-weight:bold;">{net_rating:+.1f}</div>
        <div style="margin-left:10px; font-size:0.9em; color:{'#2ecc71' if net_rating > 0 else '#e74c3c'};">
            {"Equipo con balance positivo" if net_rating > 0 else "Equipo con balance negativo"}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Barras para visualizar OER y DER
    max_value = max(oer, der) * 1.1  # Dar un poco de margen
    
    st.markdown(f"""
    <div style="margin:15px 0; background-color:#f1f1f1; border-radius:5px; padding:2px;">
        <div style="background-color:{oer_color}; width:{oer/max_value*100}%; height:25px; border-radius:5px; color:white; 
                  display:flex; align-items:center; padding-left:10px; font-weight:bold;">
            OER: {oer}
        </div>
    </div>
    
    <div style="margin:15px 0; background-color:#f1f1f1; border-radius:5px; padding:2px;">
        <div style="background-color:{der_color}; width:{der/max_value*100}%; height:25px; border-radius:5px; color:white; 
                  display:flex; align-items:center; padding-left:10px; font-weight:bold;">
            DER: {der}
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_advanced_stats(estadisticas_avanzadas):
    """
    Muestra las estadísticas avanzadas de jugadores con explicaciones.
    """
    # Crear un nuevo DataFrame solo con las columnas que queremos mostrar
    df_avanzadas = pd.DataFrame({
        'Jugador': estadisticas_avanzadas['Jugador'],
        'USG%': estadisticas_avanzadas['USG%'].round(1),
        'eFG%': estadisticas_avanzadas['eFG%'].round(1),
        'eTL': estadisticas_avanzadas['eTL'].round(2),
        'eT2': estadisticas_avanzadas['eT2'].round(2),
        'eT3': estadisticas_avanzadas['eT3'].round(2)
    })
    
    # Mostrar el DataFrame
    st.dataframe(df_avanzadas)
    
    # Explicación de las métricas
    st.markdown("### Explicación de las métricas avanzadas")
    
    # Crear explicaciones con expansores para no ocupar demasiado espacio
    with st.expander("🔍 ¿Qué es USG% (Porcentaje de uso)?"):
        st.markdown("""
        El **Porcentaje de Uso (USG%)** indica la proporción de jugadas ofensivas del equipo que finalizan con la acción de un jugador específico mientras está en cancha.
        
        **Fórmula:**
        ```
        USG% = 100 × [(FGA + 0.44 × FTA + TOV) × (Team Minutes/5)] / [(Player Minutes) × (Team FGA + 0.44 × Team FTA + Team TOV)]
        ```
        
        **Interpretación:**
        - 15-20%: Jugador de rol complementario
        - 20-25%: Contribuyente importante
        - 25-30%: Jugador principal
        - >30%: Estrella del equipo, pieza fundamental en la ofensiva
        """)
    
    with st.expander("🏀 ¿Qué es eFG% (Porcentaje efectivo de tiro)?"):
        st.markdown("""
        El **Porcentaje Efectivo de Tiro (eFG%)** ajusta el porcentaje de tiro tradicional para considerar que los tiros de 3 puntos valen más que los tiros de 2 puntos.
        
        **Fórmula:**
        ```
        eFG% = (FGM + 0.5 × 3PM) / FGA
        ```
        
        **Interpretación:**
        - <45%: Tirador deficiente
        - 45-50%: Tirador promedio
        - 50-55%: Buen tirador
        - >55%: Excelente tirador
        """)
    
    with st.expander("🎯 ¿Qué son eTL, eT2 y eT3?"):
        st.markdown("""
        Estas métricas miden la eficiencia de diferentes tipos de tiros en términos de puntos por intento.
        
        **eTL (Eficiencia en Tiros Libres):**
        ```
        eTL = Tiros Libres Convertidos / Total Tiros Libres Intentados
        ```
        Un valor de 1.0 significa un 100% de efectividad (todos los tiros libres acertados).
        
        **eT2 (Eficiencia en Tiros de 2 Puntos):**
        ```
        eT2 = (Tiros de 2 Convertidos × 2) / Total Tiros de 2 Intentados
        ```
        Un valor de 2.0 significa un 100% de efectividad (todos los tiros de 2 acertados).
        
        **eT3 (Eficiencia en Tiros de 3 Puntos):**
        ```
        eT3 = (Tiros de 3 Convertidos × 3) / Total Tiros de 3 Intentados
        ```
        Un valor de 3.0 significa un 100% de efectividad (todos los tiros de 3 acertados).
        
        **Comparativa habitual:**
        - Un eT2 promedio ronda 0.95-1.05 puntos por intento
        - Un eT3 promedio ronda 0.90-1.10 puntos por intento
        
        Si el eT3 de un jugador es superior a su eT2, generalmente es más eficiente que lance triples.
        """)


