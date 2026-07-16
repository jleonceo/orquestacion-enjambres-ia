---
name: control-stock
enjambre: operaciones
description: >
  Consulta las existencias de un producto y avisa de roturas de stock. Se activa
  con: cuánto stock queda, cuántas unidades hay de un producto, hay existencias
  de, avísame si se agota, nivel de inventario. Responde sobre el estado ACTUAL
  del almacén; no predice demanda futura (eso es predecir-demanda).
---

# Agente: control-stock

Consulta el inventario actual y señala productos por debajo del mínimo.

## DOCUMENTACION QUE CARGA

- `catalogo_productos.md`: productos y umbrales mínimos de stock.
