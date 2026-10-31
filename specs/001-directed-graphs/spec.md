# Feature Specification: Directed Graphs

**Feature Branch**: `001-directed-graphs`

**Created**: 2026-10-30

**Status**: Ready for Planning

**Input**: User description: "Feature 1 — Directed graphs: Users can load a directed, unweighted graph from a file and display it: its vertices and its edges."

## Clarifications

### Clarification 1: Formato exacto de visualización en salida estándar
- **Pregunta**: ¿Cuál es el formato exacto de salida en `stdout` al visualizar un grafo?
- **Decisión**: Formato estructurado con conteos y listados indentados ordenados lexicográficamente:
  ```text
  Vertices (<N>):
    <vertice_1>
    <vertice_2>
  Edges (<M>):
    <origen_1> -> <destino_1>
    <origen_2> -> <destino_2>
  ```
  Donde los vértices se listan en orden lexicográfico ascendente, y las aristas se listan ordenadas lexicográficamente primero por vértice de origen y luego por vértice de destino. En caso de grafo vacío, se muestra:
  ```text
  Vertices (0):
  Edges (0):
  ```

### Clarification 2: Manejo de filas con origen y destino vacío (`source,`)
- **Pregunta**: ¿Cómo debe interpretar el sistema una fila con origen definido pero columna de destino vacía (como `watch,` en `data/small-dag.csv`)?
- **Decisión**: Vértice aislado válido. Se registra el identificador de origen como un vértice del grafo sin generar aristas salientes. Las filas con destino presente pero origen vacío (ej. `,target`) o con comas adicionales se rechazan como error de formato.

### Clarification 3: Tratamiento de aristas duplicadas en el archivo de entrada
- **Pregunta**: ¿Cómo deben manejarse las aristas duplicadas en el archivo (como `Data Structures,Algorithms` en `data/cs-curriculum.csv`)?
- **Decisión**: Deduplicación silenciosa. El grafo representa un conjunto matemático de vértices y aristas únicas. Las apariciones repetidas de la misma relación dirigida se consolidan en una única arista en el modelo y en la salida, sin emitir mensajes de advertencia.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Carga y visualización de grafos dirigidos válidos (Priority: P1)

Como usuario de la herramienta de línea de comandos, quiero cargar un archivo en formato de valores separados por coma (CSV) que describe dependencias dirigidas y visualizar en pantalla un resumen claro con sus vértices y sus aristas dirigidas, para inspeccionar la estructura de relaciones de mi proyecto o plan.

**Why this priority**: Es la funcionalidad central (MVP) de la herramienta. Sin la capacidad de cargar y mostrar el grafo, ninguna otra operación tiene utilidad.

**Independent Test**: Se puede verificar ejecutando el comando de visualización sobre un archivo válido como `data/small-dag.csv` y comprobando que se muestre el resumen correcto en la salida estándar con código de salida 0.

**Acceptance Scenarios**:

1. **AS-001**: **Given** el archivo de entrada válido `data/small-dag.csv` con encabezado `source,target`, **When** el usuario solicita visualizar el grafo, **Then** el sistema escribe en la salida estándar:
   ```text
   Vertices (9):
     belt
     jacket
     pants
     shirt
     shoes
     socks
     tie
     undershorts
     watch
   Edges (9):
     belt -> jacket
     pants -> belt
     pants -> shoes
     shirt -> belt
     shirt -> tie
     socks -> shoes
     tie -> jacket
     undershorts -> pants
     undershorts -> shoes
   ```
   y finaliza con código de salida 0.
2. **AS-002**: **Given** el archivo de entrada válido `data/cs-curriculum.csv` cuyos nombres de vértices contienen espacios y caracteres alfanuméricos, **When** el usuario solicita visualizar el grafo, **Then** el sistema preserva los nombres completos de los vértices, lista todas las relaciones dirigidas únicas en orden lexicográfico determinista en la salida estándar y finaliza con código de salida 0.
3. **AS-003**: **Given** el archivo de entrada `data/build-with-cycle.csv` que contiene ciclos dirigidos y auto-bucles, **When** el usuario solicita visualizar el grafo, **Then** el sistema carga y muestra fielmente todos los vértices y aristas dirigidas en la salida estándar sin bloquearse ni fallar, finalizando con código de salida 0.

