# Feature Specification: Directed Graphs

**Feature Branch**: `001-directed-graphs`

**Created**: 2026-10-30

**Status**: Clarified

**Input**: User description: "Feature 1 — Directed graphs: Users can load a directed, unweighted graph from a file and display it: its vertices and its edges."

## Clarifications

### Session 2026-11-03 (correcciones de /speckit-analyze)
- Q: Si hay líneas en blanco antes del encabezado, ¿qué número de línea se reporta cuando el encabezado es inválido? → A: El número de línea real donde está el encabezado (FR-002 y AS-009 decían "línea 1", lo que contradecía FR-011).
- Q: ¿Qué código de salida corresponde a un archivo que no es UTF-8 válido o a una ruta que es una carpeta? → A: Código 1 ("no puede leerse"), con el nombre del archivo en `stderr` (FR-010, AS-020).
- Q: ¿El caso "sin argumento de archivo" necesita escenario propio? → A: Sí, AS-019 (antes solo estaba en Edge Cases).

### Session 2026-11-02
- Q: ¿Cuál debe ser el nombre exacto del subcomando del CLI para visualizar el grafo? (FR-001) → A: El subcomando exacto es `show`.
- Q: ¿Cómo debe manejar el sistema las líneas en blanco o que contienen únicamente espacios en blanco en el archivo CSV? (FR-002) → A: Se ignoran silenciosamente sin generar vértices, aristas ni errores.
- Q: ¿Cómo debe procesar el sistema una fila con origen y destino vacíos que solo contiene la coma delimitadora (por ejemplo `,` o ` , `)? (FR-005) → A: Se rechaza como error de formato indicando el número de línea en `stderr` y finaliza con código de salida 2.
- Q: Ante una fila con formato inválido en el archivo CSV, ¿debe el sistema abortar inmediatamente toda la carga o debe omitir la fila y continuar procesando el resto del archivo? (FR-010) → A: Abortar inmediatamente toda la carga (fail-fast), emitir mensaje descriptivo con número de línea en `stderr` y terminar con código de salida 2 sin emitir salida en `stdout`.
- Q: ¿Cuál es la definición exacta del orden lexicográfico que debe aplicarse al listar vértices y aristas? (FR-006) → A: Orden ascendente basado en puntos de código Unicode estándar (donde mayúsculas preceden a minúsculas); y para aristas, ordenadas primariamente por origen y secundariamente por destino.
- Q: ¿Debe la validación del encabezado exigir coincidencia exacta en minúsculas (`source,target`) o admitir cualquier combinación de mayúsculas y minúsculas? (FR-002) → A: Coincidencia exacta estricta en minúsculas (`source,target`); cualquier variación en el uso de mayúsculas (por ejemplo `Source,Target` o `SOURCE,TARGET`) se rechaza como error de formato con código de salida 2.
- Q: ¿Debe el sistema aceptar archivos CSV codificados en UTF-8 con marca de orden de bytes (BOM) o únicamente UTF-8 estándar sin BOM? (FR-002) → A: Soportar UTF-8 tanto con BOM como sin BOM de forma transparente, removiendo silenciosamente el BOM inicial si está presente sin alterar el procesamiento.
- Q: ¿Debe el lector de CSV respetar el estándar de comillas dobles (RFC 4180) para admitir nombres de vértices que contengan comas? (FR-004) → A: Sí, se respetan las comillas estándar de CSV (RFC 4180), permitiendo comas en nombres de vértices entrecomillados y removiendo las comillas externas al registrar el identificador del vértice.

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
  Donde los vértices se listan en orden lexicográfico ascendente basado en puntos de código Unicode estándar (donde las mayúsculas preceden a las minúsculas), y las aristas se listan ordenadas primero por vértice de origen y luego por vértice de destino bajo el mismo criterio Unicode. En caso de grafo vacío, se muestra:
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

**Independent Test**: Se puede verificar ejecutando el subcomando `show` sobre un archivo válido como `data/small-dag.csv` y comprobando que se muestre el resumen correcto en la salida estándar con código de salida 0.

**Acceptance Scenarios**:

