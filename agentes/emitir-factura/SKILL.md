---
name: emitir-factura
enjambre: operaciones
description: >
  Emite la factura de un pedido ya registrado. Se activa con: factura este
  pedido, genera la factura, emite el comprobante, saca la factura del pedido.
  Toma un pedido existente y produce su factura con impuestos. No registra el
  pedido (eso es registrar-pedido) ni lo convierte a PDF (eso es la utilidad pdf).
---

# Agente: emitir-factura

Genera la factura de un pedido existente, con impuestos y total.

## DOCUMENTACION QUE CARGA

- `reglas_facturacion.md` — tipos de impuesto y formato de numeración.

## RESULTADO

Devuelve un contrato con: `id_factura`, `id_pedido`, `base`, `impuestos`, `total`.
