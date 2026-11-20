# Equipo 1 — Procesamiento de grandes volúmenes de información

## 1. Problema empresarial
**Empresa (caso simulado):** LogiAndes S.A.S., operador logístico con ventas en seis regiones.

El cierre contable diario procesa un archivo de ventas de más de un millón de registros. El proceso tarda cada vez más y en temporada compite por CPU y memoria con otros servicios.

## 2. Situación inicial medible
`src/linea_base.py` carga el CSV completo como lista de diccionarios y recorre la lista una vez por región. La ejecución inicial (`python -m src.linea_base`) produjo estos valores:

| n | Tiempo de una corrida | Fecha | Equipo |
|---:|---:|---|---|
| 200 000 registros | 0.583 s | 2026-11-18 | Equipo 1; Windows 11 x64, Intel Family 6 Model 186, 10 núcleos físicos / 12 lógicos, CPython 3.14.0 |

La salida de totales por región está guardada en [resultados/evidencia_linea_base.txt](resultados/evidencia_linea_base.txt). Para obtener el diagnóstico del equipo en una nueva sesión, ejecute `python -m herramientas.diagnostico_entorno`; el arnés formal también guarda el entorno en un JSON junto al CSV.

### Magnitudes físicas que intervienen
- El tiempo de pared `t` se mide en segundos (s); el tamaño de entrada `n`, en registros.
- El trabajo computacional se aproxima por el número de operaciones/ciclos: `N ≈ f·t`, donde `f` es la frecuencia del procesador en hertz (Hz). Una pasada en vez de seis reduce operaciones y puede reducir tiempo y ciclos.
- La lectura mueve datos de almacenamiento a RAM y CPU. Se puede describir su tasa como datos transferidos por tiempo (MB/s); la caché del sistema puede hacer que una lectura posterior no refleje el disco.
- La memoria Python se registra en MiB. `tracemalloc` permite comparar objetos asignados por Python, pero no es la memoria total residente.
- La energía cumple `E = P̄·t` y se expresa en joules (J), con potencia media `P̄` en watts (W). Solo se concluye ahorro de energía si hay lecturas RAPL válidas; el porcentaje de CPU no es potencia.

## 3. Pregunta de investigación
¿Cómo cambian el tiempo (s) y el pico de memoria Python (MiB) al variar la estrategia de procesamiento (A, B, C) y el tamaño de entrada (100 000, 300 000 y 1 000 000 filas), manteniendo equipo, datos y condiciones constantes?

## 4. Hipótesis
Ver H1–H3 en [docs/hipotesis.md](docs/hipotesis.md). Son predicciones cuantitativas; los resultados medidos y sus límites están en [docs/informe.md](docs/informe.md).

## 5. Estrategias
| Id | Estrategia | Idea principal | Efecto físico esperado |
|---|---|---|---|
| A | Línea base | Lista de diccionarios; recorre el archivo por región. | Más recorridos y objetos retenidos; se espera mayor tiempo (s) y pico de memoria (MiB). |
| B | Flujo `DictReader` | Una pasada, acumulando mientras lee. | Menos operaciones que seis pasadas y menor retención en RAM; se espera bajar tiempo y memoria. |
| C | Flujo `csv.reader` | Una pasada con índices, sin diccionario por fila. | Reduce creación de objetos/búsquedas; se espera menos trabajo por registro y menor tiempo/memoria que B. |

A igual potencia media, una reducción de tiempo podría reducir `E = P̄·t`; la energía no se presume si el sensor no está disponible.

## 6. Cómo reproducir
```powershell
python -m herramientas.diagnostico_entorno
python -m src.linea_base
python -m unittest discover -s pruebas
python -m experimentos.ejecutar_experimento --rapido --salida resultados/corridas/prueba_rapida.csv
python -m experimentos.ejecutar_experimento --salida resultados/corridas/formal.csv
python -m herramientas.analizar_resultados resultados/corridas/formal.csv
```

El arnés valida resultados, aleatoriza orden con semilla 42, calienta funciones y precalienta los CSV antes de medir. Cada corrida debe usar una ruta nueva; si el archivo existe, el programa se detiene para proteger la evidencia previa. Para repetir, cambie el nombre de salida y analice ese CSV. La caché caliente no puede garantizarse en todos los sistemas; anotar esta limitación. Las corridas de memoria usan `tracemalloc` por separado de las de tiempo. RAPL y temperatura son opcionales.

## 7. Integrantes y responsabilidades
La asignación nominal y las ramas por integrante están en [docs/ramas_equipo.md](docs/ramas_equipo.md): Jhostyn (A), Steven (B) y Liney (C). Liney lidera la contribución de optimización, análisis y gráficos; todos deben entender los conceptos físicos y el código.

## 8. Documentación
[Ramas del equipo](docs/ramas_equipo.md) · [Variables](docs/variables.md) · [Protocolo](docs/protocolo.md) · [Entorno](docs/entorno.md) · [Decisiones](docs/decisiones.md) · [Uso de IA](docs/uso_ia.md) · [Informe](docs/informe.md)

## 9. Resultados y conclusiones
Los resultados y sus límites están consolidados en [docs/informe.md](docs/informe.md) y en los CSV versionados dentro de `resultados/`. El CV de la corrida formal superó 10 % en todas las combinaciones; la repetición del 20 de noviembre también superó el umbral; ver `resultados/repeticion_cv_2026-11-20/` y el informe antes de extrapolar las cifras.
