# Feature Specification: Topological Sorting

**Feature Branch**: `002-topological-sort`

**Created**: 2026-11-03

**Status**: Draft

**Input**: User description: "Feature 2 — Topological sorting: Users can ask the application for a topological order of a loaded graph: an ordering of the vertices in which every vertex comes before all the vertices it points to. Builds on Feature 1 (subcomando `show`, mismo formato de archivo y mismas reglas de carga)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Obtener un orden válido de procesamiento (Priority: P1)

Como usuario con un grafo de dependencias sin ciclos (un plan de estudios, una compilación, un plan de tareas), quiero pedirle a la herramienta un orden en el que puedo procesar todos los elementos, de modo que cada elemento aparezca antes de todos los que dependen de él.

**Why this priority**: Es el objetivo de la feature: sin un orden válido, no hay valor nuevo para el usuario.

**Independent Test**: Ejecutar el subcomando de orden sobre `data/small-dag.csv` y verificar que, para cada arista `u -> v`, `u` aparece antes que `v`.

**Acceptance Scenarios**:

1. **AS-101**: **Given** `data/small-dag.csv`, **When** el usuario pide el orden topológico, **Then** el sistema muestra los 9 vértices en un orden válido y termina con código 0. [NEEDS CLARIFICATION: formato exacto de salida]
2. **AS-102**: **Given** `data/cs-curriculum.csv`, **When** el usuario pide el orden topológico, **Then** el sistema muestra los 19 vértices en un orden válido y termina con código 0.
3. **AS-103**: **Given** un grafo con varios órdenes válidos, **When** el usuario pide el orden dos veces, **Then** obtiene exactamente la misma salida. [NEEDS CLARIFICATION: ¿cuál de los órdenes válidos se muestra?]

### User Story 2 - Entender por qué no existe un orden (Priority: P2)

Como usuario con datos que tienen dependencias circulares, quiero que la herramienta me diga que no existe un orden y me dé información que me ayude a arreglar mis datos.

**Why this priority**: Los datos reales tienen errores (como `build-with-cycle.csv`); un mensaje útil ahorra tiempo de depuración.

**Independent Test**: Ejecutar el subcomando de orden sobre `data/build-with-cycle.csv` y verificar el mensaje y el código de salida.

**Acceptance Scenarios**:

1. **AS-104**: **Given** `data/build-with-cycle.csv`, **When** el usuario pide el orden topológico, **Then** el sistema informa en la salida de errores que no existe un orden y termina con un código distinto de 0. [NEEDS CLARIFICATION: ¿qué información sobre el ciclo se muestra y con qué código de salida?]

### User Story 3 - Mismas reglas de archivo que la Feature 1 (Priority: P3)

Como usuario, quiero que el subcomando de orden acepte y rechace exactamente los mismos archivos que `show`, con los mismos mensajes y códigos.

**Acceptance Scenarios**:

1. **AS-105**: **Given** un archivo inexistente o con formato inválido, **When** el usuario pide el orden topológico, **Then** el sistema se comporta igual que `show` (códigos 1 y 2 de la Feature 001).

### Edge Cases

- Vértices aislados (como `watch`): [NEEDS CLARIFICATION]
- Auto-lazos (como `metrics,metrics`): ¿cuentan como ciclo?
- Grafo vacío (solo encabezado).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-101**: El sistema DEBE proveer un subcomando para calcular el orden topológico de un grafo cargado desde un archivo con el mismo formato y reglas de la Feature 001.
- **FR-102**: El orden mostrado DEBE contener cada vértice del grafo exactamente una vez, y para cada arista `u -> v`, `u` DEBE aparecer antes que `v`.
- **FR-103**: La salida DEBE ser determinista.
- **FR-104**: Si no existe orden topológico, el sistema DEBE informarlo en la salida de errores con información útil para corregir los datos.
- **FR-105**: Los errores de lectura y formato DEBEN comportarse igual que en la Feature 001.

### Key Entities

- **Orden topológico**: secuencia de todos los vértices del grafo que respeta la dirección de cada arista.
- **Ciclo**: secuencia de aristas que vuelve al vértice de partida; impide que exista un orden topológico.

## Success Criteria *(mandatory)*

- **SC-101**: 100 % de los órdenes producidos son válidos según un verificador independiente.
- **SC-102**: El sistema reporta que no hay orden exactamente cuando el grafo tiene al menos un ciclo.
- **SC-103**: Un grafo de 10.000 aristas se ordena en menos de 1 segundo.

## Assumptions

- La carga del archivo reutiliza todas las reglas de la Feature 001 (encabezado, BOM, comillas, recorte, líneas en blanco, fail-fast).
