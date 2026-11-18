
#Línea base — Equipo 1: Procesamiento de grandes volúmenes de información.

#Situación inicial (así funciona HOY el sistema de la empresa):
# 1. Lee TODO el archivo de ventas en una lista de diccionarios.
#2. Para CADA región, recorre la lista completa filtrando sus ventas.
#Resultado: total vendido (cantidad · precio) por región.#


import csv
from pathlib import Path

from src.generar_datos import generar_ventas

DATOS = Path(__file__).resolve().parents[1] / "datos"


def preparar(n: int) -> Path:
    ruta = DATOS / f"ventas_{n}.csv"
    if not ruta.exists():
        generar_ventas(ruta, n)
    return ruta


def ejecutar(ruta: Path) -> dict[str, float]:
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))              # todo el archivo en memoria
    regiones = sorted({fila["region"] for fila in filas})
    totales = {}
    for region in regiones:                           # una pasada completa POR región
        total = 0.0
        for fila in filas:
            if fila["region"] == region:
                total += int(fila["cantidad"]) * float(fila["precio_unitario"])
        totales[region] = round(total, 2)
    return totales


if __name__ == "__main__":
    import time
    datos = preparar(200_000)
    t0 = time.perf_counter()
    print(ejecutar(datos))
    print(f"Tiempo: {time.perf_counter() - t0:.3f} s  (una corrida, solo verificación)")
