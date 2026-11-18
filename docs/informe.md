# Informe científico breve — Equipo 1

**Título:** Comparación del procesamiento de ventas por región  · **Integrantes:**  · **Fecha:**  · **Repositorio:**

## Resumen (≤ 150 palabras)
Pendiente de mediciones. Informar problema, método, principal resultado con cifra y unidad, intervalo de confianza y conclusión. No presentar predicciones como resultados.

## 1. Introducción
El caso simulado representa un archivo de ventas de más de un millón de filas. La pregunta es cómo cambian el tiempo (s) y el pico de memoria Python (MiB) al procesar los mismos registros con tres estrategias. El trabajo computacional se relaciona con el número de operaciones y los ciclos aproximados por N = f·t. La lectura mueve datos desde almacenamiento a RAM y CPU, con una tasa efectiva en MB/s. La energía satisface E = P̄·t; solo se afirmará ahorro de energía si RAPL está disponible y se registraron mediciones adecuadas.

## 2. Hipótesis
Usar literalmente H1–H3 de `docs/hipotesis.md`; no cambiarlas después de observar los resultados. Marcar cada una como confirmada o refutada según los umbrales predefinidos.

## 3. Método
A: lista de diccionarios y recorrido por región. B: `DictReader` en flujo y una pasada. C: `csv.reader` en flujo y acceso por índice. El generador usa semilla 1; los tres métodos deben devolver totales idénticos. El arnés utiliza orden pseudoaleatorio con semilla 42, calentamiento y caché de archivos precalentada. Revisar `docs/variables.md`, `docs/protocolo.md` y `docs/entorno.md` para controles, instrumentos y limitaciones.

## 4. Resultados
Ejecutar `python -m herramientas.analizar_resultados resultados/resultados.csv`. Insertar `resultados/resumen.csv`, `resultados/tiempo_vs_n.png` y `resultados/estrategias_n_mayor.png`. Reportar media, desviación estándar, CV e IC95 % por estrategia/tamaño. Distinguir memoria medida en corrida separada y energía/temperatura solo cuando disponibles. Añadir cifras observadas aquí después del experimento formal.

## 5. Discusión
Indicar si cada hipótesis se confirma o refuta según su criterio. Explicar efectos de pasadas, conversiones, objetos y transferencia de datos. Declarar que el escenario es principalmente de caché caliente y que `tracemalloc` no mide toda la memoria del proceso.

## 6. Propuesta para la empresa
Pendiente de los resultados: recomendar una estrategia con mejora cuantificada, condiciones de validez y riesgos.

## 7. Conclusiones
Pendientes de mediciones; no inventar cifras.

## 8. Referencias
Documentación de Python para `csv`, `time`, `tracemalloc` y `statistics`; registrar enlaces/fecha de consulta al preparar la entrega.

## Anexo: uso de IA
Resumir `docs/uso_ia.md` y revisar que el equipo pueda explicar y verificar el código.
