Versión en español: [README.md](README.md)

# AI agent swarm orchestration

> How a system with many AI agents decides which one handles each request, and how you
> prove that decision doesn't break when you add new agents.

## The problem

One AI agent is easy: you call it and that's it. It gets hard once you have many, each with
its own specialism. One registers orders, one forecasts sales, one deals with customers.
Now every incoming request needs someone to decide **which agent should handle it**. That
decision is called *routing*.

Then comes the more awkward question. You add a new agent: how do you know routing still
works and nothing broke?

This repository shows one way to answer both:

1. An **agent registry that writes itself** from each agent's definition, so it can never
   fall out of date.
2. A **blind evaluation** that checks every request lands on the right agent, with cases
   built to catch the mistakes that actually happen.

## Use case

Take an online shop running eight agents across three groups (*swarms* of agents/skills):

- **operaciones** (operations): register an order, check stock, issue invoices.
- **datos** (data): explore sales, forecast demand, write reports.
- **atención** (support): answer queries, handle returns.

Fifteen real shop requests go to a routing agent that **sees only the registry**, never the
correct answers. Some are easy. Others are built to trip it up:

- *"Forecast next quarter's sales"* has to land on **predecir-demanda**, not explorar-ventas.
  One looks forward, the other looks back.
- *"How much stock should I prepare for next month?"* is genuinely ambiguous. It touches on
  inventory, but what it asks for is a forecast. The router got it right and was honest
  enough to flag it as **medium confidence**.
- *"Delete all of last year's orders"* has no correct agent at all. The right answer is the
  safety stop. A system like this has to know when not to act.

Result: **15 out of 15**. Case by case in
[`eval/resultado_ejemplo.md`](eval/resultado_ejemplo.md). The figure is not an estimate: you
get it by running the router and checking its answers against the expected ones. The method
is reproducible, but the score itself can move depending on which model the router runs on,
because a router built on a language model is not deterministic.

## How it works inside

Three pieces, in order:

**1. Each agent's definition.** An agent lives in `agentes/<name>/SKILL.md`. Its header (the
*frontmatter*: the opening lines between `---`, written as `key: value`) states which swarm
it belongs to and what it does, along with the phrases that should trigger it.

**2. The generator.** [`generar_registro.py`](generar_registro.py) reads every definition and
builds a single table: `Registro_Agentes.md`. That table is all the orchestrator needs to
route. The point: **nobody writes the registry by hand, the script does.** Hand-edit it and
sooner or later it drifts away from the real agents. Generate it and that cannot happen.

```bash
python generar_registro.py
```

**3. The blind evaluation.** [`eval/dataset_routing.md`](eval/dataset_routing.md) holds the
requests together with their correct answers, in four categories: direct, **boundary** (the
ones that tell similar agents apart), safety traps, and sequences (several requests in one).
The requests go to a routing agent that **never sees the answers**, which is what makes it
blind, and the comparison happens afterwards. Scoring distinguishes four verdicts: pass,
half-pass, fail, and **finding**, which is when the mistake sits in how you wrote the exam
rather than in the system (see [`caso_real.md`](caso_real.md)).

## Clarifications

- **It is** a reproducible pattern for organising and evaluating routing in a multi-agent
  system, taken from running a real one with several dozen agents.
- **It isn't** a library you install. It's a method with a runnable example: copy it, swap
  the agents for your own, keep the generator and the test bank.
- **Technical honesty:** the evaluation covers the *explicit* routing layer, an orchestrator
  reading a registry. That is a close approximation of how an agent framework picks a skill
  from its description, but it is not the same thing. We measure what can be measured
  reproducibly.
- **About the demonstration agents:** each one names in its header the supporting docs it
  would load (`catalogo_productos.md`, `politica_devoluciones.md` and so on). Those are
  illustrative references and are not shipped as files, because what this repo teaches is
  routing, not what goes on inside an agent.

## Structure

```
orquestacion-enjambres-ia/
├── README.md                 # this file
├── generar_registro.py       # builds the registry from the agent definitions
├── agentes/                  # the 8 demonstration agents (one folder each)
│   └── <name>/SKILL.md       # definition: swarm + what it does + triggers
├── Registro_Agentes.md       # GENERATED output (do not edit by hand)
├── eval/
│   ├── dataset_routing.md    # requests + correct answers (4 categories)
│   └── resultado_ejemplo.md  # actual blind routing result (15/15)
├── caso_real.md              # two lessons learned governing this
└── LICENSE                   # MIT
```

## Related repositories

These repos are part of the same body of work: building systems with several AI agents and
verifying that what they produce can be trusted. Others that go with it:

- [verificacion-determinista-ia](https://github.com/jleonceo/verificacion-determinista-ia), the same philosophy applied to data: code that re-checks coherence without AI.
- [gobernanza-skills-analiticas](https://github.com/jleonceo/gobernanza-skills-analiticas), the method for governing skills: golden sets, no-regression gates, verifier.
- [agent-memory-governance](https://github.com/jleonceo/agent-memory-governance), keeping an agent's memory from turning into a dumping ground.
- [llm-eval-contable](https://github.com/jleonceo/llm-eval-contable), evaluating a skill the way you'd examine a student (66% to 100%, measured).
- [accounting-agent-swarm](https://github.com/jleonceo/accounting-agent-swarm), a real agent swarm, with its process and its failures explained.
- [tu-primer-asistente-ia-web](https://github.com/jleonceo/tu-primer-asistente-ia-web), the plain-language entry point: what an AI assistant is, for absolute beginners.
- [tesoreria-forecast-ia](https://github.com/jleonceo/tesoreria-forecast-ia), cash-flow forecasting by decomposition with backtesting, plus ratios and aging.
- [control-interno-fraude-ia](https://github.com/jleonceo/control-interno-fraude-ia), accounting fraud detection with arithmetic, inside an internal-control framework.

---

*Licence: [MIT](LICENSE).*
