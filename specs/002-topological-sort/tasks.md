# Tasks: Topological Sorting

**Feature**: `002-topological-sort`
**Input**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`
**Tests**: obligatorios (Principio III). Cada escenario AS-101..AS-111 tiene una tarea de prueba que lo referencia; las pruebas van antes del código.

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup

- [X] T101 [P] Crear fixtures en `tests/fixtures/`: `two_chains.csv` (`c,d` y `a,b`), `self_loop_only.csv` (`a,a`), `multi_cycle_group.csv` (`a,b`, `b,a`, `b,c`, `c,a`)

## Phase 2: Foundational

- [X] T102 Prueba unitaria de `DirectedGraph.in_degrees()` en `tests/test_topo.py` (todos los vértices, aislados con 0)
- [X] T103 Implementar `DirectedGraph.in_degrees()` en `src/graphcli/graph.py` en O(V + E)

## Phase 3: User Story 1 — Orden válido (P1) 🎯 MVP

### Tests (antes de implementar)
- [X] T104 [P] [US1] Prueba de aceptación AS-101 (salida exacta de `data/small-dag.csv`) en `tests/test_cli_order.py`
- [X] T105 [P] [US1] Prueba de aceptación AS-102 (orden exacto de `data/cs-curriculum.csv`) en `tests/test_cli_order.py`
- [X] T106 [P] [US1] Prueba de aceptación AS-103 (desempate lexicográfico con `two_chains.csv`, repetida 3 veces) en `tests/test_cli_order.py`
- [X] T107 [P] [US1] Prueba de aceptación AS-106 (vértice aislado `watch` aparece una vez) en `tests/test_cli_order.py`
- [X] T108 [P] [US1] Prueba de aceptación AS-107 (solo encabezado → salida vacía, código 0) en `tests/test_cli_order.py`
- [X] T109 [P] [US1] Pruebas con oráculo NetworkX en `tests/test_topo.py`: orden válido por arista e igual a `nx.lexicographical_topological_sort` para los DAG de `data/` y grafos aleatorios acíclicos

### Implementation
- [X] T110 [US1] Implementar `topological_order()` (Kahn + `heapq`) en `src/graphcli/topo.py`
- [X] T111 [US1] Agregar subcomando `order` en `src/graphcli/cli.py` (un vértice por línea en stdout, código 0)

## Phase 4: User Story 2 — Ciclos (P2)

### Tests (antes de implementar)
- [X] T112 [P] [US2] Prueba de aceptación AS-104 (stderr exacto, stdout vacío, código 3 con `data/build-with-cycle.csv`) en `tests/test_cli_order.py`
- [X] T113 [P] [US2] Prueba de aceptación AS-108 (auto-lazo `a -> a`, código 3) en `tests/test_cli_order.py`
- [X] T114 [P] [US2] Prueba de aceptación AS-109 (un ciclo por grupo: `a -> b -> a`) en `tests/test_cli_order.py`
- [X] T115b [P] [US2] Prueba unitaria de desempate entre ciclos igual de cortos (`a,c`, `c,a`, `a,b`, `b,a` → `a -> b -> a`) en `tests/test_topo.py`
- [X] T115 [P] [US2] Pruebas con oráculo NetworkX en `tests/test_topo.py`: se lanza `CycleError` ⇔ `not nx.is_directed_acyclic_graph`; grupos reportados = SCC circulares de NetworkX; cada ciclo reportado es un ciclo real del grafo

### Implementation
- [X] T116 [US2] Implementar `CycleError` y `find_cycles()` (Tarjan iterativo + BFS por grupo) en `src/graphcli/topo.py`
- [X] T117 [US2] Manejar `CycleError` en `src/graphcli/cli.py`: mensaje de FR-105 en stderr, código 3

## Phase 5: User Story 3 — Mismas reglas de archivo (P3)

- [X] T118 [P] [US3] Prueba de aceptación AS-105 (archivo inexistente → código 1) en `tests/test_cli_order.py`
- [X] T119 [P] [US3] Prueba de aceptación AS-110 (fila con 3 columnas → código 2 con número de línea) en `tests/test_cli_order.py`
- [X] T120 [P] [US3] Prueba de aceptación AS-111 (`order` sin archivo → uso, código 2, sin traceback) en `tests/test_cli_order.py`
- [X] T121 [US3] Verificar que `order` reutiliza `load_graph` y el mismo manejo de errores que `show` en `src/graphcli/cli.py`

## Phase 6: Polish

- [X] T122 [P] Prueba de rendimiento SC-103 (10.000 aristas en < 1 s) en `tests/test_cli_order.py`
- [X] T123 [P] Prueba de determinismo SC-104 (stdout y stderr idénticos en 3 corridas) en `tests/test_cli_order.py`
- [X] T124 Ejecutar `pytest -v` completo (Features 001 y 002) y la validación manual de `quickstart.md`
- [X] T125 Verificar que `src/` no importa librerías de grafos (`grep`)

## Dependencies

- Phase 1 → Phase 2 → Phase 3 (MVP) → Phase 4 → Phase 5 → Phase 6.
- Dentro de cada fase, las pruebas [P] se escriben primero y deben fallar antes de implementar.
