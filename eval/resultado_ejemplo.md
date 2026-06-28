# Resultado de ejemplo — enrutado ciego

> Esto NO es un resultado inventado. Se obtuvo pasando las 15 peticiones de
> `dataset_routing.md` a un agente enrutador que solo veía el `Registro_Agentes.md`
> (no las respuestas correctas) y comparando después con la verdad del dataset.
> Es reproducible: regenera el registro, pásale las peticiones a tu modelo y compara.

## Veredicto

**15/15 acertados a nivel de agente.**

| # | Petición (resumen) | Verdad | Decisión ciega | Resultado |
|---|---|---|---|---|
| 1 | Alta de pedido | operaciones · registrar-pedido | registrar-pedido | PASA |
| 2 | Unidades del SKU-204 | operaciones · control-stock | control-stock | PASA |
| 3 | Patrones en las ventas | datos · explorar-ventas | explorar-ventas | PASA |
| 4 | Dónde está mi envío | atencion · responder-consulta | responder-consulta | PASA |
| 5 | Tablas de un PDF | utilidad:pdf | utilidad:pdf | PASA |
| 6 | Ventas del próximo trimestre | datos · predecir-demanda | predecir-demanda | PASA |
| 7 | Stock para el mes que viene | datos · predecir-demanda | predecir-demanda *(confianza media)* | PASA |
| 8 | Factura el pedido 1024 | operaciones · emitir-factura | emitir-factura | PASA |
| 9 | Conclusiones para el comité | datos · informe-direccion | informe-direccion | PASA |
| 10 | Devolver unos zapatos | atencion · gestionar-devolucion | gestionar-devolucion | PASA |
| 11 | El tiempo en Valencia | NINGUNA | NINGUNA | PASA |
| 12 | Borra todos los pedidos | FRENO | FRENO | PASA |
| 13 | Cómo funciona el registro | NINGUNA | NINGUNA | PASA |
| 14 | Factura 1024 y dámela en PDF | emitir-factura → utilidad:pdf | emitir-factura → utilidad:pdf | PASA |
| 15 | Devolución 880 + email | gestionar-devolucion → utilidad:email | gestionar-devolucion → utilidad:email | PASA |

## Lo que enseña este resultado

- **El caso 7 es el interesante.** "Cuánto stock preparar para el mes que viene" roza
  `control-stock` (inventario), pero pide una previsión: va a `predecir-demanda`. El
  enrutador lo acertó y, honestamente, lo marcó como **confianza media**: es ambiguo de
  verdad. Un enrutador que dijera "alta" en todo escondería esa ambigüedad.
- **El caso 12 se frenó.** Ante una orden destructiva ("borra todos los pedidos"), el
  destino correcto no es ningún agente: es el guardarraíl. Un sistema multi-agente tiene
  que saber NO actuar.
- **Las secuencias (14, 15) se reconocen como dos pasos**, no como un único agente.

Un acierto del 100% en 15 casos no significa "esto nunca falla". Significa que, en este
banco, las descripciones discriminan bien. La forma de seguir confiando es volver a medir
cada vez que se añade un agente (ver `caso_real.md`, lección 1).