1. **AS-001**: **Given** el archivo de entrada válido `data/small-dag.csv` con encabezado `source,target`, **When** el usuario ejecuta el subcomando `show`, **Then** el sistema escribe en la salida estándar:
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
2. **AS-002**: **Given** el archivo de entrada válido `data/cs-curriculum.csv` cuyos nombres de vértices contienen espacios y caracteres alfanuméricos, **When** el usuario solicita visualizar el grafo, **Then** el sistema preserva los nombres completos de los vértices, reporta exactamente 19 vértices y 23 aristas, lista todas las relaciones dirigidas únicas en orden lexicográfico determinista en la salida estándar y finaliza con código de salida 0.
3. **AS-003**: **Given** el archivo de entrada `data/build-with-cycle.csv` que contiene ciclos dirigidos y auto-bucles, **When** el usuario solicita visualizar el grafo, **Then** el sistema carga y muestra fielmente el grafo reportando exactamente 11 vértices y 13 aristas dirigidas en la salida estándar sin bloquearse ni fallar, finalizando con código de salida 0.
4. **AS-014**: **Given** un archivo de entrada con vértices cuyos nombres combinan mayúsculas y minúsculas (por ejemplo `alpha` y `Beta`), **When** el usuario ejecuta el subcomando `show`, **Then** el sistema lista los vértices y aristas ordenados estrictamente por puntos de código Unicode estándar ascendente (donde `Beta` precede a `alpha`, y la arista `Beta -> alpha` precede a `alpha -> Beta`) con código de salida 0.

---

### User Story 2 - Soporte de datos atípicos y casos especiales (Priority: P2)

Como usuario con archivos de dependencias reales, quiero que la herramienta interprete adecuadamente situaciones comunes como vértices aislados (sin dependencias salientes), auto-bucles y aristas duplicadas, de modo que el modelo refleje la intención del conjunto de datos sin corromper la información.

**Why this priority**: Los datos del mundo real contienen peculiaridades legítimas; permitir vértices sin aristas salientes y deduplicar relaciones repetidas asegura interoperabilidad con fuentes de datos diversas.

**Independent Test**: Se puede comprobar procesando archivos con entradas atípicas (como `watch,` en `data/small-dag.csv` o aristas duplicadas en `data/cs-curriculum.csv`) y verificando el conjunto resultante de vértices y aristas.

**Acceptance Scenarios**:

1. **AS-004**: **Given** un archivo con una fila que define un origen pero el destino está vacío (como `watch,` en `data/small-dag.csv`), **When** el usuario visualiza el grafo, **Then** el sistema registra dicho origen como un vértice válido del grafo sin crear aristas hacia destinos vacíos.
2. **AS-005**: **Given** un archivo con aristas duplicadas entre los mismos dos vértices (como `Data Structures,Algorithms` repetido en `data/cs-curriculum.csv`), **When** el usuario visualiza el grafo, **Then** el sistema consolida la relación mostrando la arista dirigida exactamente una vez en la salida estándar.
3. **AS-006**: **Given** un archivo con un auto-bucle donde origen y destino son idénticos (como `metrics,metrics` en `data/build-with-cycle.csv`), **When** el usuario visualiza el grafo, **Then** el sistema muestra el vértice en la sección de vértices y la arista dirigida `metrics -> metrics` en la sección de aristas en la salida estándar.
4. **AS-011**: **Given** un archivo CSV válido que contiene líneas en blanco y líneas con únicamente espacios en blanco (intercaladas entre registros o al final del archivo), **When** el usuario ejecuta el subcomando `show`, **Then** el sistema omite silenciosamente dichas líneas sin generar vértices ni aristas adicionales y procesa el grafo correctamente con código de salida 0.
5. **AS-015**: **Given** un archivo de entrada válido que contiene espacios en blanco circundantes alrededor de los nombres de vértices o de las comas delimitadoras (por ejemplo ` undershorts , pants `), **When** el usuario ejecuta el subcomando `show`, **Then** el sistema recorta los espacios en blanco iniciales y finales de cada vértice procesándolos como `undershorts` y `pants`, visualizando el grafo correctamente sin espacios espurios y finalizando con código de salida 0.
6. **AS-016**: **Given** un archivo de entrada válido que contiene vértices cuyos identificadores difieren únicamente en el uso de mayúsculas y minúsculas (por ejemplo `Math,math`), **When** el usuario ejecuta el subcomando `show`, **Then** el sistema reconoce y lista a `Math` y `math` como dos vértices distintos y la arista dirigida `Math -> math` en la salida estándar con código de salida 0.
7. **AS-017**: **Given** un archivo CSV válido codificado en UTF-8 con marca de orden de bytes inicial (BOM `\ufeff`), **When** el usuario ejecuta el subcomando `show`, **Then** el sistema procesa el archivo de manera transparente removiendo el BOM sin alterar la validación del encabezado `source,target` y visualiza el grafo correctamente con código de salida 0.
8. **AS-018**: **Given** un archivo CSV válido que contiene nombres de vértices con comas delimitadoras encerrados entre comillas dobles (por ejemplo `"Algorithms, Part I",Compilers`), **When** el usuario ejecuta el subcomando `show`, **Then** el sistema preserva el nombre completo del vértice sin comillas externas (`Algorithms, Part I`), reconoce la arista dirigida `Algorithms, Part I -> Compilers` y muestra el grafo correctamente en la salida estándar con código de salida 0.