---

### User Story 2 - Soporte de datos atípicos y casos especiales (Priority: P2)

Como usuario con archivos de dependencias reales, quiero que la herramienta interprete adecuadamente situaciones comunes como vértices aislados (sin dependencias salientes), auto-bucles y aristas duplicadas, de modo que el modelo refleje la intención del conjunto de datos sin corromper la información.

**Why this priority**: Los datos del mundo real contienen peculiaridades legítimas; permitir vértices sin aristas salientes y deduplicar relaciones repetidas asegura interoperabilidad con fuentes de datos diversas.

**Independent Test**: Se puede comprobar procesando archivos con entradas atípicas (como `watch,` en `data/small-dag.csv` o aristas duplicadas en `data/cs-curriculum.csv`) y verificando el conjunto resultante de vértices y aristas.

**Acceptance Scenarios**:

1. **AS-004**: **Given** un archivo con una fila que define un origen pero el destino está vacío (como `watch,` en `data/small-dag.csv`), **When** el usuario visualiza el grafo, **Then** el sistema registra dicho origen como un vértice válido del grafo sin crear aristas hacia destinos vacíos.
2. **AS-005**: **Given** un archivo con aristas duplicadas entre los mismos dos vértices (como `Data Structures,Algorithms` repetido en `data/cs-curriculum.csv`), **When** el usuario visualiza el grafo, **Then** el sistema consolida la relación mostrando la arista dirigida exactamente una vez en la salida estándar.
3. **AS-006**: **Given** un archivo con un auto-bucle donde origen y destino son idénticos (como `metrics,metrics` en `data/build-with-cycle.csv`), **When** el usuario visualiza el grafo, **Then** el sistema muestra el vértice en la sección de vértices y la arista dirigida `metrics -> metrics` en la sección de aristas en la salida estándar.

---

### User Story 3 - Manejo robusto de errores de entrada y argumentos (Priority: P3)

Como usuario, quiero recibir mensajes descriptivos en caso de suministrar un archivo inexistente, un archivo vacío, un encabezado incorrecto o filas malformadas, para corregir rápidamente mi archivo o comando sin ver volcados internos de error del sistema.

**Why this priority**: La robustez ante entradas inválidas garantiza que la herramienta sea segura, predecible y cumpla con las normas de usabilidad y gobernanza del proyecto.

**Independent Test**: Se puede verificar ejecutando el comando apuntando a un archivo que no existe o a un archivo corrupto, confirmando que la salida se dirija a la salida de errores con un mensaje claro y un código de salida distinto de 0.

**Acceptance Scenarios**:

1. **AS-007**: **Given** un nombre o ubicación de archivo que no existe en el sistema de archivos, **When** el usuario ejecuta el comando de visualización, **Then** el sistema escribe un mensaje de error explicativo en la salida de errores especificando el nombre del archivo no encontrado y termina con código de salida 1.
2. **AS-008**: **Given** un archivo de entrada completamente vacío (0 bytes), **When** el usuario ejecuta el comando, **Then** el sistema escribe en la salida de errores que el archivo carece del encabezado requerido `source,target` indicando la línea 1 y termina con código de salida 2.
3. **AS-009**: **Given** un archivo cuyo primer registro no corresponde al encabezado `source,target`, **When** el usuario ejecuta el comando, **Then** el sistema escribe un mensaje de error en la salida de errores indicando que el encabezado es inválido en la línea 1 y termina con código de salida 2.
4. **AS-010**: **Given** un archivo con una fila con un número de columnas diferente a dos (por ejemplo tres columnas o una sola sin coma), **When** el usuario ejecuta el comando, **Then** el sistema escribe un mensaje de error en la salida de errores indicando el número de línea que contiene el formato inválido y termina con código de salida 2.

---

### Edge Cases

