
#labmedicion.py — Arnés de medición reproducible para el laboratorio.#
#Mide UNA ejecución de una función y devuelve un registro#
from __future__ import annotations

import csv
import datetime as dt
import gc
import json
import os
import platform
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any, Callable

try:  # funciona como script suelto y como paquete (herramientas/)
    from . import sensores  # type: ignore
except ImportError:
    import sensores  # type: ignore

try:
    import psutil  # type: ignore
except ImportError:  # pragma: no cover
    psutil = None

CAMPOS = [
    "marca_tiempo", "equipo", "estrategia", "n", "repeticion",
    "tiempo_s", "cpu_proceso_s", "uso_cpu_pct", "pico_mem_mib", "rss_mib",
    "frecuencia_mhz", "temperatura_c", "energia_j", "potencia_w",
    "medicion_memoria", "observacion",
]

MIB = 1024 * 1024


def describir_entorno() -> dict[str, Any]:
    """Condiciones del experimento que deben documentarse (variables controladas)."""
    info: dict[str, Any] = {
        "fecha": dt.datetime.now().isoformat(timespec="seconds"),
        "sistema": f"{platform.system()} {platform.release()}",
        "maquina": platform.machine(),
        "procesador": platform.processor() or "ver lscpu / Administrador de tareas",
        "nucleos_logicos": os.cpu_count(),
        "python": sys.version.split()[0],
        "implementacion": platform.python_implementation(),
        "psutil": getattr(psutil, "__version__", None),
        "sensores_disponibles": sensores.disponibilidad(),
    }
    if psutil is not None:
        info["memoria_total_gib"] = round(psutil.virtual_memory().total / 1024**3, 2)
        info["nucleos_fisicos"] = psutil.cpu_count(logical=False)
        try:
            bat = psutil.sensors_battery()
            info["conectado_a_corriente"] = None if bat is None else bat.power_plugged
        except (AttributeError, OSError):
            info["conectado_a_corriente"] = None
    return info


class Experimento:
    """Registra mediciones en un CSV y el entorno en un JSON hermano."""

    def __init__(self, ruta_csv: str | Path, equipo: str = "") -> None:
        self.ruta = Path(ruta_csv)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self.equipo = equipo
        nuevo = not self.ruta.exists()
        self._archivo = self.ruta.open("a", newline="", encoding="utf-8")
        self._escritor = csv.DictWriter(self._archivo, fieldnames=CAMPOS)
        if nuevo:
            self._escritor.writeheader()
        entorno = self.ruta.with_suffix(".entorno.json")
        entorno.write_text(json.dumps(describir_entorno(), indent=2, ensure_ascii=False), encoding="utf-8")
        self._proceso = psutil.Process() if psutil else None

    # ------------------------------------------------------------------
    def medir(
        self,
        funcion: Callable[..., Any],
        *args: Any,
        estrategia: str,
        n: int,
        repeticion: int,
        medir_memoria: bool = False,
        observacion: str = "",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Ejecuta funcion(*args, **kwargs) una vez y guarda el registro.

        medir_memoria=False -> corrida de TIEMPO (sin el sobrecosto de tracemalloc)
        medir_memoria=True  -> corrida de MEMORIA (el tiempo queda inflado)
        """
        gc.collect()  # parte de las condiciones controladas: mismo estado inicial
        if medir_memoria:
            tracemalloc.start()

        e0 = sensores.energia_rapl_j()
        c0 = time.process_time()
        t0 = time.perf_counter()
        funcion(*args, **kwargs)
        t1 = time.perf_counter()
        c1 = time.process_time()
        e1 = sensores.energia_rapl_j()

        pico = None
        if medir_memoria:
            _, pico_bytes = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            pico = round(pico_bytes / MIB, 3)

        tiempo = t1 - t0
        cpu = c1 - c0
        energia = sensores.delta_energia_j(e0, e1)
        registro = {
            "marca_tiempo": dt.datetime.now().isoformat(timespec="milliseconds"),
            "equipo": self.equipo,
            "estrategia": estrategia,
            "n": n,
            "repeticion": repeticion,
            "tiempo_s": f"{tiempo:.6f}",
            "cpu_proceso_s": f"{cpu:.6f}",
            "uso_cpu_pct": f"{(cpu / tiempo * 100) if tiempo > 0 else 0:.1f}",
            "pico_mem_mib": "" if pico is None else pico,
            "rss_mib": round(self._proceso.memory_info().rss / MIB, 2) if self._proceso else "",
            "frecuencia_mhz": sensores.frecuencia_mhz() or "",
            "temperatura_c": sensores.temperatura_c() or "",
            "energia_j": "" if energia is None else f"{energia:.4f}",
            "potencia_w": "" if (energia is None or tiempo <= 0) else f"{energia / tiempo:.3f}",
            "medicion_memoria": "si" if medir_memoria else "no",
            "observacion": observacion,
        }
        self._escritor.writerow(registro)
        self._archivo.flush()
        return registro

    def cerrar(self) -> None:
        self._archivo.close()

    def __enter__(self) -> "Experimento":
        return self

    def __exit__(self, *exc: object) -> None:
        self.cerrar()


def calentar(funcion: Callable[..., Any], *args: Any, veces: int = 2, **kwargs: Any) -> None:
    """Ejecuciones de calentamiento que NO se registran (cachés, archivos, JIT del SO)."""
    for _ in range(veces):
        funcion(*args, **kwargs)
