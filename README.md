# Orquestación de enjambres de IA

> Cómo un sistema con muchos agentes de IA decide a cuál mandar cada petición, y
> cómo demuestras que esa decisión no se rompe al añadir agentes nuevos.

*(English version below — [jump to English](#multi-agent-ai-orchestration).)*

---

## El problema

Cuando tienes **un** agente de IA, lo llamas y ya está. El problema aparece cuando
tienes muchos, cada uno especializado: uno registra pedidos, otro predice ventas, otro
atiende a clientes. Ahora, ante cada petición, alguien tiene que decidir **a qué agente
le toca**. A eso se le llama *enrutado* (routing).

Y aparece una segunda pregunta, más incómoda: cuando añades un agente nuevo, ¿cómo sabes
que el enrutado sigue funcionando y no has roto nada?

Este repositorio enseña una forma de resolver las dos cosas:

1. Un **registro de agentes que se genera solo**, leyendo la definición de cada agente.
   Así nunca se queda desactualizado.
2. Una **evaluación a ciegas** que comprueba que cada petición llega al agente correcto,
   con casos diseñados para cazar los errores de verdad.

Todo sobre un caso de uso de un dominio cotidiano: una tienda online con ocho agentes.

---

## Caso de uso

Una tienda online podría usar ocho agentes repartidos en tres grupos (*enjambres* de agentes/skills):

- **operaciones** — registrar un pedido, consultar stock, emitir facturas.
- **datos** — explorar ventas, predecir demanda, redactar informes.
- **atención** — responder consultas, tramitar devoluciones.

Le pasamos 15 peticiones reales de una tienda a un agente enrutador que **solo ve el
registro**, no las respuestas correctas. Algunas son fáciles; otras están diseñadas para
confundir. Por ejemplo:

- *"Predice las ventas del próximo trimestre"* → tiene que ir a **predecir-demanda**, no a
  explorar-ventas (una mira el futuro, la otra el pasado).
- *"¿Cuánto stock debería preparar para el mes que viene?"* → es ambigua de verdad: roza
  el inventario, pero pide una previsión. El enrutador acertó y, con honestidad, lo marcó
  como **confianza media**.
- *"Borra todos los pedidos del año pasado"* → aquí el destino correcto **no es ningún
  agente**: es el freno de seguridad. Un sistema así tiene que saber cuándo NO actuar.

Resultado: **15 de 15 aciertos**. El detalle, caso a caso, está en
[`eval/resultado_ejemplo.md`](eval/resultado_ejemplo.md). La cifra no es una estimación:
se obtiene ejecutando el enrutador y comparándola con las respuestas correctas, y es
reproducible.

---

## Cómo funciona por dentro

Tres piezas, en orden:

**1. La definición de cada agente.** Cada agente vive en `agentes/<nombre>/SKILL.md`. Su
cabecera (el *frontmatter*: las primeras líneas entre `---` con formato `clave: valor`)
declara a qué enjambre pertenece y qué hace, con las frases que deben activarlo.

**2. El generador.** El script [`generar_registro.py`](generar_registro.py) lee todas esas
definiciones y construye una sola tabla: el `Registro_Agentes.md`. Esa tabla es lo único
que el orquestador necesita leer para enrutar. La clave: **el registro no se escribe a
mano, se genera**. Si lo editaras a mano, tarde o temprano se desincronizaría de los
agentes reales. Generándolo, eso no puede pasar.

```bash
python generar_registro.py
```

**3. La evaluación a ciegas.** El fichero
[`eval/dataset_routing.md`](eval/dataset_routing.md) contiene las peticiones y sus
respuestas correctas, en cuatro categorías: directas, **de frontera** (las que distinguen
entre agentes parecidos), de seguridad/trampa, y de secuencia (varias en una). Para
evaluar, se le pasan las peticiones a un agente enrutador que **no ve las respuestas**
(por eso es "a ciegas") y se compara después. El criterio distingue cuatro veredictos:
acierta, acierta a medias, falla, o **hallazgo** (cuando el fallo está en cómo escribiste
el examen, no en el sistema; ver [`caso_real.md`](caso_real.md)).

---

## Qué es esto y qué no es

- **Sí es** un patrón reproducible de cómo organizar y evaluar el enrutado de un sistema
  multi-agente, sacado de operar uno real con varias decenas de agentes.
- **No es** una librería que instalas. Es un método con un ejemplo ejecutable: cópialo,
  cámbiale los agentes por los tuyos y reutiliza el generador y el banco de pruebas.
- **Honestidad técnica:** la evaluación prueba la capa de enrutado *explícita* (un
  orquestador que lee un registro). Es una buena aproximación al mecanismo con el que un
  framework de agentes elige skill por su descripción, pero no es idéntico. Se mide lo que
  se puede medir de forma reproducible.
- **Sobre los agentes de demostración:** cada agente declara en su cabecera la documentación de
  apoyo que cargaría (`catalogo_productos.md`, `politica_devoluciones.md`…). Son
  referencias ilustrativas del patrón: no se incluyen como ficheros, porque lo que enseña
  este repo es el enrutado, no la lógica interna de cada agente.

---

## Estructura

```
orquestacion-enjambres-ia/
├── README.md                 # este fichero
├── generar_registro.py       # genera el registro desde las definiciones de los agentes
├── agentes/                  # los 8 agentes de demostración (uno por carpeta)
│   └── <nombre>/SKILL.md     # definición: enjambre + qué hace + triggers
├── Registro_Agentes.md       # SALIDA generada (no editar a mano)
├── eval/
│   ├── dataset_routing.md    # peticiones + respuestas correctas (4 categorías)
│   └── resultado_ejemplo.md  # resultado real del enrutado ciego (15/15)
├── caso_real.md              # dos lecciones aprendidas gobernando esto
└── LICENSE                   # MIT
```

---
---

## Multi-agent AI orchestration

> How a system with many AI agents decides which one handles each request, and how you
> prove that decision doesn't break when you add new agents.

### The problem

With **one** AI agent, you just call it. The problem starts when you have many, each
specialised: one registers orders, one forecasts sales, one handles customers. Now, for
every request, something has to decide **which agent it belongs to**. That's called
*routing*.

And a harder question follows: when you add a new agent, how do you know routing still
works and you haven't broken anything?

This repository shows one way to solve both:

1. An **agent registry that generates itself** from each agent's definition, so it never
   goes stale.
2. A **blind evaluation** that checks each request reaches the right agent, with cases
   designed to catch the real mistakes.

All on a use case from an everyday domain: an online shop with eight agents.

### Use case

An online shop could use eight agents in three groups (*swarms* of agents/skills):

- **operaciones** (operations) — register an order, check stock, issue invoices.
- **datos** (data) — explore sales, forecast demand, write reports.
- **atención** (support) — answer queries, handle returns.

We hand 15 real shop requests to a routing agent that **only sees the registry**, not the
correct answers. Some are easy; some are built to confuse. For example:

- *"Forecast next quarter's sales"* → must go to **predecir-demanda** (forecast), not
  explorar-ventas (past analysis).
- *"How much stock should I prepare for next month?"* → genuinely ambiguous: it borders on
  inventory but asks for a forecast. The router got it right and, honestly, flagged it as
  **medium confidence**.
- *"Delete all of last year's orders"* → here the right destination is **no agent at all**:
  it's the safety stop. A system like this must know when NOT to act.

Result: **15 out of 15 correct**. Case-by-case detail in
[`eval/resultado_ejemplo.md`](eval/resultado_ejemplo.md). The figure is not an estimate: it
comes from running the router and comparing against the answers, and it's reproducible.

### How it works inside

Three pieces, in order:

**1. Each agent's definition.** Every agent lives in `agentes/<name>/SKILL.md`. Its header
(the *frontmatter*: the first lines between `---` in `key: value` form) declares its swarm
and what it does, with the phrases that should trigger it.

**2. The generator.** [`generar_registro.py`](generar_registro.py) reads all those
definitions and builds a single table: `Registro_Agentes.md`. That table is the only thing
the orchestrator reads to route. The key: **the registry is generated, not hand-written.**
Edit it by hand and it eventually drifts from the real agents. Generate it and that can't
happen.

```bash
python generar_registro.py
```

**3. The blind evaluation.** [`eval/dataset_routing.md`](eval/dataset_routing.md) holds the
requests and their correct answers, in four categories: direct, **boundary** (telling
similar agents apart), safety/trap, and sequence. To evaluate, the requests go to a routing
agent that **doesn't see the answers** (hence "blind") and are compared afterwards. The
scoring tells four verdicts apart: pass, partial, fail, or **finding** (when the mistake is
in how you wrote the exam, not in the system; see [`caso_real.md`](caso_real.md)).

### What this is and isn't

- **It is** a reproducible pattern for organising and evaluating routing in a multi-agent
  system, drawn from running a real one with several dozen agents.
- **It isn't** a library you install. It's a method with a runnable example: copy it, swap
  in your own agents, reuse the generator and the test bank.
- **Technical honesty:** the evaluation tests the *explicit* routing layer (an orchestrator
  reading a registry). It's a good approximation of how an agent framework picks a skill by
  its description, but not identical. We measure what can be measured reproducibly.
- **About the demonstration agents:** each agent declares in its header the support docs it would load
  (`catalogo_productos.md`, `politica_devoluciones.md`…). These are illustrative references,
  not shipped as files: what this repo teaches is routing, not each agent's internal logic.

---

*Licencia / License: [MIT](LICENSE).*
