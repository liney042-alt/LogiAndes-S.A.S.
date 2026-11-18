# Hipótesis verificables

Las predicciones siguientes se fijan antes de analizar los resultados. Se evaluarán en n = 1 000 000; una predicción que no alcance su umbral se considera refutada para este equipo y protocolo.

| Id | Hipótesis completa | VI | VD | Predicción | Mecanismo | Refutación |
|---|---|---|---|---|---|---|
| H1 | Si se cambia A por B, el pico de memoria Python disminuirá al menos 70 % a n = 1 000 000, porque B procesa el flujo sin conservar la lista completa de diccionarios. | Estrategia | Pico MiB | Reducción ≥70 % | Menos objetos vivos y menor volumen retenido en RAM | Reducción <70 % o memoria B ≥ A en medición separada. |
| H2 | Si se cambia A por B, el tiempo medio disminuirá al menos 20 % a n = 1 000 000, porque B reemplaza una pasada por región por una sola pasada y acumula en línea. | Estrategia | Tiempo s | Reducción ≥20 % | Menos comparaciones/recorridos; persisten parseo y conversiones | Reducción <20 % o B tarda igual/más que A. |
| H3 | Si se cambia B por C, el tiempo medio disminuirá al menos 5 % a n = 1 000 000, porque `csv.reader` evita crear un diccionario por fila. | Estrategia | Tiempo s | Reducción ≥5 % | Menos construcción y búsqueda de claves por registro | Reducción <5 % o C tarda igual/más que B. |

## Criterios
Comparar medias de las corridas de tiempo (sin `tracemalloc`) por estrategia y tamaño, con mismo CSV. Informar variabilidad e IC95 %. Las pruebas de corrección deben confirmar totales idénticos antes del experimento. No afirmar ahorro de energía si RAPL no entrega mediciones utilizables; el uso de CPU tampoco equivale a potencia.
