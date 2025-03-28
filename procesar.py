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
