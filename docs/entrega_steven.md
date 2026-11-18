# Entrega de Steven — integrante B

**Rol:** R2 y revisión de las alternativas de R3. **Rama:** `integrante-b-steven`.

## Responsabilidad
Explicar la línea base, comprobar que las tres estrategias conservan los mismos totales por región y revisar que una mejora de rendimiento no cambie el resultado. Los cambios de esta rama fortalecen las pruebas, incluido el caso de un CSV válido sin filas de datos.

## Evidencia
`pruebas/test_correccion.py` verifica equivalencia con datos deterministas, que se producen seis regiones y que los totales se redondean a centavos. También verifica que las tres implementaciones devuelven `{}` cuando el CSV solo contiene encabezados.

## Revisión para integrar
Antes de aprobar cambios de estrategia, ejecutar:
```powershell
python -m unittest discover -s pruebas
```
Comparar cada resultado con `src.linea_base.ejecutar` y revisar que no se alteren los encabezados esperados del CSV.