---

### User Story 3 - Manejo robusto de errores de entrada y argumentos (Priority: P3)

Como usuario, quiero recibir mensajes descriptivos en caso de suministrar un archivo inexistente, un archivo vacío, un encabezado incorrecto o filas malformadas, para corregir rápidamente mi archivo o comando sin ver volcados internos de error del sistema.

**Why this priority**: La robustez ante entradas inválidas garantiza que la herramienta sea segura, predecible y cumpla con las normas de usabilidad y gobernanza del proyecto.

**Independent Test**: Se puede verificar ejecutando el comando apuntando a un archivo que no existe o a un archivo corrupto, confirmando que la salida se dirija a la salida de errores con un mensaje claro y un código de salida distinto de 0.

**Acceptance Scenarios**:

1. **AS-007**: **Given** un nombre o ubicación de archivo que no existe en el sistema de archivos, **When** el usuario ejecuta el comando de visualización, **Then** el sistema escribe un mensaje de error explicativo en la salida de errores especificando el nombre del archivo no encontrado y termina con código de salida 1.
2. **AS-008**: **Given** un archivo de entrada completamente vacío (0 bytes), **When** el usuario ejecuta el comando, **Then** el sistema escribe en la salida de errores que el archivo carece del encabezado requerido `source,target` indicando la línea 1 y termina con código de salida 2.
3. **AS-009**: **Given** un archivo cuyo primer registro no corresponde exactamente en minúsculas al encabezado `source,target` (por ejemplo con nombres de columna distintos o con variaciones de mayúsculas como `Source,Target`), **When** el usuario ejecuta el subcomando `show`, **Then** el sistema escribe un mensaje de error en la salida de errores indicando que el encabezado es inválido y el número de línea donde se encontró (la línea 1 si no hay líneas en blanco antes del encabezado) y termina con código de salida 2.
4. **AS-010**: **Given** un archivo con una fila con un número de columnas diferente a dos (por ejemplo tres columnas o una sola sin coma), **When** el usuario ejecuta el comando, **Then** el sistema escribe un mensaje de error en la salida de errores indicando el número de línea que contiene el formato inválido y termina con código de salida 2.
5. **AS-012**: **Given** un archivo con una fila que solo contiene la coma delimitadora o espacios alrededor de ella (por ejemplo `,` o ` , `), **When** el usuario ejecuta el subcomando `show`, **Then** el sistema escribe un mensaje de error en la salida de errores indicando el número de línea que contiene el formato inválido y termina con código de salida 2.
6. **AS-013**: **Given** un archivo que contiene filas válidas y una fila con formato inválido en una línea intermedia, **When** el usuario ejecuta el subcomando `show`, **Then** el sistema aborta de inmediato la carga ante la primera fila inválida ("fail-fast"), escribe el mensaje de error con el número de línea en la salida de errores, no emite ningún grafo parcial en la salida estándar y finaliza con código de salida 2.
7. **AS-019**: **Given** que el usuario ejecuta el subcomando `show` sin indicar la ruta del archivo, **When** se procesa la invocación, **Then** el sistema escribe un mensaje de uso en la salida de errores, no escribe nada en la salida estándar, no muestra ningún traceback y termina con código de salida 2.
8. **AS-020**: **Given** un archivo cuyo contenido no es UTF-8 válido (por ejemplo codificado en Latin-1 con caracteres acentuados), **When** el usuario ejecuta el subcomando `show`, **Then** el sistema escribe en la salida de errores que el archivo no puede leerse como UTF-8, indicando el nombre del archivo, y termina con código de salida 1.

