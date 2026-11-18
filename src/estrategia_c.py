"""Estrategia C: flujo con csv.reader y acceso por índice, sin dict por fila."""
import csv
from pathlib import Path


def ejecutar(ruta: Path) -> dict[str, float]:
    acumulados: dict[str, float] = {}
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.reader(f)
        encabezado = next(lector)
        i_region = encabezado.index("region")
        i_cantidad = encabezado.index("cantidad")
        i_precio = encabezado.index("precio_unitario")
        for fila in lector:
            region = fila[i_region]
            acumulados[region] = acumulados.get(region, 0.0) + int(fila[i_cantidad]) * float(fila[i_precio])
    return {region: round(total, 2) for region, total in sorted(acumulados.items())}
