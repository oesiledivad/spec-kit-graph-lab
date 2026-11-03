# Tasks: Directed Graphs

**Feature**: Directed Graphs (`001-directed-graphs`)  
**Input**: Design documents from `specs/001-directed-graphs/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`)  
**Prerequisites**: `plan.md`, `spec.md`, `constitution.md`, `data-model.md`, `contracts/`  
**Tests**: Mandatory per Constitution (Principio III) and user instructions. Every acceptance scenario (`AS-001` to `AS-020`) has an automated test task referencing its ID, and tests are placed before implementation.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US1]`, `[US2]`, `[US3]`)
- Every task includes exact file paths

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure and dependency configuration

- [X] T001 Create project directories `src/graphcli/` and `tests/fixtures/` per `plan.md`
- [X] T002 [P] Configure project packaging and dependencies in `pyproject.toml` with `pytest` and `networkx` as test dependencies
- [X] T003 [P] Create package initialization files `src/graphcli/__init__.py` (nota de implementación: `tests/__init__.py` no se creó; las pruebas usan `tests/conftest.py` y `pythonpath` en `pyproject.toml`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and baseline modules that all user stories depend on

*⚠️ CRITICAL: Must complete before user story implementation begins*

- [X] T004 Create `DirectedGraph` data structure in `src/graphcli/graph.py` with `vertices: set[str]` and `_adj: dict[str, set[str]]`, implementing `add_vertex`, `add_edge`, `get_vertices`, `get_edges`, `vertex_count`, `edge_count`, `successors`, and `in_degree`
- [X] T005 [P] Create baseline CSV parser module skeleton in `src/graphcli/csv_parser.py` using `csv.reader` and `utf-8-sig` encoding
- [X] T006 [P] Create baseline CLI entry point scaffolding in `src/graphcli/cli.py` and `src/graphcli/__main__.py` with `argparse` configuration

---

## Phase 3: User Story 1 - Carga y visualización de grafos dirigidos válidos (Priority: P1) 🎯 MVP

**Goal**: Load a valid directed graph from a CSV file and display its vertices and edges in a structured, deterministic output format sorted by Unicode code point ascending order.

**Independent Test**: Execute `python -m graphcli show data/small-dag.csv` and verify exact stdout format and return code 0.

### Tests for User Story 1 (Written and failing BEFORE implementation)

- [X] T007 [P] [US1] Create test fixture `tests/fixtures/case_order.csv` containing mixed uppercase and lowercase vertices (`Beta`, `alpha`)
- [X] T008 [P] [US1] Implement unit and NetworkX oracle tests for `DirectedGraph` in `tests/test_graph.py` verifying node/edge counts, edge deduplication, and isolated vertices
- [X] T009 [P] [US1] Implement automated acceptance test for AS-001 (`data/small-dag.csv` showing 9 vertices and 9 edges with exact output and exit code 0) in `tests/test_cli.py`
- [X] T010 [P] [US1] Implement automated acceptance test for AS-002 (`data/cs-curriculum.csv` showing 19 vertices and 23 edges with exact counts and exit code 0) in `tests/test_cli.py`
- [X] T011 [P] [US1] Implement automated acceptance test for AS-003 (`data/build-with-cycle.csv` showing 11 vertices and 13 edges with exit code 0) in `tests/test_cli.py`
- [X] T012 [P] [US1] Implement automated acceptance test for AS-014 (sorting mixed case vertices `Beta` before `alpha` and edge `Beta -> alpha` before `alpha -> Beta` using `tests/fixtures/case_order.csv`) in `tests/test_cli.py`

### Implementation for User Story 1

- [X] T013 [US1] Implement deterministic output formatter in `src/graphcli/cli.py` formatting `Vertices (<N>):` and `Edges (<M>):` with two-space indentation and Unicode sorting per `cli-contract.md`
- [X] T014 [US1] Implement the `show` subcommand execution in `src/graphcli/cli.py` loading the graph via `src/graphcli/csv_parser.py` and writing output to `stdout` with exit code 0
- [X] T015 [US1] Wire CLI execution in `src/graphcli/__main__.py` to dispatch `show` command arguments from `sys.argv` to `src/graphcli/cli.py`

**Checkpoint**: User Story 1 fully functional as MVP. Can load and display any valid directed graph deterministically.

---

## Phase 4: User Story 2 - Soporte de datos atípicos y casos especiales (Priority: P2)

**Goal**: Support isolated vertices (`watch,`), self-loops (`metrics -> metrics`), duplicate edge deduplication, blank lines, whitespace trimming, case-sensitivity, UTF-8 BOM, and RFC 4180 quotes.

**Independent Test**: Execute `python -m graphcli show` with CSVs containing isolated vertices, duplicate edges, BOM, and quoted names with commas.

### Tests for User Story 2 (Written and failing BEFORE implementation)

- [X] T016 [P] [US2] Create test fixtures in `tests/fixtures/` for atypical scenarios: `isolated_vertex.csv`, `duplicate_edges.csv`, `self_loop.csv`, `blank_lines.csv`, `whitespace_names.csv`, `case_sensitive_names.csv`, `bom_utf8.csv`, and `quoted_names.csv`
- [X] T017 [P] [US2] Implement automated acceptance test for AS-004 (isolated vertex with empty target `watch,` in `tests/fixtures/isolated_vertex.csv`) in `tests/test_csv_parser.py` and `tests/test_cli.py`
- [X] T018 [P] [US2] Implement automated acceptance test for AS-005 (silent edge deduplication for `Data Structures,Algorithms` in `data/cs-curriculum.csv`) in `tests/test_graph.py` and `tests/test_cli.py`
- [X] T019 [P] [US2] Implement automated acceptance test for AS-006 (self-loop edge `metrics,metrics` in `data/build-with-cycle.csv`) in `tests/test_graph.py` and `tests/test_cli.py`
- [X] T020 [P] [US2] Implement automated acceptance test for AS-011 (silently ignoring blank lines and lines with whitespace in `tests/fixtures/blank_lines.csv`) in `tests/test_csv_parser.py` and `tests/test_cli.py`
- [X] T021 [P] [US2] Implement automated acceptance test for AS-015 (trimming whitespace around names and delimiters ` undershorts , pants ` in `tests/fixtures/whitespace_names.csv`) in `tests/test_csv_parser.py` and `tests/test_cli.py`
- [X] T022 [P] [US2] Implement automated acceptance test for AS-016 (case sensitivity treating `Math` and `math` as distinct vertices in `tests/fixtures/case_sensitive_names.csv`) in `tests/test_graph.py` and `tests/test_cli.py`
- [X] T023 [P] [US2] Implement automated acceptance test for AS-017 (transparent support for UTF-8 with BOM prefix `\ufeff` in `tests/fixtures/bom_utf8.csv`) in `tests/test_csv_parser.py` and `tests/test_cli.py`
- [X] T024 [P] [US2] Implement automated acceptance test for AS-018 (handling commas inside quoted vertex names `"Algorithms, Part I",Compilers` in `tests/fixtures/quoted_names.csv`) in `tests/test_csv_parser.py` and `tests/test_cli.py`

### Implementation for User Story 2

- [X] T025 [US2] Implement whitespace trimming (`FR-013`), RFC 4180 quote preservation with outer quote stripping (`FR-015`), and UTF-8 BOM removal (`FR-002`) in `src/graphcli/csv_parser.py`
- [X] T026 [US2] Enhance `src/graphcli/graph.py` to ensure case-sensitive vertex identity (`FR-014`), isolated vertex handling (`FR-005`), and automatic edge deduplication (`FR-007`)

**Checkpoint**: User Stories 1 and 2 fully functional. Real-world CSV peculiarities handled seamlessly.

---

## Phase 5: User Story 3 - Manejo robusto de errores de entrada y argumentos (Priority: P3)

**Goal**: Implement robust error detection and fail-fast abort on corrupt or missing files, outputting clear error messages with file and line number to `stderr` without tracebacks.

**Independent Test**: Execute `python -m graphcli show` with non-existent, empty, and malformed files, verifying `stderr` message, absence of `stdout`, and exit codes 1 and 2.

### Tests for User Story 3 (Written and failing BEFORE implementation)

- [X] T027 [P] [US3] Create test fixtures in `tests/fixtures/` for error scenarios: `empty.csv` (0 bytes), `invalid_header.csv`, `header_uppercase.csv`, `malformed_columns.csv`, `empty_fields_comma.csv`, and `fail_fast_intermediate.csv`
- [X] T028 [P] [US3] Implement automated acceptance test for AS-007 (non-existent file reports file name in `stderr` with exit code 1) in `tests/test_cli.py`
- [X] T029 [P] [US3] Implement automated acceptance test for AS-008 (empty file 0 bytes reports missing header on line 1 in `stderr` with exit code 2) in `tests/test_cli.py`
- [X] T030 [P] [US3] Implement automated acceptance test for AS-009 (header mismatch or uppercase `Source,Target` reports invalid header with its real line number in `stderr` with exit code 2) in `tests/test_cli.py`
- [X] T031 [P] [US3] Implement automated acceptance test for AS-010 (row with column count != 2 reports line number in `stderr` with exit code 2) in `tests/test_cli.py`
- [X] T032 [P] [US3] Implement automated acceptance test for AS-012 (row with only comma or spaces ` , ` reports line number in `stderr` with exit code 2) in `tests/test_cli.py`
- [X] T033 [P] [US3] Implement automated acceptance test for AS-013 (fail-fast immediate abort on first malformed row, reporting line in `stderr`, empty `stdout`, with exit code 2) in `tests/test_cli.py`
- [X] T034 [P] [US3] Implement automated acceptance test for AS-019 (missing file argument reports usage in `stderr` with exit code 2 and zero Python tracebacks) in `tests/test_cli.py`
- [X] T034b [P] [US3] Create fixture `tests/fixtures/latin1.csv` and implement automated acceptance test for AS-020 (non-UTF-8 file reports file name in `stderr` with exit code 1) in `tests/test_cli.py`

### Implementation for User Story 3

- [X] T035 [US3] Implement structured exception types and fail-fast parsing validation with line number tracking in `src/graphcli/csv_parser.py` for empty files, invalid headers, and malformed rows (`FR-002`, `FR-005`, `FR-012`)
- [X] T036 [US3] Implement CLI error handling in `src/graphcli/cli.py` capturing file errors, parse errors, and argument errors, writing clear messages to `stderr` with exit codes 1 and 2, suppressing tracebacks (`FR-009`, `FR-010`, `SC-004`)

**Checkpoint**: All three user stories fully functional, robust against bad input and compliant with CLI conventions.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end verification, test oracle validation, and code quality checks

- [X] T037 [P] Execute end-to-end validation scenarios against `specs/001-directed-graphs/quickstart.md`
- [X] T038 [P] Run full test suite with `pytest -v` verifying 100% pass rate across all 20 acceptance scenarios (`AS-001` to `AS-020`)
- [X] T038b [P] Implement performance test for SC-001 (generated graph with 10,000 edges is displayed in under 1 second) in `tests/test_cli.py`
- [X] T039 Clean up code, add type annotations and docstrings across `src/graphcli/` and `tests/`

---

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1 (Setup)**: No dependencies — starts immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3 (User Story 1 - P1)**: Depends on Phase 2 — MVP delivery
- **Phase 4 (User Story 2 - P2)**: Depends on Phase 3 completion
- **Phase 5 (User Story 3 - P3)**: Depends on Phase 4 completion
- **Phase 6 (Polish)**: Depends on all user stories complete

### Within Each User Story
- Test fixtures created first
- Automated acceptance tests written and verified FAILING before implementation
- Implementation completed to satisfy tests
- Automated tests verified PASSING

---

## Parallel Execution Opportunities

- Phase 1: T002 and T003 can run in parallel.
- Phase 2: T005 and T006 can run in parallel once T004 is defined.
- Phase 3: Test tasks T007, T008, T009, T010, T011, T012 can all run in parallel.
- Phase 4: Fixture task T016 and test tasks T017 through T024 can all run in parallel.
- Phase 5: Fixture task T027 and test tasks T028 through T034 can all run in parallel.
- Phase 6: Validation tasks T037 and T038 can run in parallel.

---

## Implementation Strategy (MVP First)

1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Complete Phase 3 (User Story 1): write tests T007-T012, implement T013-T015.
3. **VALIDATE MVP**: Run `pytest` on US1 tests and execute `python -m graphcli show data/small-dag.csv`.
4. Proceed to Phase 4 (User Story 2) for edge cases and RFC 4180 parsing.
5. Proceed to Phase 5 (User Story 3) for fail-fast error handling and exit codes.
6. Run Phase 6 (Polish & Verification) against `quickstart.md`.
