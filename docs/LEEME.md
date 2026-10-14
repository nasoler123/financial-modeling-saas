# Producto de modelos financieros

Interfaz React, fórmulas, drivers, dependencias, proyecciones y adaptación a Google Sheets.

## Qué demuestra este caso

El frontend completo necesita componentes compartidos, autenticación y API. La demo usa el motor temporal original con un modelo sintético.

**Resultado del proyecto:** Producto construido; el frontend propio no captó clientes.

## Probar el componente

Requiere Python 3.10 o posterior. No necesita instalar dependencias, introducir claves ni conectar una cuenta.

```sh
python3 -I demo.py
```

La demo usa datos sintéticos y rechaza conexiones de red y subprocesos. Verifica 3 comportamientos del código original. [Resultados](../verification.json).

## Recorrido del código

[source/sample.py](../source/timeseries_engine.py) es la muestra ejecutable. Módulo original completo, sin cambios. [Procedencia completa](../provenance.json).

- [E06 Prototipo financiero React con datos sintéticos](../evidence/E06.md)
- [E07 Registro y autenticación de usuario en frontend](../evidence/E07.md)
- [E08 Parser TypeScript de fórmulas a AST](../evidence/E08.md)
- [E09 Compilación SQL, dependencias y componentes fuertemente conexas](../evidence/E09.md)
- [E10 Grid presupuestario, borradores y protección frente a previews antiguas](../evidence/E10.md)
- [E19 Contrato del add-on, identidad y adaptador de Sheets](../evidence/E19.md)
- [E20 Apps Script, sesión, readback y bridge de hoja/dataset](../evidence/E20.md)
- [E21 BigQuery IAM por workspace y Connected Sheets](../evidence/E21.md)

## Alcance

Este caso conserva una selección de una construcción mayor. Los identificadores de infraestructura y clientes se han anonimizado donde corresponde; la procedencia registra las modificaciones. Para ejecutarla completa se necesitarían sus adaptadores y servicios; esta muestra no despliega ni modifica Chals AI.

[Portada en inglés](../README.md) · [Arquitectura](architecture.md) · [Decisiones](decisions.md) · [Recorrido del código](code-tour.md).
