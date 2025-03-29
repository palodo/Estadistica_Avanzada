import pandas as pd


def convertir_a_minutos_decimales(tiempo):
    """Convierte un string MM:SS a minutos en decimal."""
    if isinstance(tiempo, str) and ":" in tiempo:
        minutos, segundos = map(int, tiempo.split(":"))
        return minutos + segundos / 60


def calcular_avanzadas_old(df, total_team_stats):
    """
    Calcula el porcentaje de uso (USG%) de cada jugador en base a las estadísticas del equipo.
    :param df: DataFrame con estadísticas individuales
    :param total_team_stats: Diccionario con estadísticas totales del equipo
    :return: DataFrame con la columna USG% añadida
    """
    team_fga = total_team_stats['FGA']
    team_fta = total_team_stats['FTA']
    team_tov = total_team_stats['TOV']
    team_minutes = total_team_stats['Minutos']

    # Calcular USG% para cada jugador
    df['USG%'] = 100 * (
        (df['T2'].apply(lambda x: int(x.split('/')[1])) +  # Intentos de 2pts
        df['T3'].apply(lambda x: int(x.split('/')[1])) +  # Intentos de 3pts
        0.44 * df['TL'].apply(lambda x: int(x.split('/')[1])) +  # Intentos de TL ajustados
        df['BP'].astype(int)) * (team_minutes / 5)
    ) / (
        df['Minutos_decimal'].astype(int) * (team_fga + 0.44 * team_fta + team_tov)#aqui minutos tiene 
    )

    #eFG% (Effective Field Goal Percentage - Porcentaje de tiro efectivo)

    df['eFG%'] = ((df['T2'].apply(lambda x: int(x.split('/')[0])) + 
              1.5 * df['T3'].apply(lambda x: int(x.split('/')[0]))) /
              (df['T2'].apply(lambda x: int(x.split('/')[1])) + 
               df['T3'].apply(lambda x: int(x.split('/')[1])))) * 100
    


    #Seria interesante poner restricciones del estilo, haber tirado 2 o 3 triples por partido.

    # eTL   Calcula la eficiencia en tiros libres (Puntos por Intento de Tiro Libre)
    df['eTL'] = df['TL'].apply(lambda x: int(x.split('/')[0]))/df['TL'].apply(lambda x: int(x.split('/')[1]))

    #eT2    Calcula la eficiencia en tiros de 2 puntos (Puntos por Intento de Tiro de 2).
    df['eT2'] = df['T2'].apply(lambda x: int(x.split('/')[0]))*2/df['T2'].apply(lambda x: int(x.split('/')[1]))

    #eT3    Calcula la eficiencia en tiros de 3 puntos (Puntos por Intento de Tiro de 3).
    df['eT3'] = df['T3'].apply(lambda x: int(x.split('/')[0]))*3/df['T3'].apply(lambda x: int(x.split('/')[1]))


    
    return df




def calcular_rendimiento_equipo(totales_equipo, puntos_permitidos):
    """
    Calcula estadísticas avanzadas del equipo, incluyendo Ritmo, OER y DER.
    :param df: DataFrame con estadísticas individuales
    :param totales_equipo: Diccionario con estadísticas totales del equipo
    :param puntos_equipo: Puntos totales anotados por el equipo
    :param puntos_permitidos: Puntos totales permitidos por el equipo
    :return: Diccionario con estadísticas avanzadas del equipo
    """
    
    # Calcular Ritmo
    ritmo = ((totales_equipo['FGA'] + 0.44 * totales_equipo['FTA'] + totales_equipo['TOV']) * 100) / totales_equipo['Minutos']
    
    # Calcular OER (Offensive Efficiency Rating)
    oer = (totales_equipo['PT'] * 100) / (totales_equipo['FGA'] + 0.44 * totales_equipo['FTA'] + totales_equipo['TOV'])
    
    # Calcular DER (Defensive Efficiency Rating)
    der = (puntos_permitidos * 100) / (totales_equipo['FGA'] + 0.44 * totales_equipo['FTA'] + totales_equipo['TOV'])
    
    # Crear un diccionario con las estadísticas avanzadas del equipo
    estadisticas_avanzadas_equipo = {
        'Ritmo': ritmo,
        'OER': oer,
        'DER': der
    }
    
    return estadisticas_avanzadas_equipo



def ranking_minutos(estadisticas):
    
    
    # Ordenamos los jugadores por los minutos jugados en orden descendente
    ranking = estadisticas.sort_values(by="Minutos_decimal", ascending=False)
    
    # Seleccionamos las columnas relevantes
    ranking = ranking[['Jugador', 'Minutos_decimal', 'Puntos']]
    
    return ranking


