# Feature Specification: Topological Sorting

**Feature Branch**: `002-topological-sort`

**Created**: 2026-11-03

**Status**: Clarified

**Input**: User description: "Feature 2 — Topological sorting: Users can ask the application for a topological order of a loaded graph: an ordering of the vertices in which every vertex comes before all the vertices it points to. Builds on Feature 1 (subcomando `show`, mismo formato de archivo y mismas reglas de carga)."

## Clarifications

### Session 2026-11-03
- Q: ¿Cómo pide el usuario el orden topológico? → A: Con un subcomando nuevo `order`: `python -m graphcli order <archivo>`, paralelo a `show`.
- Q: ¿Cuál es el formato de salida? → A: Un vértice por línea en `stdout`, sin encabezado ni numeración, para que la salida se pueda usar directamente en otros programas.
- Q: Si existen varios órdenes válidos, ¿cuál se muestra? → A: Siempre el **menor en orden lexicográfico**: en cada paso se elige, entre los vértices disponibles (sin predecesores pendientes), el menor por código Unicode (mismo criterio que la Feature 001).
- Q: Si no existe orden (hay ciclos), ¿qué ve el usuario y con qué código? → A: Código de salida **3** (nuevo; distinto de 1 = lectura y 2 = formato). En `stderr` se indica que no existe orden y se lista **un ciclo concreto por cada grupo de vértices mutuamente dependientes**, por ejemplo `auth -> session -> user-profile -> auth`. Nada en `stdout` (sin orden parcial).
- Q: `build-with-cycle.csv` tiene dos problemas (`auth -> session -> user-profile -> auth` y `metrics -> metrics`). ¿Se muestra uno o todos? → A: Todos: un ciclo por cada grupo, para que el usuario pueda arreglar todos sus datos en una sola pasada. Cada ciclo empieza en su vértice menor, es el ciclo más corto que pasa por ese vértice, y los ciclos se listan ordenados por su vértice inicial.
- Q: ¿Un auto-lazo cuenta como ciclo? → A: Sí, es un ciclo de longitud 1 y se muestra como `metrics -> metrics`.
- Q: ¿Se incluyen los vértices aislados (como `watch`) en el orden? → A: Sí; se ubican según la regla del menor lexicográfico como cualquier otro vértice sin predecesores.
- Q: ¿Grafo vacío (solo encabezado)? → A: Salida vacía y código 0 (un grafo vacío tiene un orden válido: el vacío).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Obtener un orden válido de procesamiento (Priority: P1)

Como usuario con un grafo de dependencias sin ciclos (un plan de estudios, una compilación, un plan de tareas), quiero pedirle a la herramienta un orden en el que puedo procesar todos los elementos, de modo que cada elemento aparezca antes de todos los que dependen de él.

**Why this priority**: Es el objetivo de la feature: sin un orden válido, no hay valor nuevo para el usuario.

**Independent Test**: Ejecutar `order` sobre `data/small-dag.csv` y verificar que, para cada arista `u -> v`, `u` aparece antes que `v`, y que la salida coincide exactamente con AS-101.

**Acceptance Scenarios**:

1. **AS-101**: **Given** `data/small-dag.csv`, **When** el usuario ejecuta el subcomando `order`, **Then** el sistema escribe en la salida estándar, un vértice por línea:
   ```text
   shirt
   socks
   tie
   undershorts
   pants
   belt
   jacket
   shoes
   watch
   ```
   la salida de errores queda vacía y termina con código 0.
2. **AS-102**: **Given** `data/cs-curriculum.csv`, **When** el usuario ejecuta `order`, **Then** el sistema escribe los 19 vértices, uno por línea, en este orden exacto: `Calculus I`, `Calculus II`, `Computer Networks`, `Discrete Mathematics`, `Linear Algebra`, `Probability and Statistics`, `Programming Fundamentals`, `Computer Architecture`, `Object-Oriented Programming`, `Data Structures`, `Algorithms`, `Databases`, `Machine Learning`, `Operating Systems`, `Distributed Systems`, `Software Engineering`, `Capstone Project`, `Theory of Computation`, `Compilers`; y termina con código 0.
3. **AS-103**: **Given** un archivo con varias soluciones válidas (`c,d` y `a,b`, sin otras aristas), **When** el usuario ejecuta `order` varias veces, **Then** obtiene siempre `a`, `b`, `c`, `d` (el menor orden lexicográfico) con código 0.
4. **AS-106**: **Given** un archivo con un vértice aislado (`watch,` en `data/small-dag.csv`), **When** el usuario ejecuta `order`, **Then** el vértice aislado aparece exactamente una vez en la salida.
5. **AS-107**: **Given** un archivo que solo contiene el encabezado `source,target`, **When** el usuario ejecuta `order`, **Then** la salida estándar queda vacía y termina con código 0.

### User Story 2 - Entender por qué no existe un orden (Priority: P2)

Como usuario con datos que tienen dependencias circulares, quiero que la herramienta me diga que no existe un orden y me muestre todos los ciclos que debo romper.

**Why this priority**: Los datos reales tienen errores (como `build-with-cycle.csv`); un mensaje concreto ahorra tiempo de depuración.

**Independent Test**: Ejecutar `order` sobre `data/build-with-cycle.csv` y verificar mensaje, salida estándar vacía y código 3.

**Acceptance Scenarios**:

