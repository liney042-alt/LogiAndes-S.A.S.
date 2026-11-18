# Entrega de Liney — integrante C

**Roles:** R3 y mitad de R4. **Rama:** `integrante-c-liney`.

Liney lidera el diseño de estrategias alternativas, la interpretación estadística y la preparación de gráficos. Las estrategias B/C y el analizador están en `src/estrategia_b.py`, `src/estrategia_c.py` y `herramientas/analizar_resultados.py`.

La corrida formal de entrega y sus archivos asociados son `resultados/medicion_formal_local.csv`, `resultados/medicion_formal_local.entorno.json`, `resultados/resumen.csv`, `resultados/tiempo_vs_n.png` y `resultados/estrategias_n_mayor.png`. Se ejecutaron diez corridas de tiempo por combinación; memoria se midió por separado. El CV supera 10 % y queda documentado como limitación.

Para reproducir el resumen y las figuras:
```powershell
python -m herramientas.analizar_resultados resultados/medicion_formal_local.csv
```
