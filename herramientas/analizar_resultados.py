"""Resume el CSV del experimento y genera gráficos si matplotlib está instalado."""
import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

T_CRIT_95 = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571,
             7: 2.447, 8: 2.365, 9: 2.306, 10: 2.262, 11: 2.228,
             12: 2.201, 13: 2.179, 14: 2.160, 15: 2.145, 16: 2.131,
             17: 2.120, 18: 2.110, 19: 2.101, 20: 2.093, 21: 2.086,
             22: 2.080, 23: 2.074, 24: 2.069, 25: 2.064, 26: 2.060,
             27: 2.056, 28: 2.052, 29: 2.048, 30: 2.045}


def resumen(valores: list[float]) -> tuple[float, float, float, float, float]:
    media = statistics.mean(valores)
    sd = statistics.stdev(valores) if len(valores) > 1 else 0.0
    cv = sd / media * 100 if media else 0.0
    tcrit = T_CRIT_95.get(len(valores) - 1, 1.96)
    margen = tcrit * sd / math.sqrt(len(valores)) if len(valores) > 1 else 0.0
    return media, sd, cv, media - margen, media + margen


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", nargs="?", default="resultados/resultados.csv")
    args = parser.parse_args()
    ruta = Path(args.csv)
    grupos: dict[tuple[str, int], list[float]] = defaultdict(list)
    memorias: dict[tuple[str, int], list[float]] = defaultdict(list)
    with ruta.open(newline="", encoding="utf-8-sig") as f:
        for fila in csv.DictReader(f):
            clave = (fila["estrategia"], int(fila["n"]))
            if fila.get("medicion_memoria") == "si":
                if fila.get("pico_mem_mib"):
                    memorias[clave].append(float(fila["pico_mem_mib"]))
            elif int(fila["repeticion"]) > 0 and fila.get("tiempo_s"):
                grupos[clave].append(float(fila["tiempo_s"]))

    salida = ruta.parent / "resumen.csv"
    with salida.open("w", newline="", encoding="utf-8") as f:
        campos = ["estrategia", "n", "repeticiones_tiempo", "media_s", "desviacion_s",
                  "cv_pct", "ic95_inf_s", "ic95_sup_s", "pico_memoria_mib", "mediciones_memoria"]
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for clave in sorted(set(grupos) | set(memorias), key=lambda x: (x[1], x[0])):
            xs = grupos.get(clave, [])
            ys = memorias.get(clave, [])
            media, sd, cv, inf, sup = resumen(xs) if xs else (None,) * 5
            escritor.writerow({"estrategia": clave[0], "n": clave[1],
                "repeticiones_tiempo": len(xs), "media_s": media, "desviacion_s": sd,
                "cv_pct": cv, "ic95_inf_s": inf, "ic95_sup_s": sup,
                "pico_memoria_mib": max(ys) if ys else "", "mediciones_memoria": len(ys)})
            if xs:
                print(f"{clave[0]} n={clave[1]}: media={media:.4f}s, SD={sd:.4f}s, CV={cv:.1f}%, IC95% [{inf:.4f}, {sup:.4f}]")
    print(f"Resumen: {salida}")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib no instalado; se omitieron los gráficos.")
        return
    nombres = sorted({e for e, _ in grupos})
    tamanos = sorted({n for _, n in grupos})
    if tamanos:
        plt.figure()
        for nombre in nombres:
            medias = [statistics.mean(grupos[(nombre, n)]) if grupos.get((nombre, n)) else float("nan") for n in tamanos]
            errores = [resumen(grupos[(nombre, n)])[3:] if grupos.get((nombre, n)) else (0, 0) for n in tamanos]
            yerr = [[m - lo for m, (lo, hi) in zip(medias, errores)], [hi - m for m, (lo, hi) in zip(medias, errores)]]
            plt.errorbar(tamanos, medias, yerr=yerr, marker="o", capsize=3, label=nombre)
        plt.xscale("log"); plt.yscale("log")
        plt.xlabel("Registros n"); plt.ylabel("Tiempo (s)"); plt.legend(); plt.tight_layout()
        plt.savefig(ruta.parent / "tiempo_vs_n.png", dpi=160); plt.close()
        mayor = tamanos[-1]
        etiquetas = [e for e in nombres if grupos.get((e, mayor))]
        if etiquetas:
            medias = [statistics.mean(grupos[(e, mayor)]) for e in etiquetas]
            errores = [resumen(grupos[(e, mayor)])[3:] for e in etiquetas]
            plt.figure(); plt.bar(etiquetas, medias)
            plt.ylabel("Tiempo medio (s)"); plt.xticks(rotation=15, ha="right"); plt.tight_layout()
            plt.savefig(ruta.parent / "estrategias_n_mayor.png", dpi=160); plt.close()
        print(f"Gráficos guardados en {ruta.parent}")


if __name__ == "__main__":
    main()
