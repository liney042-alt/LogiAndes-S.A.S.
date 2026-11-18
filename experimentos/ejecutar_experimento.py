"""Automatiza la comparación de estrategias y registra las mediciones."""
import argparse
import random
from pathlib import Path

from herramientas.labmedicion import Experimento, calentar
from src import estrategia_b, estrategia_c, linea_base

ESTRATEGIAS = {
    "A_linea_base": linea_base,
    "B_flujo_dictreader": estrategia_b,
    "C_flujo_csv_reader": estrategia_c,
}
TAMANOS = [100_000, 300_000, 1_000_000]
REPETICIONES = 10


def precalentar_archivos(rutas: dict[int, Path]) -> None:
    """Lee cada entrada antes del cronómetro para aproximar un escenario de caché caliente."""
    for ruta in rutas.values():
        with ruta.open("rb") as archivo:
            while archivo.read(8 * 1024 * 1024):
                pass


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--rapido", action="store_true")
    p.add_argument("--salida", default="resultados/resultados.csv")
    a = p.parse_args()
    tamanos = TAMANOS[:1] if a.rapido else TAMANOS
    reps = 2 if a.rapido else REPETICIONES

    datos = {n: linea_base.preparar(n) for n in tamanos}
    for n, ruta in datos.items():
        esperado = linea_base.ejecutar(ruta)
        for nombre, mod in ESTRATEGIAS.items():
            assert mod.ejecutar(ruta) == esperado, f"{nombre} da un resultado distinto para n={n}"

    precalentar_archivos(datos)
    plan = [(e, n, r) for e in ESTRATEGIAS for n in tamanos for r in range(1, reps + 1)]
    random.Random(42).shuffle(plan)
    for mod in ESTRATEGIAS.values():
        calentar(mod.ejecutar, datos[tamanos[0]], veces=1)

    salida = Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.unlink(missing_ok=True)
    with Experimento(salida, equipo="Equipo 1") as exp:
        for i, (e, n, r) in enumerate(plan, 1):
            exp.medir(ESTRATEGIAS[e].ejecutar, datos[n], estrategia=e, n=n, repeticion=r)
            if r == 1:
                exp.medir(ESTRATEGIAS[e].ejecutar, datos[n], estrategia=e, n=n, repeticion=0,
                          medir_memoria=True, observacion="corrida de memoria")
            print(f"\r{i}/{len(plan)}", end="", flush=True)
    print(f"\nListo: {salida}")


if __name__ == "__main__":
    main()
