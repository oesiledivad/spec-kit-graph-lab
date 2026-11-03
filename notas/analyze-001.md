# `/speckit-analyze` — Feature 001

> Nota de proceso: la primera corrida de `/speckit-analyze` se hizo con Antigravity CLI (modo solo lectura, sin cambios en el árbol de trabajo). Antes de poder registrar y aplicar las correcciones se agotó la cuota individual de Antigravity ("Individual quota reached… Resets in 95h"). El análisis de consistencia y las correcciones de abajo se completaron con Claude (Cowork) sobre los mismos artefactos (`spec.md`, `plan.md`, `tasks.md`, `contracts/`).

## Corrida 1 — Hallazgos

| ID | Severidad | Categoría | Ubicación | Hallazgo | Corrección (documento) |
|----|-----------|-----------|-----------|----------|------------------------|
| A1 | HIGH | Inconsistencia | spec FR-002, AS-009 vs FR-011, cli-contract | FR-002 y AS-009 dicen que el encabezado inválido se reporta "en la línea 1", pero FR-011 permite líneas en blanco antes del encabezado y el contrato dice "línea N". Una prueba no puede satisfacer ambas. | **spec.md**: se reporta el número de línea real del encabezado. tasks T030 ajustada. |
| A2 | HIGH | Cobertura | spec FR-010 | "No pueda leerse" no define qué pasa con un archivo que no es UTF-8 válido ni con una ruta que es una carpeta. El código podría lanzar `UnicodeDecodeError` (traceback, viola Principio V). | **spec.md**: FR-010 incluye carpeta / permisos / no UTF-8 → código 1; nuevo **AS-020**; fixture y tarea **T034b**; contrato CLI actualizado. |
| A3 | MEDIUM | Cobertura (Principio III) | spec Edge Cases, tasks T034 | "Sin argumento de archivo → código 2" estaba solo en Edge Cases, sin ID de escenario; la constitución exige que cada escenario tenga prueba referenciada por ID. | **spec.md**: nuevo **AS-019**; T034 ahora lo referencia. |
| A4 | MEDIUM | Cobertura | spec SC-001, tasks | SC-001 (10.000 aristas en < 1 s) no tenía ninguna tarea. | **tasks.md**: nueva tarea **T038b** (prueba de rendimiento). |
| A5 | MEDIUM | Ambigüedad | spec FR-001 | FR-001 decía `python -m <paquete>`; el plan ya decidió `graphcli`. | **spec.md**: FR-001 usa `graphcli`. |
| A6 | LOW | Portabilidad | plan.md, quickstart.md | Enlaces absolutos `file:///C:/Users/Laptop/...` que solo funcionan en una máquina. | Enlaces relativos. |
| A7 | LOW | Duplicación | spec Clarifications | La sección tiene el formato de specify ("Clarification 1..3") y el de clarify ("Session …") a la vez. | Se deja: documenta qué decidió cada fase. |

**Métricas (después de corregir):** 15 FR · 20 AS · 41 tareas · Cobertura AS→tarea: 100 % · CRITICAL: 0 · HIGH: 0.

**Constitución:** sin violaciones (graph libs solo en tests, stdlib en `src/`, pruebas antes del código, stdout/stderr y códigos definidos).

## Corrida 2 (después de corregir)

Sin hallazgos CRITICAL ni HIGH. Quedan solo A7 (LOW, aceptado).