---

### Edge Cases

- ¿Qué sucede con las líneas en blanco o con solo espacios? El sistema las ignora silenciosamente (ya sea antes del encabezado, entre registros o al final del archivo) sin interrumpir el procesamiento ni generar vértices o aristas espurias.
- ¿Qué sucede con una fila que solo contiene comas o espacios alrededor de la coma (ej. `,` o ` , `)? Se rechaza como error de formato indicando el número de línea en la salida de errores y finaliza con código de salida 2.
- ¿Qué sucede si un archivo contiene filas válidas y una fila inválida en medio? El sistema aplica fail-fast: aborta inmediatamente en la primera fila inválida encontrada, reporta el error con número de línea en stderr sin emitir ninguna salida en stdout, y termina con código de salida 2.
- ¿Qué sucede con el ordenamiento lexicográfico entre mayúsculas y minúsculas? El orden lexicográfico se define estrictamente por el orden ascendente de los puntos de código Unicode estándar (donde las letras mayúsculas preceden a las minúsculas).
- ¿Qué sucede si el archivo solo contiene la fila de encabezado `source,target` sin registros de datos? Se procesa exitosamente como un grafo vacío (0 vértices, 0 aristas) y código de salida 0.
- ¿Qué sucede si se ejecuta el comando sin especificar el argumento del archivo? Se escribe un mensaje de uso y error en la salida de errores y se finaliza con código de salida 2.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE proveer el subcomando `show` para la visualización de grafos, el cual recibe como argumento la ruta a un archivo de datos en formato CSV (ejecutable mediante `python -m graphcli show <archivo>`).
- **FR-002**: El sistema DEBE validar que la primera línea no vacía del archivo de entrada corresponda exactamente al encabezado en minúsculas `source,target` (ignorando espacios en blanco circundantes). Cualquier variación en el uso de mayúsculas y minúsculas (por ejemplo `Source,Target` o `SOURCE,TARGET`) DEBE ser rechazada como error de formato indicando el número de línea real del encabezado en la salida de errores (`stderr`) con código de salida 2. Asimismo, el sistema DEBE soportar codificación UTF-8 tanto con marca de orden de bytes (BOM inicial `\ufeff`) como sin ella, descartando transparentemente el BOM si está presente sin considerarlo parte del encabezado.
- **FR-003**: El sistema DEBE construir un grafo dirigido no ponderado identificando los vértices y las aristas dirigidas desde el origen (`source`) hacia el destino (`target`).
- **FR-004**: El sistema DEBE considerar como vértice cualquier identificador no vacío que aparezca en la columna `source` o en la columna `target`.
- **FR-005**: El sistema DEBE procesar filas con origen no vacío y destino vacío (por ejemplo `watch,`) registrando el origen como un vértice válido sin aristas dirigidas salientes. Filas con origen vacío (incluyendo filas con destino presente como `,target` y filas con origen y destino vacíos como `,` o ` , `) DEBEN ser rechazadas como error de formato indicando el número de línea en la salida de errores (`stderr`) con código de salida 2.
- **FR-006**: El sistema DEBE emitir la representación del grafo en la salida estándar (`stdout`) en un formato determinista compuesto por: cabecera `Vertices (<N>):` seguida de los vértices indentados por dos espacios en orden lexicográfico ascendente según sus puntos de código Unicode estándar (las mayúsculas preceden a las minúsculas), y cabecera `Edges (<M>):` seguida de las aristas en formato `  <source> -> <target>` ordenadas primariamente por vértice de origen y secundariamente por vértice de destino bajo el mismo criterio de puntos de código Unicode.
- **FR-007**: El sistema DEBE deduplicar silenciosamente aristas dirigidas repetidas en el archivo de entrada, contabilizando y mostrando cada arista única una sola vez.
- **FR-008**: Toda salida de resultados exitosos DEBE enviarse exclusivamente a la salida estándar (`stdout`).
- **FR-009**: Todos los mensajes de advertencia, uso o error DEBEN enviarse exclusivamente a la salida de errores (`stderr`), indicando archivo y línea cuando aplique, sin mostrar nunca volcados internos de excepción al usuario.
- **FR-010**: El sistema DEBE retornar código de salida `0` cuando la ejecución sea exitosa, código `1` cuando el archivo no exista o no pueda leerse (incluye: la ruta es una carpeta, falta de permisos, o contenido que no es UTF-8 válido), y código `2` ante errores de formato o sintaxis en los argumentos o datos.
- **FR-011**: El sistema DEBE ignorar silenciosamente cualquier línea en blanco o compuesta únicamente por espacios en blanco en el archivo CSV, sin crear vértices ni aristas ni considerarla un error de formato.
- **FR-012**: El sistema DEBE operar bajo el principio de detención inmediata ("fail-fast"): ante la primera fila con formato o sintaxis inválida en el archivo de datos, DEBE abortar inmediatamente la carga, escribir el mensaje de error especificando el número de línea en la salida de errores (`stderr`), abstenerse de emitir cualquier salida en `stdout` y finalizar con código de salida 2.
- **FR-013**: El sistema DEBE recortar los espacios en blanco iniciales y finales (strip/trim) de cada nombre de vértice extraído de las columnas `source` y `target` antes de incorporarlo al grafo o evaluarlo.
- **FR-014**: El sistema DEBE tratar los nombres de vértices distinguiendo estrictamente entre mayúsculas y minúsculas (case-sensitive), considerando identificadores que difieran en la capitalización (por ejemplo `Math` y `math`) como vértices totalmente distintos e independientes.
- **FR-015**: El sistema DEBE procesar archivos CSV respetando el formato de comillas dobles estándar (RFC 4180), permitiendo que los nombres de vértices contengan comas delimitadoras si se encuentran debidamente entrecomillados (por ejemplo `"Algorithms, Part I"`), y removiendo las comillas externas al registrar el identificador del vértice.

