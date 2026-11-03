# Implementation Plan: Topological Sorting

**Branch**: `002-topological-sort` | **Date**: 2026-11-03 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-topological-sort/spec.md` (clarificada) y el código existente de la Feature 001 (`src/graphcli/`).

---

## Summary

Agregar el subcomando `order` a `graphcli`. Reutiliza sin cambios el lector CSV (`csv_parser.load_graph`) y la representación `DirectedGraph` de la Feature 001. El orden se calcula con el **algoritmo de Kahn** usando un **heap** (`heapq`) como cola de prioridad para obtener siempre el menor orden lexicográfico. Si Kahn no logra procesar todos los vértices, hay ciclos: se calculan los **grupos de dependencia circular** (componentes fuertemente conexas, algoritmo de Tarjan iterativo) y, por cada grupo con ciclo, el ciclo más corto desde su vértice menor (BFS con sucesores ordenados). Los ciclos se reportan en `stderr` con código 3.

---

## Technical Context

**Language/Version**: Python 3.11+ (igual que 001).

**Primary Dependencies**: solo biblioteca estándar (`heapq`, `collections.deque`).

**Testing**: pytest; NetworkX solo en `tests/` como oráculo (`nx.is_directed_acyclic_graph`, `nx.lexicographical_topological_sort`, `nx.strongly_connected_components`).

**Project Type**: mismo CLI (`python -m graphcli order <archivo>`).

**Performance Goals**: 10.000 aristas en < 1 s (SC-103). Complejidad: Kahn con heap O((V + E) log V); Tarjan O(V + E); BFS por grupo O(V + E) en total.

**Constraints**: determinismo (Principio VI), sin librerías de grafos (Principio II), código 3 nuevo definido en la spec (Principio V).

**Scale/Scope**: Feature 2 de 2. No se modifica el comportamiento de `show`.

---

## Constitution Check

| Principio | Estado | Evidencia |
|-----------|--------|-----------|
| I. Stack y estructura | PASS | Mismo paquete `graphcli`, nuevo módulo `src/graphcli/topo.py`, pruebas en `tests/test_topo.py` y `tests/test_cli_order.py`. |
| II. Grafos propios | PASS | Kahn, Tarjan y BFS implementados a mano. NetworkX solo en tests como oráculo. |
| III. Pruebas obligatorias | PASS | AS-101..AS-111 con prueba referenciada por ID; pruebas antes del código en `tasks.md`. |
| IV. Spec y código coinciden | PASS | Ver "Cambios a la Feature 001": solo código interno, sin cambio de comportamiento ni de spec 001. |
| V. CLI | PASS | stdout solo para el orden; ciclos y errores en stderr; códigos 0/1/2/3 definidos en FR-108. |
| VI. Determinismo | PASS | Heap con desempate por código Unicode; ciclos canónicos (FR-106). |
| VII. Simplicidad | PASS | Un módulo nuevo y un subcomando; sin opciones extra. |

---

## Cambios a la Feature 001 (código, no spec)

`DirectedGraph.in_degree(v)` recorre todas las listas de adyacencia: O(V + E) por llamada. Usarlo para cada vértice en Kahn daría O(V·(V + E)), lo que rompe SC-103. Se agrega el método **`in_degrees() -> dict[str, int]`** que calcula todos los grados de entrada en una sola pasada O(V + E). Es un agregado interno; `show` y la spec 001 no cambian. La representación (lista de adyacencia + conjunto de vértices) se mantiene: Kahn necesita sucesores (O(grado) con `successors`) y grados de entrada (`in_degrees`).

---

## Project Structure

```text
specs/002-topological-sort/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/cli-contract.md
├── checklists/requirements.md
└── tasks.md

src/graphcli/
├── graph.py        # + in_degrees()
├── topo.py         # NUEVO: topological_order(), find_cycles(), CycleError
└── cli.py          # + subcomando order, código 3

tests/
├── fixtures/       # + two_chains.csv, self_loop_only.csv, multi_cycle_group.csv
├── test_topo.py        # NUEVO: unitarias + oráculo NetworkX
└── test_cli_order.py   # NUEVO: aceptación AS-101..AS-111
```

## Complexity Tracking

Sin violaciones.