- ¿Qué sucede cuando una fila contiene espacios en blanco alrededor de las comas o nombres (por ejemplo ` undershorts , pants `)? El sistema recorta los espacios en blanco iniciales y finales de cada nombre de vértice antes de procesarlo.
- ¿Qué sucede con la distinción entre mayúsculas y minúsculas? Los nombres de vértices son sensibles a mayúsculas y minúsculas (por ejemplo, `Math` y `math` se consideran vértices distintos).
- ¿Qué sucede si el archivo solo contiene la fila de encabezado `source,target` sin registros de datos? Se procesa exitosamente como un grafo vacío (0 vértices, 0 aristas) y código de salida 0.
- ¿Qué sucede si se ejecuta el comando sin especificar el argumento del archivo? Se escribe un mensaje de uso y error en la salida de errores y se finaliza con código de salida 2.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE proveer un subcomando de visualización de grafos que reciba como argumento la ruta a un archivo de datos en formato CSV.
- **FR-002**: El sistema DEBE validar que la primera línea del archivo de entrada corresponda exactamente al encabezado `source,target` (ignorando espacios en blanco circundantes).
- **FR-003**: El sistema DEBE construir un grafo dirigido no ponderado identificando los vértices y las aristas dirigidas desde el origen (`source`) hacia el destino (`target`).
- **FR-004**: El sistema DEBE considerar como vértice cualquier identificador no vacío que aparezca en la columna `source` o en la columna `target`.
- **FR-005**: El sistema DEBE procesar filas con origen no vacío y destino vacío (por ejemplo `watch,`) registrando el origen como un vértice válido sin aristas dirigidas salientes. Filas con origen vacío y destino presente DEBEN ser rechazadas como error de formato con código de salida 2.
- **FR-006**: El sistema DEBE emitir la representación del grafo en la salida estándar (`stdout`) en un formato determinista compuesto por: cabecera `Vertices (<N>):` seguida de los vértices indentados por dos espacios en orden lexicográfico ascendente, y cabecera `Edges (<M>):` seguida de las aristas en formato `  <source> -> <target>` en orden lexicográfico ascendente.
- **FR-007**: El sistema DEBE deduplicar silenciosamente aristas dirigidas repetidas en el archivo de entrada, contabilizando y mostrando cada arista única una sola vez.
- **FR-008**: Toda salida de resultados exitosos DEBE enviarse exclusivamente a la salida estándar (`stdout`).
- **FR-009**: Todos los mensajes de advertencia, uso o error DEBEN enviarse exclusivamente a la salida de errores (`stderr`), indicando archivo y línea cuando aplique, sin mostrar nunca volcados internos de excepción al usuario.
- **FR-010**: El sistema DEBE retornar código de salida `0` cuando la ejecución sea exitosa, código `1` cuando el archivo no exista o no pueda leerse, y código `2` ante errores de formato o sintaxis en los argumentos o datos.

### Key Entities *(include if feature involves data)*

- **Grafo Dirigido**: Colección finita de vértices y aristas dirigidas que representan relaciones de dependencia unilaterales entre pares de elementos.
- **Vértice**: Identificador textual único que representa una entidad o elemento dentro del grafo (por ejemplo, una prenda de vestir, una materia académica o un componente de software).
- **Arista Dirigida**: Relación orientada que conecta un vértice origen con un vértice destino, indicando que el origen precede o se relaciona con el destino.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Los usuarios pueden visualizar cualquier grafo de dependencias de hasta 10,000 aristas en menos de 1 segundo de tiempo de ejecución.
- **SC-002**: El 100% de las ejecuciones sobre el mismo archivo de entrada producen idéntica salida byte a byte (determinismo absoluto).
- **SC-003**: El 100% de los escenarios de aceptación automatizados (`AS-001` a `AS-010`) son verificables mediante pruebas independientes.
- **SC-004**: Cero volcados internos o trazas de excepción no controladas son expuestas a los usuarios en cualquier escenario de error.

## Assumptions

- Los archivos de entrada están codificados en UTF-8 estándar.
- Los nombres de vértices no contienen caracteres de salto de línea.
- La herramienta se ejecuta en entornos de terminal de texto estándar capaces de recibir argumentos y mostrar texto en salidas de consola estándar y de error.
