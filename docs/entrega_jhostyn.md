# Entrega de Jhostyn — integrante A

**Roles:** R1 y mitad de R4. **Rama:** `integrante-a-jhostyn`.

## Responsabilidad
Mantener protocolo y condiciones controladas, documentar el entorno y coordinar la ejecución de las mediciones. Revisar la distribución aleatoria y la precarga de archivos para que las estrategias se midan en condiciones comparables.

## Evidencia incluida
- `resultados/evidencia_linea_base.txt`: primera ejecución de `python -m src.linea_base` (n=200 000; una corrida de verificación, 0.583 s).
- `resultados/resultados.csv` y `resultados/resultados.entorno.json`: primera serie formal (10 corridas de tiempo por estrategia y tamaño, más una corrida de memoria por combinación).
- `resultados/repeticion_2.csv` y `resultados/repeticion_2.entorno.json`: segunda serie formal, repetida al observar CV > 10 % en varias condiciones.

Las dos series quedan separadas para que las diferencias entre sesiones puedan examinarse. La caché fue precalentada; los datos representan principalmente ese escenario y no una lectura fría del disco. El CSV de memoria usa `tracemalloc` en una corrida separada.

## Comandos ejecutados
```powershell
python -m src.linea_base
python -m experimentos.ejecutar_experimento
python -m experimentos.ejecutar_experimento --salida resultados/repeticion_2.csv
```

## Siguiente revisión
Revisar incidentes y variables de entorno entre ambas series. El CV combinado supera 10 % en todas las combinaciones de tiempo; informar esa variabilidad y no presentar los intervalos como evidencia concluyente de reproducibilidad.
