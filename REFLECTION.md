# REFLECTION — Spec-Driven Development Lab 2: Graphs and Topological Sorting

Apuntes de detalle en [`notas/`](notas/).

## 1. Agente usado

Usamos **dos agentes**, y conviene decirlo tal cual:

- **Antigravity CLI (`agy`)**, integración de Spec Kit `--integration agy`, para el init, la constitución y las fases specify, clarify, plan y tasks de la Feature 001. Los comandos son skills con guion (`/speckit-specify`, …).
- **Claude (Cowork, modelo Claude Opus)** para todo lo demás: analyze e implement de la 001 y la Feature 002 completa. Durante la primera corrida de `/speckit-analyze` de la 001, Antigravity respondió *"Individual quota reached… Resets in 95h"* y no se podía esperar cuatro días. Los commits de esa parte salen con el autor "Claude (asistente)".

**Qué ayudó:** Antigravity generó documentos muy completos (`research.md` con las alternativas rechazadas y un plan con Constitution Check) y siguió bien las instrucciones cuando le dimos una lista concreta de puntos para clarify. **Qué estorbó:** su cuota se acabó a mitad del proceso. También tendía a declarar el trabajo terminado antes de tiempo: en specify marcó la spec como *"Ready for Planning"* sin pasar por clarify, y tras el analyze intentó un commit cuando no había nada que commitear.

## 2. Preguntas de clarify y decisiones

**Feature 001** (detalle en `notas/clarify-001.md`):

- subcomando `show`;
- líneas en blanco: se ignoran;
- fila `,`: error de formato, código 2;
- fila inválida: se aborta toda la carga (fail-fast);
- orden: por código Unicode, sensible a mayúsculas;
- encabezado: exacto `source,target` en minúsculas;
- UTF-8 con BOM: se acepta;
- comillas: RFC 4180;
- espacios alrededor de los nombres: se recortan;
- `Math` y `math`: son vértices distintos.

En analyze se agregó: archivo no UTF-8 o carpeta → código 1, y el número de línea real del encabezado.

**Feature 002** (detalle en `notas/clarify-002.md`):

- subcomando `order`, un vértice por línea;
- desempate: siempre el menor orden lexicográfico;
- con ciclos: código 3 y un ciclo por cada grupo de dependencia circular en stderr;
- auto-lazo: es un ciclo;
- vértices aislados: se incluyen;
- grafo vacío: salida vacía.

**La más difícil:** *¿qué se muestra cuando hay ciclos?* `build-with-cycle.csv` tiene dos problemas (`auth → session → user-profile → auth` y `metrics → metrics`), y además dos vértices (`api`, `web`) que no están en ningún ciclo pero tampoco se pueden ordenar. Las tres opciones tenían problemas:

- mostrar "hay un ciclo" no ayuda;
- mostrar los vértices que Kahn no procesó incluye a `api` y `web`, que no son la causa;
- mostrar todos los ciclos simples puede ser exponencial.

Elegimos **un ciclo por cada grupo de vértices mutuamente alcanzables**. Es finito, es determinista (empieza en el vértice menor y es el más corto) y le dice al usuario exactamente qué romper.

En la 001 la decisión discutible fue el encabezado estricto: rechazar `Source,Target`, aunque nuestra lista recomendaba aceptarlo.

## 3. Rarezas en los datos

| Dato | Feature 001 (`show`) | Feature 002 (`order`) |
|------|----------------------|------------------------|
| `watch,` en `small-dag.csv` (destino vacío) | Vértice aislado (9 vértices, 9 aristas) | Aparece en el orden (al final por desempate) |
| `Data Structures,Algorithms` repetida en `cs-curriculum.csv` | Se deduplica en silencio (19 vértices, 23 aristas) | No afecta |
| `metrics,metrics` (auto-lazo) | Se muestra como arista | Ciclo de longitud 1, código 3 |
| `auth → session → user-profile → auth` | Se muestra normal (11 vértices, 13 aristas) | Ciclo reportado, código 3 |
| Nombres con espacios (`Calculus I`) | Se conservan completos | Igual |

Verificamos también que **no** había espacios extra, tabs, CRLF, BOM ni caracteres no ASCII, y aun así la spec define qué pasa con cada uno.

## 4. Representación del grafo

**Lista de adyacencia** `dict[str, set[str]]` más un **conjunto de vértices** (para los aislados). El `set` deduplica aristas en O(1).

Alternativas rechazadas:

- **Matriz de adyacencia:** O(V²) de memoria en grafos dispersos, y encontrar los sucesores cuesta O(V).
- **Lista de aristas:** encontrar sucesores o duplicados cuesta O(E), y deduplicar al cargar sería O(E²).

**¿Aguantó la Feature 2?** La estructura sí. Solo `in_degree(v)` resultó insuficiente: recorre todo el grafo, así que llamarlo por cada vértice en Kahn costaría O(V·(V+E)). Se agregó `in_degrees()` en O(V+E). Fue un cambio de código, no de spec, y `show` no cambió. Para la Feature 3 opcional (pesos), cambiar `set[str]` por `dict[str, float]` bastaría sin reescribir 001 ni 002.

## 5. Lo que reportó `/speckit-analyze`

**001** (`notas/analyze-001.md`):

- **HIGH:** FR-002/AS-009 decían "línea 1" para el encabezado inválido, en contradicción con FR-011 (permite líneas en blanco antes del encabezado). Se cambió a "línea real".
- **HIGH:** no estaba definido qué pasa con un archivo no UTF-8 o una carpeta; habría salido un traceback. Ahora es código 1 (FR-010, AS-020).
- **MEDIUM:** el caso "sin argumento" no tenía ID de escenario (se creó AS-019); SC-001 no tenía tarea (se agregó la prueba de rendimiento); `<paquete>` → `graphcli`.
- **LOW:** enlaces absolutos `file:///C:/...` en el plan.

**002** (`notas/analyze-002.md`):

- **MEDIUM:** no estaba definido el desempate entre dos ciclos igual de cortos; se definió y se agregó una prueba.
- **MEDIUM:** cómo se escribe la ruta en el mensaje de ciclos; queda tal como la escribió el usuario.

## 6. Cuando el agente hizo algo distinto a lo que queríamos

En la fase specify de la 001, Antigravity escribió su propia sección "Clarifications" con 3 preguntas, la marcó como resuelta y puso `Status: Ready for Planning`. Es decir, se saltó la fase clarify. Además dejó dos decisiones (recortar espacios y distinguir mayúsculas) solo en *Edge Cases*, sin requisito ni escenario. **La spec no era ambigua; el agente la ignoró:** la constitución exige un escenario con prueba por cada comportamiento, y el flujo exige clarify antes del plan. Lo corregimos corriendo `/speckit-clarify` dos veces con una lista propia de preguntas, lo que subió los escenarios de 10 a 18.

Un segundo caso, ya con Claude: la primera versión de una prueba con grafos aleatorios pedía más aristas de las posibles cuando había pocos vértices, y la suite se colgó. El bug estaba en la prueba, no en la spec ni en el código; se corrigió el generador.
