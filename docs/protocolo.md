# Protocolo experimental reproducible

**Responsable:** R1 · **Revisado por:** equipo · **Versión:** 2

## Objetivo
Comparar exactitud, tiempo y memoria de A, B y C al totalizar ventas por región manteniendo datos, máquina y condiciones de ejecución tan constantes como sea posible.

## Preparación
1. Conectar a corriente si es posible; usar perfil equilibrado y cerrar aplicaciones pesadas. Anotar excepciones en `docs/entorno.md`.
2. Ejecutar `python -m herramientas.sensores` y guardar los datos del entorno; también se crea un JSON junto al CSV formal.
3. Generar de forma determinista los tamaños: `python -m src.generar_datos 100000`, `300000` y `1000000`.
4. Registrar la salida de `python -m src.linea_base` como evidencia inicial. Esta corrida de demostración no es parte de las repeticiones estadísticas.

## Parámetros
- Tamaños: 100 000, 300 000 y 1 000 000 filas. Cubren dos órdenes de magnitud y el millón descrito en el caso.
- Repeticiones de tiempo: 10 por combinación estrategia/tamaño para estimar dispersión sin hacer inviable el laboratorio.
- Calentamiento: una ejecución por estrategia antes de medir.
- Orden: aleatorio con semilla 42.
- Memoria: una corrida adicional por estrategia/tamaño con `tracemalloc`; no mezclar su tiempo con las corridas de tiempo, porque el trazado añade sobrecosto.

## Ejecución y caché
1. Pruebas de corrección: `python -m unittest discover -s pruebas`.
2. Humo: `python -m experimentos.ejecutar_experimento --rapido`.
3. Formal: `python -m experimentos.ejecutar_experimento`.
4. Antes de las mediciones, el arnés lee cada archivo completo para favorecer una caché caliente. La caché del SO no se puede fijar ni verificar igual en todos los sistemas; por eso los resultados describen principalmente el escenario caliente, y se reportará como limitación. No comparar una corrida fría de una estrategia con corridas calientes de otra.

## Calidad y registro
Informar media, desviación estándar, CV e IC95 % por combinación. Si CV > 10 %, investigar procesos concurrentes/actualizaciones y repetir la serie documentando el incidente; no borrar datos sin causa. Reportar valores atípicos con regla de Tukey, sin exclusión automática. Marcar energía, temperatura y memoria según medida/ausencia y sus limitaciones.

## Incidentes
| Fecha/hora | Incidente | Corridas afectadas | Decisión |
|---|---|---|---|
