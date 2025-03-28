
# Proyecto Estadísticas de Baloncesto

Este proyecto tiene como objetivo obtener, analizar y calcular estadísticas avanzadas de baloncesto de los jugadores de la liga EBA. Las estadísticas se obtienen a través de web scraping de la página de la Federación Española de Baloncesto (FEB). 

## Requisitos

Para ejecutar este proyecto, necesitarás tener instaladas las siguientes librerías de Python:

- `pandas`
- `beautifulsoup4`
- `requests`

Puedes instalar estas dependencias con pip:

```bash
pip install pandas beautifulsoup4 requests
```

## Descripción de las Estadísticas Avanzadas

### USG% (Usage Percentage)

El **USG%** es una medida que indica el porcentaje de jugadas ofensivas en las que un jugador está involucrado mientras está en la cancha. Se calcula con la siguiente fórmula:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?\color{white}USG\%=100\times\frac{(FGA+0.44\times{FTA}+TOV)\times(\text{Team\;Minutes}/5)}{(\text{Player\;Minutes})\times(\text{Team\;FGA}+0.44\times\text{Team\;FTA}+\text{Team\;TOV})}">
  <source media="(prefers-color-scheme: light)" srcset="https://latex.codecogs.com/svg.latex?USG\%=100\times\frac{(FGA+0.44\times{FTA}+TOV)\times(\text{Team\;Minutes}/5)}{(\text{Player\;Minutes})\times(\text{Team\;FGA}+0.44\times\text{Team\;FTA}+\text{Team\;TOV})}">
  <img alt="USG% Formula" src="https://latex.codecogs.com/svg.latex?USG\%=100\times\frac{(FGA+0.44\times{FTA}+TOV)\times(\text{Team\;Minutes}/5)}{(\text{Player\;Minutes})\times(\text{Team\;FGA}+0.44\times\text{Team\;FTA}+\text{Team\;TOV})}">
</picture>

**Variables:**

- `FGA`: Intentos de tiros de campo (Field Goal Attempts)
- `FTA`: Intentos de tiros libres (Free Throw Attempts)
- `TOV`: Pérdidas de balón (Turnovers)
- `Team Minutes`: Minutos totales jugados por el equipo
- `Player Minutes`: Minutos jugados por el jugador

El **USG%** se utiliza para evaluar cuán involucrado está un jugador en la ofensiva de su equipo. Un porcentaje alto indica que el jugador es muy importante en las jugadas ofensivas.

### eFG% (Effective Field Goal Percentage)

El **eFG%** es una métrica que ajusta el porcentaje de tiros de campo (Field Goal Percentage) para tener en cuenta los tiros de tres puntos, que valen más que los tiros de dos puntos. Se calcula con la siguiente fórmula:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?\color{white}eFG\%=\frac{FGM+0.5\times{3PM}}{FGA}">
  <source media="(prefers-color-scheme: light)" srcset="https://latex.codecogs.com/svg.latex?eFG\%=\frac{FGM+0.5\times{3PM}}{FGA}">
  <img alt="eFG% Formula" src="https://latex.codecogs.com/svg.latex?eFG\%=\frac{FGM+0.5\times{3PM}}{FGA}">
</picture>

**Variables:**

- `FGM`: Tiros de campo convertidos (Field Goals Made)
- `3PM`: Tiros de tres puntos convertidos (Three-Point Field Goals Made)
- `FGA`: Intentos de tiros de campo (Field Goal Attempts)

Este porcentaje ajustado refleja mejor la efectividad de un jugador, considerando los tiros de tres puntos como más valiosos que los de dos puntos.

### eTL - Eficiencia en Tiros Libres

La **eficiencia en tiros libres (eTL)** calcula los puntos en tiros libres por intento. La fórmula es:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?\color{white}eTL=\frac{\text{Tiros\;Libres\;Convertidos}}{\text{Total\;Tiros\;Libres\;Intentados}}">
  <source media="(prefers-color-scheme: light)" srcset="https://latex.codecogs.com/svg.latex?eTL=\frac{\text{Tiros\;Libres\;Convertidos}}{\text{Total\;Tiros\;Libres\;Intentados}}">
  <img alt="eTL Formula" src="https://latex.codecogs.com/svg.latex?eTL=\frac{\text{Tiros\;Libres\;Convertidos}}{\text{Total\;Tiros\;Libres\;Intentados}}">
</picture>



### eT2 - Eficiencia en Tiros de 2 Puntos

La **eficiencia en tiros de 2 puntos (eT2)** calcula los puntos por intento de tiro de 2 puntos. La fórmula es:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?\color{white}eT2=\frac{\text{Tiros\;de\;2\;Convertidos}\times{2}}{\text{Total\;Tiros\;de\;2\;Intentados}}">
  <source media="(prefers-color-scheme: light)" srcset="https://latex.codecogs.com/svg.latex?eT2=\frac{\text{Tiros\;de\;2\;Convertidos}\times{2}}{\text{Total\;Tiros\;de\;2\;Intentados}}">
  <img alt="eT2 Formula" src="https://latex.codecogs.com/svg.latex?eT2=\frac{\text{Tiros\;de\;2\;Convertidos}\times{2}}{\text{Total\;Tiros\;de\;2\;Intentados}}">
</picture>



### eT3 - Eficiencia en Tiros de 3 Puntos

La **eficiencia en tiros de 3 puntos (eT3)** calcula los puntos por intento de tiro de 3 puntos. La fórmula es:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?\color{white}eT3=\frac{\text{Tiros\;de\;3\;Convertidos}\times{3}}{\text{Total\;Tiros\;de\;3\;Intentados}}">
  <source media="(prefers-color-scheme: light)" srcset="https://latex.codecogs.com/svg.latex?eT3=\frac{\text{Tiros\;de\;3\;Convertidos}\times{3}}{\text{Total\;Tiros\;de\;3\;Intentados}}">
  <img alt="eT3 Formula" src="https://latex.codecogs.com/svg.latex?eT3=\frac{\text{Tiros\;de\;3\;Convertidos}\times{3}}{\text{Total\;Tiros\;de\;3\;Intentados}}">
</picture>



## Funcionalidades

1. **Obtención de Estadísticas:**
   El proyecto obtiene las estadísticas de los jugadores a través de web scraping de la página de la FEB, utilizando `BeautifulSoup` y `requests`.

2. **Conversión de Minutos:**
   Los minutos jugados por cada jugador son convertidos de formato `MM:SS` a formato decimal para facilitar los cálculos de las estadísticas avanzadas.

3. **Cálculo de Estadísticas Avanzadas:**
   Se calculan estadísticas como el **USG%** y el **eFG%** para cada jugador, utilizando los datos obtenidos de la página.

## Ejecución

Para ejecutar el proyecto, simplemente ejecuta el archivo `main.py` en tu terminal:

```bash
python main.py
```

El script descargará las estadísticas de los jugadores y calculará las métricas avanzadas de manera automática.

## Contribuciones

Si deseas contribuir al proyecto, siéntete libre de realizar un fork y crear un Pull Request con tus mejoras o correcciones.

