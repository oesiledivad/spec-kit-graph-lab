# Clarify — Feature 001: Directed Graphs

Rama: `001-directed-graphs` · Spec: `specs/001-directed-graphs/spec.md`

Cómo usar este archivo:
1. **Antes** de correr `/speckit-clarify`, esta es nuestra lista propia de preguntas (APPROACH.md lo pide).
2. Al terminar cada sesión, llenar la columna **Decisión final** y marcar si la preguntó el agente o la agregamos nosotros.
3. Verificar que cada decisión quedó en un **FR** y en un **escenario de aceptación** del spec, no solo en Clarifications.

Leyenda de "Origen": `specify` = la resolvió `/speckit-specify` · `agente` = la preguntó `/speckit-clarify` · `nosotros` = la agregamos porque el agente no la preguntó.

---

## A. Ya resueltas durante `/speckit-specify` (commit `ed488d9`)

| # | Pregunta | Decisión | Origen | FR / AS |
|---|----------|----------|--------|---------|
| A1 | ¿Cuál es el formato exacto de salida al mostrar un grafo? | `Vertices (N):` + vértices indentados 2 espacios en orden; `Edges (M):` + `  origen -> destino` en orden por origen y luego destino. Grafo vacío: `Vertices (0):` / `Edges (0):` | specify | FR-006, AS-001 |
| A2 | ¿Qué significa una fila con destino vacío (`watch,` en `small-dag.csv`)? | Vértice aislado válido, sin aristas. `,target` (origen vacío) o columnas de más → error de formato | specify | FR-005, AS-004 |
| A3 | ¿Qué pasa con aristas duplicadas (`Data Structures,Algorithms` en `cs-curriculum.csv`)? | Se deduplican en silencio; se muestran una sola vez | specify | FR-007, AS-005 |

---

## B. Sesión 1 de `/speckit-clarify`

| # | Pregunta | Opciones | Recomendación | Decisión final | Origen | FR / AS |
|---|----------|----------|---------------|----------------|--------|---------|
| B1 | ¿Cuál es el nombre exacto del subcomando para mostrar el grafo? | `show` / `display` / `print` | `show` | `show` | agente | FR-001, AS-001 |
| B2 | ¿Qué se hace con líneas en blanco o con solo espacios (p. ej. al final del archivo)? | Ignorarlas / error de formato | Ignorarlas | Se ignoran en silencio | agente | FR-011, AS-011 |
| B3 | ¿Qué se hace con una fila `,` (origen y destino vacíos)? | Ignorarla / error de formato | Error de formato, código 2, con número de línea | Error de formato, código 2, con número de línea | agente | FR-005, AS-012 |
| B4 | Ante una fila inválida, ¿se aborta toda la carga o se omite la fila con advertencia y se sigue? | Abortar en el primer error / omitir y advertir / reportar todos los errores y abortar | Abortar en el primer error | Abortar en el primer error (fail-fast), nada en stdout | agente | FR-012, AS-013 |
| B5 | ¿Qué significa exactamente "orden lexicográfico"? | Por código Unicode, sensible a mayúsculas (`Z` < `a`) / sin distinguir mayúsculas / orden natural (`Calculus 2` < `Calculus 10`) | Por código Unicode, sensible a mayúsculas | Por código Unicode, sensible a mayúsculas | agente | FR-006, AS-014 |

Además, pedirle al agente en esta sesión:
- AS-002 debe dar conteos exactos: **cs-curriculum → 19 vértices, 23 aristas** (24 filas, una duplicada).
- AS-003 debe dar conteos exactos: **build-with-cycle → 11 vértices, 13 aristas** (incluye `metrics -> metrics`).

---

## C. Sesión 2 de `/speckit-clarify`

| # | Pregunta | Opciones | Recomendación | Decisión final | Origen | FR / AS |
|---|----------|----------|---------------|----------------|--------|---------|
| C1 | ¿El encabezado se compara distinguiendo mayúsculas? ¿Se acepta `Source,Target`? | Exacto `source,target` / sin distinguir mayúsculas | Sin distinguir mayúsculas | **Exacto en minúsculas** `source,target` (distinto a la recomendación: `Source,Target` es error) | agente | FR-002, AS-009 |
| C2 | ¿Se acepta un archivo UTF-8 con BOM (típico al guardar desde Excel en Windows)? | Aceptarlo / error | Aceptarlo | Se acepta, el BOM se descarta | agente | FR-002, AS-017 |
| C3 | ¿Se respetan las comillas CSV en nombres con comas (`"Smith, J",X`)? | Sí, CSV estándar / no, la coma siempre separa | Sí, CSV estándar | Sí, CSV estándar (RFC 4180) | agente | FR-015, AS-018 |
| C4 | ¿Se recortan los espacios al inicio y al final de cada nombre (` pants ` → `pants`)? Hoy está solo en Edge Cases. | Recortar / conservar | Recortar, y pasarlo a un FR con su AS | Recortar; pasado a FR/AS | nosotros | FR-013, AS-015 |
| C5 | ¿`Math` y `math` son el mismo vértice? Hoy está solo en Edge Cases. | Distintos / el mismo | Distintos, y pasarlo a un FR con su AS | Distintos; pasado a FR/AS | nosotros | FR-014, AS-016 |

---

## D. Extras (si sobra tiempo o el analyze los señala)

| # | Pregunta | Recomendación | Decisión final |
|---|----------|---------------|----------------|
| D1 | ¿Qué pasa si el archivo no es UTF-8 válido? | Error de lectura, código 1 | Código 1 (agregado en analyze: FR-010, AS-020) |
| D2 | ¿Qué pasa si la ruta es una carpeta y no un archivo? | Error de lectura, código 1 | Código 1 (agregado en analyze: FR-010) |
| D3 | ¿Un vértice puede aparecer como aislado (`watch,`) **y** también en una arista? | Sí, es el mismo vértice; sigue contándose una vez | Sí (conjunto de vértices) |
| D4 | ¿Se aceptan filas con 1 sola columna sin coma (`watch`)? | Error de formato, código 2 (solo `watch,` es aislado) | Error, código 2 (FR-005/AS-010) |
| D5 | ¿Hay advertencias en stderr en algún caso exitoso? | No (la deduplicación es silenciosa) | No |

---

## Pregunta más difícil (para REFLECTION.md)

> Escribir aquí cuál fue y por qué:

Candidata: C1 (encabezado exacto en minúsculas). Rechazar `Source,Target` es estricto y puede sorprender a un usuario que exporta desde Excel, pero es predecible y fácil de explicar; se eligió estrictez sobre tolerancia.

