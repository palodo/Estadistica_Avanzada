def convertir_a_minutos_decimales(tiempo):
    """Convierte un string MM:SS a minutos en decimal."""
    if isinstance(tiempo, str) and ":" in tiempo:
        minutos, segundos = map(int, tiempo.split(":"))
        return minutos + segundos / 60


def calcular_usage_rate(df, total_team_stats):
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

    return df