1. **AS-104**: **Given** `data/build-with-cycle.csv`, **When** el usuario ejecuta `order`, **Then** la salida estándar queda vacía, la salida de errores contiene exactamente:
   ```text
   error: data/build-with-cycle.csv: no existe un orden topológico; el grafo tiene 2 ciclo(s):
     auth -> session -> user-profile -> auth
     metrics -> metrics
   ```
   y el sistema termina con código 3.
2. **AS-108**: **Given** un archivo cuyo único problema es un auto-lazo (`a,a`), **When** el usuario ejecuta `order`, **Then** la salida de errores lista el ciclo `a -> a` y el sistema termina con código 3.
3. **AS-109**: **Given** un archivo donde un grupo de vértices mutuamente dependientes contiene más de un ciclo (`a,b`, `b,a`, `b,c`, `c,a`), **When** el usuario ejecuta `order`, **Then** se muestra un solo ciclo para ese grupo, el más corto que empieza en su vértice menor: `a -> b -> a`, con código 3.

### User Story 3 - Mismas reglas de archivo que la Feature 1 (Priority: P3)

Como usuario, quiero que `order` acepte y rechace exactamente los mismos archivos que `show`, con los mismos mensajes y códigos.

**Acceptance Scenarios**:

1. **AS-105**: **Given** un archivo inexistente, **When** el usuario ejecuta `order`, **Then** el sistema escribe el error en la salida de errores con el nombre del archivo y termina con código 1 (igual que AS-007).
2. **AS-110**: **Given** un archivo con una fila inválida (por ejemplo tres columnas), **When** el usuario ejecuta `order`, **Then** el sistema reporta el número de línea en la salida de errores y termina con código 2 (igual que AS-010/AS-013), sin mostrar ciclos ni orden.
3. **AS-111**: **Given** que el usuario ejecuta `order` sin indicar archivo, **When** se procesa la invocación, **Then** se muestra el mensaje de uso en la salida de errores y el código es 2, sin traceback.

### Edge Cases

- Vértices aislados: se incluyen (AS-106).
- Auto-lazos: son ciclos de longitud 1 (AS-108).
- Grafo vacío: salida vacía, código 0 (AS-107).
- Aristas duplicadas: no afectan el orden (ya se deduplican en la carga, FR-007 de la Feature 001).
- Vértices que no están en ningún ciclo pero dependen de uno (como `api` y `web` en `build-with-cycle.csv`): no se listan como ciclo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-101**: El sistema DEBE proveer el subcomando `order` (`python -m graphcli order <archivo>`), que carga el grafo con exactamente las mismas reglas de la Feature 001.
- **FR-102**: El orden mostrado DEBE contener cada vértice del grafo exactamente una vez (incluidos los aislados), y para cada arista `u -> v`, `u` DEBE aparecer antes que `v`.
- **FR-103**: Cuando existan varios órdenes válidos, el sistema DEBE mostrar el menor en orden lexicográfico: en cada posición, el menor vértice por código Unicode entre los que ya no tienen predecesores pendientes.
- **FR-104**: La salida exitosa DEBE escribirse en `stdout`, un vértice por línea, sin encabezado ni numeración; un grafo vacío produce salida vacía con código 0.
- **FR-105**: Si el grafo tiene al menos un ciclo (incluidos auto-lazos), el sistema NO DEBE escribir nada en `stdout`, DEBE escribir en `stderr` la línea `error: <archivo>: no existe un orden topológico; el grafo tiene <K> ciclo(s):` seguida de un ciclo por línea con indentación de dos espacios en formato `v1 -> v2 -> ... -> v1`, y DEBE terminar con código de salida 3.
- **FR-106**: El sistema DEBE reportar un ciclo por cada grupo de vértices mutuamente alcanzables que contenga un ciclo. Cada ciclo DEBE empezar en el menor vértice (por código Unicode) de su grupo y ser el más corto que vuelve a él; ante empates se elige siguiendo los vértices menores. Los ciclos se listan ordenados por su vértice inicial.
- **FR-107**: Los errores de lectura (código 1), formato (código 2) y uso (código 2) DEBEN comportarse exactamente igual que en la Feature 001.
- **FR-108**: Los códigos de salida de `order` son: `0` éxito, `1` lectura, `2` formato/uso, `3` el grafo tiene ciclos.

### Key Entities

- **Orden topológico**: secuencia de todos los vértices del grafo que respeta la dirección de cada arista.
- **Ciclo**: secuencia de aristas que vuelve al vértice de partida; impide que exista un orden topológico.
- **Grupo de dependencia circular**: conjunto máximo de vértices en el que cada uno puede alcanzar a todos los demás siguiendo aristas (contiene al menos un ciclo, o es un vértice con auto-lazo).

## Success Criteria *(mandatory)*

- **SC-101**: 100 % de los órdenes producidos son válidos según un verificador independiente.
- **SC-102**: El sistema reporta ciclos (código 3) exactamente cuando un verificador independiente indica que el grafo no es acíclico.
- **SC-103**: Un grafo de 10.000 aristas se ordena en menos de 1 segundo.
- **SC-104**: La misma entrada produce siempre exactamente la misma salida (stdout y stderr).

## Assumptions

- La carga del archivo reutiliza todas las reglas de la Feature 001 (encabezado, BOM, comillas, recorte, líneas en blanco, fail-fast).
- El subcomando `show` de la Feature 001 no cambia su comportamiento.
