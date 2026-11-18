"""Diagnostica y muestra las condiciones del equipo en formato JSON."""
import json

from herramientas.labmedicion import describir_entorno


def main() -> None:
    print(json.dumps(describir_entorno(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