### Key Entities *(include if feature involves data)*

- **Grafo Dirigido**: Colección finita de vértices y aristas dirigidas que representan relaciones de dependencia unilaterales entre pares de elementos.
- **Vértice**: Identificador textual único que representa una entidad o elemento dentro del grafo (por ejemplo, una prenda de vestir, una materia académica o un componente de software).
- **Arista Dirigida**: Relación orientada que conecta un vértice origen con un vértice destino, indicando que el origen precede o se relaciona con el destino.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Los usuarios pueden visualizar cualquier grafo de dependencias de hasta 10,000 aristas en menos de 1 segundo de tiempo de ejecución.
- **SC-002**: El 100% de las ejecuciones sobre el mismo archivo de entrada producen idéntica salida byte a byte (determinismo absoluto).
- **SC-003**: El 100% de los escenarios de aceptación automatizados (`AS-001` a `AS-020`) son verificables mediante pruebas independientes.
- **SC-004**: Cero volcados internos o trazas de excepción no controladas son expuestas a los usuarios en cualquier escenario de error.

## Assumptions

- Los archivos de entrada están codificados en UTF-8 (con o sin marca de orden de bytes BOM).
- Los nombres de vértices no contienen caracteres de salto de línea.
- La herramienta se ejecuta en entornos de terminal de texto estándar capaces de recibir argumentos y mostrar texto en salidas de consola estándar y de error.
