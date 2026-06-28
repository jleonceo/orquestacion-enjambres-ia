# Registro de Agentes (GENERADO — no editar a mano)

> Autogenerado por `generar_registro.py` el **2026-06-28 17:54** desde `agentes/*/SKILL.md`.
> Índice que lee el orquestador para enrutar. 8 agentes.

## operaciones  (3)

| Agente | Qué hace (triggers) | Documentación que carga | Contrato |
|---|---|---|---|
| `control-stock` | Consulta las existencias de un producto y avisa de roturas de stock. Se activa con: cuánto stock queda, cuántas unidades hay de un producto, hay existencias de, avísame si se agota, nivel de inventari… | `catalogo_productos.md` | — |
| `emitir-factura` | Emite la factura de un pedido ya registrado. Se activa con: factura este pedido, genera la factura, emite el comprobante, saca la factura del pedido. Toma un pedido existente y produce su factura con … | `reglas_facturacion.md` | sí |
| `registrar-pedido` | Registra un pedido nuevo en la tienda. Se activa cuando el usuario dice: nuevo pedido, dar de alta un pedido, añadir líneas a un pedido, anota este pedido, registra la compra de un cliente. Crea la ca… | `catalogo_productos.md` | sí |

## datos  (3)

| Agente | Qué hace (triggers) | Documentación que carga | Contrato |
|---|---|---|---|
| `explorar-ventas` | Explora un histórico de ventas y describe qué hay dentro: patrones, estacionalidad, productos top, segmentos. Se activa con: analiza estas ventas, qué patrones hay, explora el histórico, dame un EDA d… | `metodo_eda.md` | — |
| `informe-direccion` | Traduce los hallazgos de un análisis a un informe para dirección. Se activa con: prepárame el informe para el comité, resume esto para dirección, pásalo a un informe ejecutivo, redacta las conclusione… | `plantilla_informe.md` | — |
| `predecir-demanda` | Predice la demanda o las ventas futuras a partir del histórico. Se activa con: predice las ventas del próximo mes, cuánta demanda habrá, forecast de ventas, estima las unidades que venderé. Proyecta e… | `metodo_forecast.md` | — |

## atencion  (2)

| Agente | Qué hace (triggers) | Documentación que carga | Contrato |
|---|---|---|---|
| `gestionar-devolucion` | Tramita la devolución o el reembolso de un pedido. Se activa con: el cliente quiere devolver, tramita la devolución, gestiona el reembolso, procesa la devolución de este pedido. Aplica la política de … | `politica_devoluciones.md` | sí |
| `responder-consulta` | Responde dudas de un cliente sobre productos o sobre el estado de su pedido. Se activa con: el cliente pregunta por su pedido, responde esta consulta, dónde está mi envío, qué características tiene es… | `faq_clientes.md` | — |

