# Variables experimentales

| Tipo | Variable | Símbolo | Unidad | Valores | Obtención / control | Justificación |
|---|---|---|---|---|---|---|
| Independiente | Estrategia | S | — | A, B, C | Mismo arnés; orden aleatorio | Modifica pasadas y objetos temporales. |
| Independiente | Filas de entrada | n | registros | 100 000; 300 000; 1 000 000 | Generador con semilla 1; mismos archivos por estrategia | Permite observar cómo escala el costo. |
| Dependiente | Tiempo de pared | t | s | Por corrida | `time.perf_counter()` | Mide duración percibida de la tarea. |
| Dependiente | Pico de memoria Python | M | MiB | Por corrida separada | `tracemalloc`; no representa RSS total | Evalúa el costo de materializar filas. |
| Dependiente | Uso CPU del proceso | U | % de un núcleo | Por corrida | Tiempo CPU / tiempo de pared × 100 | Aproxima ocupación de CPU, no potencia. Puede superar 100 % si hay paralelismo. |
| Dependiente opcional | Energía del paquete | E | J | Si RAPL disponible | Diferencia del contador RAPL | Sensor del paquete, no del equipo completo; no inferir si no está disponible. |
| Dependiente opcional | Temperatura | θ | °C | Si el sensor existe | `sensores.py` | Indicador térmico con retraso; anotar disponibilidad. |
| Controlada | Equipo, Python y alimentación | — | — | Anotar en entorno | `describir_entorno()` y registro manual | Reducir cambios de plataforma y frecuencia. |
| Controlada | Datos y corrección | — | — | Mismos CSV | Semilla fija y comparación de totales | Evitar diferencias de contenido y resultados incorrectos. |
| Controlada | Orden y calentamiento | — | — | Semilla de orden 42; una corrida de calentamiento | Arnés de experimento | Mitigar deriva temporal y costo de arranque. |

## Mapa físico y computacional
`Estrategia → pasadas/objetos y conversiones → operaciones → ciclos N ≈ f·t → tiempo`.
`CSV → almacenamiento → RAM → CPU`: el volumen leído y la tasa efectiva de transferencia condicionan el tiempo, junto con el parseo y las conversiones.
`E = P̄·t`: solo si se mide energía; con potencia media similar, menos tiempo/ciclos puede reducir energía. El porcentaje de CPU no es potencia.

## Factores no controlados y mitigación
| Factor | Efecto | Mitigación |
|---|---|---|
| Caché del sistema operativo | La primera lectura puede venir del disco y las siguientes de RAM | El arnés precalienta cada archivo antes de medir; el resultado representa principalmente un escenario de caché caliente. Anotar que el caché no se puede fijar de forma portable y no generalizar a lecturas en frío. |
| Frecuencia dinámica / temperatura | Cambia ciclos por segundo y rendimiento | Corriente, perfil equilibrado, calentamiento y orden aleatorio; registrar frecuencia/temperatura disponibles. |
| Procesos del sistema | Compiten por CPU y memoria | Cerrar aplicaciones pesadas y anotar incidentes; repetir si hay interrupciones. |
