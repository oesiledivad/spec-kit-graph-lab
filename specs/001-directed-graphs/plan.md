# Implementation Plan: Directed Graphs

**Branch**: `001-directed-graphs` | **Date**: 2026-11-02 | **Spec**: [specs/001-directed-graphs/spec.md](spec.md)

**Input**: Feature specification from `specs/001-directed-graphs/spec.md` and user planning directives.

---

## Summary

Implementar la carga y visualización de grafos dirigidos no ponderados desde archivos CSV mediante una aplicación de línea de comandos en Python (`graphcli`).

El sistema leerá archivos CSV cumpliendo con RFC 4180 (soportando comas en nombres entrecomillados y codificación UTF-8 con o sin BOM), validará el encabezado exacto `source,target` en minúsculas, recortará espacios en blanco circundantes y aplicará detención inmediata ("fail-fast") ante cualquier fila corrupta.

El grafo se modelará en memoria como una lista de adyacencia (`dict[str, set[str]]`) junto a un conjunto explícito de vértices (`set[str]`), permitiendo registrar vértices aislados y deduplicar aristas automáticamente en tiempo constante $O(1)$. La salida del comando `show` emitirá los conteos y listas de vértices y aristas ordenados deterministamente según puntos de código Unicode estándar en `stdout` con código de salida 0, canalizando cualquier error a `stderr` con código 1 o 2 sin exponer tracebacks.

---

## Technical Context

**Language/Version**: Python 3.11 o superior.

**Primary Dependencies**: Ninguna dependencia externa en `src/`. Solo biblioteca estándar de Python (`sys`, `argparse`, `csv`, `pathlib`, `typing`).

**Storage**: N/A (representación del grafo exclusivamente en memoria durante la ejecución del proceso).

**Testing**: `pytest` como ejecutor de pruebas; `networkx` permitido exclusivamente como oráculo de verificación en `tests/`.

**Target Platform**: Multiplataforma (Windows PowerShell / CMD, Linux bash, macOS zsh).

**Project Type**: Herramienta de línea de comandos (CLI) invocable mediante `python -m graphcli show <archivo>`.

**Performance Goals**: Visualizar grafos de dependencias de hasta 10,000 aristas en menos de 1 segundo de tiempo de ejecución (`SC-001`).

**Constraints**:
- Salida determinista byte a byte (`SC-002`, `Principio VI`).
- Cero tracebacks o excepciones internas expuestas al usuario (`SC-004`, `Principio V`).
- Códigos de salida estrictos: `0` (éxito), `1` (archivo no existe o inaccesible), `2` (error de sintaxis, argumentos o formato) (`FR-010`).
- Prohibición total de bibliotecas de grafos en `src/` (`Principio II`).

**Scale/Scope**: Feature 1 de 2. Alcance acotado a carga, validación, deduplicación y visualización. Estructura compatible con el futuro cálculo de grados de entrada y sucesores de Feature 2, sin implementar ordenamiento topológico anticipado (`Principio VII`).

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio Constitucional | Estado | Justificación / Evidencia |
|--------------------------|--------|---------------------------|
| **I. Stack y estructura** | **PASS** | Python 3.11+, solo stdlib en `src/`, pytest en `tests/`, paquete `graphcli`, invocable con `python -m graphcli show <archivo>`. |
| **II. Grafos y algoritmos propios** | **PASS** | Implementación propia en `src/graphcli/graph.py` basada en `dict[str, set[str]]` y `set[str]`. Justificada en `research.md`. NetworkX solo en `tests/`. |
| **III. Pruebas obligatorias** | **PASS** | 20 escenarios de aceptación (`AS-001` a `AS-020`) con pruebas asignadas. Tareas de prueba planificadas antes del código en `tasks.md`. |
| **IV. Spec y código coinciden** | **PASS** | La especificación [spec.md](spec.md) está clarificada (`Status: Clarified`). El plan respeta fielmente todas sus cláusulas. |
| **V. Comportamiento del CLI** | **PASS** | `stdout` para resultados, `stderr` para advertencias/errores, códigos de salida 0, 1 y 2, cero volcados de traceback. |
| **VI. Salida determinista** | **PASS** | Ordenación garantizada por puntos de código Unicode estándar mediante `sorted()`. |
| **VII. Simplicidad** | **PASS** | Solo lo requerido para la Feature 1. Sin dependencias externas, plugins ni lógica anticipada de Feature 2. |

**Evaluación de compuertas (Gates)**: Todas las compuertas aprobadas sin violaciones.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-directed-graphs/
├── spec.md              # Especificación clarificada de la feature
├── plan.md              # Este plan de implementación (/speckit-plan)
├── research.md          # Justificación de diseño y alternativas rechazadas (Fase 0)
├── data-model.md        # Entidades, validaciones y modelo de datos (Fase 1)
├── quickstart.md        # Guía de validación y ejecución de pruebas (Fase 1)
├── contracts/           # Contratos formales de interfaces (Fase 1)
│   ├── cli-contract.md  # Contrato de invocación CLI, stdout, stderr y códigos de salida
│   └── csv-contract.md  # Contrato de formato CSV, delimitadores, BOM y comillas
└── tasks.md             # Tareas ordenadas para implementación (/speckit-tasks)
```

### Source Code (repository root)

```text
src/
└── graphcli/
    ├── __init__.py      # Declaración del paquete graphcli
    ├── __main__.py      # Punto de entrada para ejecución `python -m graphcli`
    ├── cli.py           # Configuración de argparse, subcomando `show` y control de errores
    ├── csv_parser.py    # Parser CSV (RFC 4180, strip, UTF-8 con/sin BOM, fail-fast)
    └── graph.py         # Clase DirectedGraph (lista de adyacencia y conjunto de vértices)

tests/
├── __init__.py
├── fixtures/            # Archivos CSV para casos borde y pruebas de aceptación
│   ├── empty.csv
│   ├── invalid_header.csv
│   ├── malformed_row.csv
│   ├── bom_utf8.csv
│   └── quoted_names.csv
├── test_cli.py          # Pruebas end-to-end de CLI (códigos de salida, stdout, stderr)
├── test_csv_parser.py   # Pruebas unitarias del parser CSV y manejo de errores
└── test_graph.py        # Pruebas unitarias de DirectedGraph y oráculo NetworkX
```

**Structure Decision**: Estructura de paquete único `graphcli` bajo `src/` con suite completa bajo `tests/`, cumpliendo estrictamente con el Principio I de la Constitución.

---

## Complexity Tracking

> *Sin violaciones constitucionales. Todas las compuertas pasan limpiamente.*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *Ninguna* | N/A | N/A |
