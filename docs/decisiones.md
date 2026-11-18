# Registro de decisiones técnicas

## D-001 — Alternativas de lectura en flujo
- **Fecha:** 2026-11-18 · **Autor(es):** Equipo 1 · **Issue/PR:** —
- **Contexto:** comparar la línea base de lista de diccionarios y pasadas por región con al menos dos métodos comparables.
- **Opciones consideradas:** flujo con `csv.DictReader`; flujo con `csv.reader` e índices; lectura en bloques.
- **Decisión:** implementar B con `DictReader` en una pasada y C con `csv.reader` en una pasada y acceso a columnas por índice.
- **Justificación física/computacional:** ambas evitan retener todas las filas y reducen seis recorridos a uno; C también evita un diccionario por fila. Se miden tiempo y memoria para comprobar si el trabajo y espacio retenido disminuyen.
- **Consecuencias / riesgos:** ambas hacen conversiones y acumulan por región; la caché del sistema, frecuencia y procesos concurrentes afectan medidas. Las tres deben producir el mismo total por región.
