"""Pruebas de equivalencia: ninguna estrategia rápida pero incorrecta es mejora."""
import tempfile
import unittest
from pathlib import Path

from src import estrategia_b, estrategia_c, linea_base
from src.generar_datos import generar_ventas


class TestCorreccion(unittest.TestCase):
    def test_tres_estrategias_producen_los_mismos_totales(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "ventas.csv"
            generar_ventas(ruta, 1000, semilla=17)
            esperado = linea_base.ejecutar(ruta)
            self.assertEqual(estrategia_b.ejecutar(ruta), esperado)
            self.assertEqual(estrategia_c.ejecutar(ruta), esperado)
            self.assertEqual(len(esperado), 6)

    def test_resultados_redondeados_a_centavos(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "ventas.csv"
            generar_ventas(ruta, 100, semilla=2)
            for modulo in (linea_base, estrategia_b, estrategia_c):
                self.assertTrue(all(round(total, 2) == total for total in modulo.ejecutar(ruta).values()))


if __name__ == "__main__":
    unittest.main()
