"""Genera un CSV de ventas SIMULADAS reproducible (semilla fija). Uso: python -m src.generar_datos 1000000"""
import csv
import random
import sys
from pathlib import Path

REGIONES = ["Andina", "Caribe", "Pacífica", "Orinoquía", "Amazonía", "Insular"]


def generar_ventas(ruta: Path, n: int, semilla: int = 1) -> None:
    rng = random.Random(semilla)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id_venta", "fecha", "region", "producto", "cantidad", "precio_unitario"])
        for i in range(n):
            w.writerow([i, f"2026-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}", rng.choice(REGIONES),
                        f"P{rng.randint(1, 5000):05d}", rng.randint(1, 20), f"{rng.uniform(1000, 250000):.2f}"])


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    destino = Path(__file__).resolve().parents[1] / "datos" / f"ventas_{n}.csv"
    generar_ventas(destino, n)
    print(f"{destino} ({destino.stat().st_size / 1e6:.1f} MB)")
