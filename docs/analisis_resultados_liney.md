# Análisis de resultados — Liney

## Datos de entrada
`resultados/consolidado.csv` reúne dos series formales, cada una con diez repeticiones de tiempo por estrategia/tamaño. `resultados/resumen.csv` contiene media, desviación estándar, CV e IC95 %. Las corridas de memoria son separadas y hay dos por combinación.

## Hallazgo principal
Para un millón de registros, A promedió 3.9367 s, B 3.0288 s y C 1.2860 s. C redujo el tiempo estimado 67.3 % respecto de A y 57.5 % respecto de B. La lectura en flujo evitó retener el millón de diccionarios: `tracemalloc` registró 529.310 MiB para A y menos de 0.2 MiB para B/C, con solo dos lecturas de memoria por método.

## Criterio y límites
Los promedios cumplen las predicciones cuantitativas H1–H3 a n = 1 000 000. Sin embargo, el CV consolidado supera 10 % en todas las combinaciones. Las dos series también varían entre sí; tratar los IC95 % como descriptivos y no como garantía de repetibilidad. No hay energía RAPL válida y no se generaron gráficos porque falta matplotlib. La propuesta de C es provisional y se limita al escenario principalmente de caché caliente.
