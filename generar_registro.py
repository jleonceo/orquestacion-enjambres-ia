"""Genera Registro_Agentes.md DERIVÁNDOLO de la definición de cada agente.

Es el índice ligero que lee el orquestador para enrutar: qué agentes hay, en qué
enjambre viven (campo `enjambre:` del frontmatter), qué hacen (su `description`),
qué documentación de apoyo cargan y si devuelven un contrato de resultado.

Idea central: el registro NO se edita a mano. Se recalcula desde los propios
agentes. Así no se desincroniza: si añades un agente y olvidas regenerar, el
agente queda invisible al enrutado (ver caso_real.md). Por eso este paso es
obligatorio tras dar de alta un agente.

Uso:
    python generar_registro.py

Lee  ./agentes/<nombre>/SKILL.md   (frontmatter YAML + cuerpo Markdown)
Escribe  ./Registro_Agentes.md

Sin dependencias externas: solo biblioteca estándar.
"""
import os
import re
import glob
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.join(AQUI, "agentes")
OUT = os.path.join(AQUI, "Registro_Agentes.md")

HEADING_RE = re.compile(r"^#{1,6}\s")
BACKTICK_RE = re.compile(r"`([^`]+)`")
DOC_FILE_RE = re.compile(r".+\.(md|txt)$", re.IGNORECASE)
KEY_RE = re.compile(r"([A-Za-z_][\w-]*):\s*(.*)$")
DOC_HEADING = "DOCUMENTACION QUE CARGA"  # encabezado que marca la lista de apoyo
# Orden de presentación de los enjambres en el registro.
ORDEN = ["operaciones", "datos", "atencion", "utilidad", "(sin enjambre)"]


def parse_frontmatter(lines):
    """Devuelve un dict con el frontmatter YAML, resolviendo bloques '>' y '|' multilínea."""
    fm = {}
    if not lines or lines[0].strip() != "---":
        return fm
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        ln = lines[i]
        if not ln.startswith((" ", "\t")):
            m = KEY_RE.match(ln)
            if m:
                key, val = m.group(1), m.group(2).strip()
                # Bloque multilínea: '>' (plegado) o '|' (literal) y sus variantes.
                if val in (">", "|", ">-", "|-", ">+", "|+", ""):
                    buff, j = [], i + 1
                    while (j < len(lines) and lines[j].strip() != "---"
                           and (lines[j].startswith((" ", "\t")) or not lines[j].strip())):
                        if lines[j].strip():
                            buff.append(lines[j].strip())
                        j += 1
                    fm[key] = " ".join(buff)
                    i = j
                    continue
                fm[key] = val
        i += 1
    return fm


def parse(path):
    """Extrae de un SKILL.md: nombre, enjambre, descripción, docs de apoyo y si hay contrato."""
    nombre = os.path.basename(os.path.dirname(path))
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    fm = parse_frontmatter(lines)
    nombre = fm.get("name", nombre)
    enjambre = fm.get("enjambre", "(sin enjambre)")
    desc = fm.get("description", "").strip()
    desc = desc[:200] + ("…" if len(desc) > 200 else "")

    docs, in_docs, contrato = [], False, False
    for ln in lines:
        if HEADING_RE.match(ln):
            up = ln.upper()
            in_docs = DOC_HEADING in up
            if "RESULTADO" in up or "RESULT CONTRACT" in up:
                contrato = True
        elif in_docs:
            for tok in BACKTICK_RE.findall(ln):
                if DOC_FILE_RE.match(tok) and tok not in docs:
                    docs.append(tok)
    return nombre, enjambre, desc, docs, contrato


def main():
    files = sorted(glob.glob(os.path.join(AGENTS_DIR, "*", "SKILL.md")))
    if not files:
        raise SystemExit(f"No hay agentes en {AGENTS_DIR}. ¿Ruta correcta?")

    por_enj = {}
    for p in files:
        nombre, enj, desc, docs, contrato = parse(p)
        por_enj.setdefault(enj, []).append((nombre, desc, docs, contrato))

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    L = ["# Registro de Agentes (GENERADO: no editar a mano)", ""]
    L.append(f"> Autogenerado por `generar_registro.py` el **{ts}** desde `agentes/*/SKILL.md`.")
    L.append(f"> Índice que lee el orquestador para enrutar. {len(files)} agentes.")
    L.append("")

    enjs = [e for e in ORDEN if e in por_enj] + [e for e in por_enj if e not in ORDEN]
    for enj in enjs:
        items = sorted(por_enj[enj])
        L.append(f"## {enj}  ({len(items)})")
        L.append("")
        L.append("| Agente | Qué hace (triggers) | Documentación que carga | Contrato |")
        L.append("|---|---|---|---|")
        for nombre, desc, docs, contrato in items:
            doc_cell = ", ".join(f"`{d}`" for d in docs) if docs else "(ninguna)"
            L.append(f"| `{nombre}` | {desc or '(sin descripción)'} | {doc_cell} | {'sí' if contrato else 'no'} |")
        L.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    resumen = " · ".join(f"{e}:{len(por_enj[e])}" for e in enjs)
    print(f"REGISTRO_OK {ts} | {len(files)} agentes | {resumen}")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
