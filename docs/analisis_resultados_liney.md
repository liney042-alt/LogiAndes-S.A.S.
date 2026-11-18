# Análisis de resultados — Liney

## Datos analizados
La corrida formal de entrega está en `resultados/medicion_formal_local.csv`: diez mediciones de tiempo por estrategia y tamaño, además de corridas separadas de memoria. `resultados/resumen.csv` contiene media, desviación estándar, CV e IC95 %. Los archivos `resultados/resultados.csv`, `resultados/repeticion_2.csv` y `resultados/consolidado.csv` conservan series anteriores; no se mezclan con las cifras de esta corrida.

## Hallazgo principal
Para un millón de registros, A promedió 3.4624 s, B 2.4070 s y C 1.0400 s. C redujo el tiempo estimado 70.0 % respecto de A y 56.8 % respecto de B. En mediciones separadas, `tracemalloc` registró 529.310 MiB para A, 0.182 MiB para B y 0.176 MiB para C.

## Figuras
`resultados/tiempo_vs_n.png` muestra el tiempo frente a n con barras de error. `resultados/estrategias_n_mayor.png` compara las estrategias para n = 1 000 000.

## Criterio y límites
Las estimaciones puntuales cumplen H1–H3 a n = 1 000 000. El CV de tiempo está entre 11.5 % y 23.7 %, por encima del umbral de 10 %; se reporta como limitación. No hubo energía RAPL válida. La medición describe principalmente caché caliente y no es memoria total del proceso.
