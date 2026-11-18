# Equipo 1 — Procesamiento de grandes volúmenes de información

> Proyecto: *Laboratorio colaborativo de rendimiento y eficiencia computacional desde la física aplicada*
> Física Aplicada al Desarrollo de Software · SENA · ADSO · 7.º trimestre

## 1. Problema empresarial
**Empresa (caso simulado):** LogiAndes S.A.S., operador logístico con ventas en seis regiones.

El cierre contable diario procesa un archivo de ventas de más de un millón de registros. El proceso tarda cada vez más y en temporada compite por CPU y memoria con otros servicios.

## 2. Situación inicial medible
`src/linea_base.py` carga el CSV completo como lista de diccionarios y lo recorre una vez por región. Ejecute `python -m src.linea_base` y conserve la salida en `resultados/evidencia_linea_base.txt` como evidencia inicial.

## 3. Pregunta de investigación
¿Cómo cambian el tiempo (s) y el pico de memoria Python (MiB) al variar la estrategia de procesamiento (A, B, C) y el tamaño de entrada (100 000, 300 000 y 1 000 000 filas), manteniendo equipo, datos y condiciones constantes?

## 4. Hipótesis
Ver H1–H3 en [docs/hipotesis.md](docs/hipotesis.md). Son predicciones cuantitativas pendientes de prueba.

## 5. Estrategias
| Id | Estrategia | Idea principal |
|---|---|---|
| A | Línea base | Lista de diccionarios y recorrido por región. |
| B | Flujo `DictReader` | Una pasada, sin retener todas las filas. |
| C | Flujo `csv.reader` | Una pasada, columnas por índice, sin diccionario por fila. |

## 6. Cómo reproducir
```powershell
python -m src.linea_base
python -m unittest discover -s pruebas
python -m experimentos.ejecutar_experimento --rapido
python -m experimentos.ejecutar_experimento
python -m herramientas.analizar_resultados resultados/resultados.csv
```

El arnés valida resultados, aleatoriza orden con semilla 42, calienta funciones y precalienta los CSV antes de medir. La caché caliente no puede garantizarse en todos los sistemas; anotar esta limitación. Las corridas de memoria usan `tracemalloc` por separado de las de tiempo. RAPL y temperatura son opcionales.

## 7. Integrantes y responsabilidades
Registrar nombres y la distribución del enunciado para equipo de tres: A coordina protocolo/entorno y parte de R4; B desarrolla la base y pruebas, revisa las alternativas; C desarrolla alternativas y parte de R4 para análisis/gráficos. Todos deben entender los conceptos físicos y el código.

## 8. Documentación
[Variables](docs/variables.md) · [Protocolo](docs/protocolo.md) · [Entorno](docs/entorno.md) · [Decisiones](docs/decisiones.md) · [Uso de IA](docs/uso_ia.md) · [Informe](docs/informe.md)

## 9. Resultados y conclusiones
Pendientes de la ejecución formal. No completar con cifras estimadas; incluir resultados observados, unidades y sus intervalos de confianza.
