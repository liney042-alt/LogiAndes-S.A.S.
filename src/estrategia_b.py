#Estrategia B: una sola pasada por el CSV con lectura en flujo.#
import csv
from pathlib import Path


def ejecutar(ruta: Path) -> dict[str, float]:
    acumulados: dict[str, float] = {}
    with open(ruta, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            region = fila["region"]
            acumulados[region] = acumulados.get(region, 0.0) + int(fila["cantidad"]) * float(fila["precio_unitario"])
    return {region: round(total, 2) for region, total in sorted(acumulados.items())}
