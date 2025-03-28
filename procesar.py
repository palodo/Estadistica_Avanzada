def convertir_a_minutos_decimales(tiempo):
    """Convierte un string MM:SS a minutos en decimal."""
    if isinstance(tiempo, str) and ":" in tiempo:
        minutos, segundos = map(int, tiempo.split(":"))
        return minutos + segundos / 60


def calcular_avanzadas(df, total_team_stats):
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




def calcular_estadisticas_avanzadas_equipo(df, total_team_stats):
    """
    Calcula las estadísticas avanzadas del equipo basadas en los totales del equipo.
    :param df: DataFrame con estadísticas individuales
    :param total_team_stats: Diccionario con estadísticas totales del equipo
    :return: Diccionario con las estadísticas avanzadas del equipo
    """
    
    # Totales del equipo (última fila)
    totales_equipo = df.iloc[-1]
    
    # **True Shooting Percentage (TS%)**
    # TS% = PTS / (2 * (FGA + 0.44 * FTA))
    ts_pct = totales_equipo['PTS'] / (2 * (totales_equipo['FGA'] + 0.44 * totales_equipo['FTA'])) * 100
    
    # **Eficiencia de equipo**
    # Eficiencia = PTS / (FGA + FTA + TOV)
    eficiencia_equipo = totales_equipo['PTS'] / (totales_equipo['FGA'] + totales_equipo['FTA'] + totales_equipo['TOV'])
    
    # **Offensive Rating (ORtg)**
    # ORtg = PTS * 100 / (FGA + 0.44 * FTA + TOV)
    ortg = totales_equipo['PTS'] * 100 / (totales_equipo['FGA'] + 0.44 * totales_equipo['FTA'] + totales_equipo['TOV'])
    
    # **Defensive Rating (DRtg)**
    # DRtg = (PTS en contra * 100) / (FGA + 0.44 * FTA + TOV)  (Suponiendo que tienes datos de puntos en contra)
    # Si no tienes datos de puntos en contra, este puede ser un cálculo más complicado. Aquí se simplifica.
    drtg = (totales_equipo['PTS'] * 100) / (totales_equipo['FGA'] + 0.44 * totales_equipo['FTA'] + totales_equipo['TOV'])
    
    # **Pace (Ritmo de juego)**
    # Pace = (FGA + (0.44 * FTA) + TOV) / minutos jugados (por equipo)
    pace = (totales_equipo['FGA'] + (0.44 * totales_equipo['FTA']) + totales_equipo['TOV']) / totales_equipo['Minutos']
    
    # Crear un diccionario con las estadísticas avanzadas del equipo
    estadisticas_avanzadas_equipo = {
        'TS%': ts_pct,
        'Eficiencia': eficiencia_equipo,
        'ORtg': ortg,
        'DRtg': drtg,
        'Pace': pace
    }
    
    return estadisticas_avanzadas_equipo
