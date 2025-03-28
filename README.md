Estadísticas Avanzadas de Baloncesto
Este proyecto tiene como objetivo calcular estadísticas avanzadas para jugadores de baloncesto utilizando datos extraídos de una página web.

Estadísticas Implementadas
1. USG% (Uso de Jugador)
USG% mide el porcentaje de posesiones de un equipo que un jugador utiliza mientras está en el campo. Indica cuántas veces un jugador está involucrado en la creación de tiros, incluyendo intentos de tiro, tiros libres y pérdidas de balón.

Fórmula:
𝑈
𝑆
𝐺
%
=
100
×
(
𝐹
𝐺
𝐴
+
0.44
×
𝐹
𝑇
𝐴
+
𝑇
𝑂
𝑉
)
×
𝑇
𝑒
𝑎
𝑚
 
𝑀
𝑖
𝑛
𝑢
𝑡
𝑒
𝑠
5
𝑃
𝑙
𝑎
𝑦
𝑒
𝑟
 
𝑀
𝑖
𝑛
𝑢
𝑡
𝑒
𝑠
×
(
𝑇
𝑒
𝑎
𝑚
 
𝐹
𝐺
𝐴
+
0.44
×
𝑇
𝑒
𝑎
𝑚
 
𝐹
𝑇
𝐴
+
𝑇
𝑒
𝑎
𝑚
 
𝑇
𝑂
𝑉
)
USG%=100× 
Player Minutes×(Team FGA+0.44×Team FTA+Team TOV)
(FGA+0.44×FTA+TOV)× 
5
Team Minutes
​
 
​
 
Donde:

FGA: Intentos de tiro de campo (Field Goals Attempted).

FTA: Intentos de tiro libre (Free Throws Attempted).

TOV: Pérdidas de balón (Turnovers).

Team Minutes: Minutos totales jugados por el equipo.

Player Minutes: Minutos jugados por el jugador.

Team FGA: Intentos de tiro de campo del equipo.

Team FTA: Intentos de tiro libre del equipo.

Team TOV: Pérdidas de balón del equipo.

Nota: Esta fórmula tiene en cuenta que las pérdidas de balón también deben considerarse como parte del uso del jugador.

2. eFG% (Porcentaje de Tiro Efectivo)
eFG% ajusta el porcentaje de tiros de campo para tener en cuenta que los triples valen más que los dobles. Es una medida más precisa de la eficiencia de un jugador al realizar tiros.

Fórmula:
𝑒
𝐹
𝐺
%
=
𝑇
2
 encestados
+
1.5
×
𝑇
3
 encestados
𝐹
𝐺
𝐴
eFG%= 
FGA
T2 encestados+1.5×T3 encestados
​
 
Donde:

T2 encestados: Canastas de 2 puntos encestadas.

T3 encestados: Canastas de 3 puntos encestadas.

FGA: Intentos de tiro de campo (Field Goals Attempted).

Nota: Los triples se ponderan como 1.5 veces más valiosos que los dobles para reflejar mejor la eficiencia en los tiros.