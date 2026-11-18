# Entrega de Liney — integrante C

**Roles:** R3 y mitad de R4. **Rama:** `integrante-c-liney`.

Liney lidera el diseño de estrategias alternativas, la interpretación estadística y la preparación de gráficos. Las estrategias B/C y el analizador están en `src/estrategia_b.py`, `src/estrategia_c.py` y `herramientas/analizar_resultados.py`. Esta rama incorpora el análisis de dos series y las cifras observadas al informe.

Reproducir el resumen consolidado:
```powershell
python -m herramientas.analizar_resultados resultados/consolidado.csv
```
El entorno no tiene matplotlib; por ello el analizador produjo el CSV resumen, pero no produjo los gráficos PNG previstos. Mantener esa limitación explícita hasta que se instale la dependencia o se acuerde otro medio de visualización.