def ranking_jugadores_mas_usados(estadisticas):
    
    
    # Ordenamos los jugadores por los minutos jugados en orden descendente
    ranking = estadisticas.sort_values(by="USG%", ascending=False)
    
    # Seleccionamos las columnas relevantes
    ranking = ranking[['Jugador','USG%', 'Minutos', 'Partidos']]
    
    return ranking

def calcular_avanzadas(df, total_team_stats, min_partidos=10):
    """
    Calcula el porcentaje de uso (USG%) de cada jugador en base a las estadísticas del equipo.
    :param df: DataFrame con estadísticas individuales
    :param total_team_stats: Diccionario con estadísticas totales del equipo
    :param min_partidos: Número mínimo de partidos para considerar las estadísticas
    :return: DataFrame con la columna USG% añadida
    """
    team_fga = total_team_stats['FGA']
    team_fta = total_team_stats['FTA']
    team_tov = total_team_stats['TOV']
    team_minutes = total_team_stats['Minutos']

    # Convertir 'Partidos' a numérico para asegurar que las comparaciones sean correctas
    df['Partidos'] = pd.to_numeric(df['Partidos'], errors='coerce')
    
    # Crear máscara para jugadores con suficientes partidos
    mascara_partidos = df['Partidos'] >= min_partidos
    
    # Inicializar columnas con NaN
    df['USG%'] = float('nan')
    df['eFG%'] = float('nan')
    df['eTL'] = float('nan')
    df['eT2'] = float('nan')
    df['eT3'] = float('nan')
    
    # Calcular USG% solo para jugadores con suficientes partidos
    df.loc[mascara_partidos, 'USG%'] = 100 * (
        (df.loc[mascara_partidos, 'T2'].apply(lambda x: int(x.split('/')[1])) +  # Intentos de 2pts
         df.loc[mascara_partidos, 'T3'].apply(lambda x: int(x.split('/')[1])) +  # Intentos de 3pts
         0.44 * df.loc[mascara_partidos, 'TL'].apply(lambda x: int(x.split('/')[1])) +  # Intentos de TL ajustados
         df.loc[mascara_partidos, 'BP'].astype(int)) * (team_minutes / 5)
    ) / (
        df.loc[mascara_partidos, 'Minutos_decimal'] * (team_fga + 0.44 * team_fta + team_tov)
    )

    # eFG% (Effective Field Goal Percentage - Porcentaje de tiro efectivo)
    df.loc[mascara_partidos, 'eFG%'] = ((
        df.loc[mascara_partidos, 'T2'].apply(lambda x: int(x.split('/')[0])) + 
        1.5 * df.loc[mascara_partidos, 'T3'].apply(lambda x: int(x.split('/')[0]))
    ) / (
        df.loc[mascara_partidos, 'T2'].apply(lambda x: int(x.split('/')[1])) + 
        df.loc[mascara_partidos, 'T3'].apply(lambda x: int(x.split('/')[1]))
    )) * 100
    
    # eTL - Calcula la eficiencia en tiros libres (Puntos por Intento de Tiro Libre)
    # Evitar división por cero
    mascara_tl = mascara_partidos & (df['TL'].apply(lambda x: int(x.split('/')[1])) > 0)
    df.loc[mascara_tl, 'eTL'] = df.loc[mascara_tl, 'TL'].apply(lambda x: int(x.split('/')[0])) / df.loc[mascara_tl, 'TL'].apply(lambda x: int(x.split('/')[1]))

    # eT2 - Calcula la eficiencia en tiros de 2 puntos (Puntos por Intento de Tiro de 2)
    # Evitar división por cero
    mascara_t2 = mascara_partidos & (df['T2'].apply(lambda x: int(x.split('/')[1])) > 0)
    df.loc[mascara_t2, 'eT2'] = df.loc[mascara_t2, 'T2'].apply(lambda x: int(x.split('/')[0])) * 2 / df.loc[mascara_t2, 'T2'].apply(lambda x: int(x.split('/')[1]))

    # eT3 - Calcula la eficiencia en tiros de 3 puntos (Puntos por Intento de Tiro de 3)
    # Evitar división por cero
    mascara_t3 = mascara_partidos & (df['T3'].apply(lambda x: int(x.split('/')[1])) > 0)
    df.loc[mascara_t3, 'eT3'] = df.loc[mascara_t3, 'T3'].apply(lambda x: int(x.split('/')[0])) * 3 / df.loc[mascara_t3, 'T3'].apply(lambda x: int(x.split('/')[1]))

    return df