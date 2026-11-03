# Phase 0 Research: Directed Graphs

**Feature**: Directed Graphs (`001-directed-graphs`)  
**Status**: Completed  
**Date**: 2026-11-02  

---

## 1. Representación del grafo en memoria

### Decisión
Representar el grafo dirigido no ponderado utilizando una **lista de adyacencia** basada en un diccionario de vértices a conjuntos de sucesores (`dict[str, set[str]]`), complementado con un conjunto explícito de vértices (`set[str]`).

```python
class DirectedGraph:
    vertices: set[str]           # Todos los vértices (incluyendo aislados)
    _adj: dict[str, set[str]]    # Mapeo de source -> set de targets
```

### Justificación
1. **Eficiencia en espacio**: Ocupa memoria proporcional a $O(V + E)$ (donde $V$ es el número de vértices y $E$ el de aristas únicas). Para los grafos del dominio del problema (planes de estudio, dependencias de paquetes, grafos de tareas), el grado promedio de cada vértice es relativamente bajo ($E \ll V^2$), por lo que una estructura dispersa es óptima.
2. **Soporte nativo de vértices aislados**: Mantener un conjunto de vértices separado de las aristas permite registrar y preservar vértices que no tienen aristas salientes ni entrantes (por ejemplo filas con `watch,`), cumpliendo con FR-004 y FR-005.
3. **Deduplicación silenciosa en tiempo constante**: El uso de `set[str]` para los sucesores de cada vértice permite insertar aristas en tiempo promedio $O(1)$ y garantiza la deduplicación automática de aristas repetidas exigida en FR-007.
4. **Preparación sin fricción para Feature 2**:
   - Para el cálculo de grados de entrada (in-degree): se puede calcular fácilmente iterando sobre las listas de adyacencia en $O(V + E)$ o manteniendo un contador auxiliar.
   - Para el algoritmo de Kahn o DFS (orden topológico en Feature 2): la consulta de sucesores inmediatos se ejecuta en $O(1)$ por búsqueda de clave y $O(\text{deg}^+(u))$ por iteración sobre el conjunto.
   - No se implementa ninguna lógica de ordenamiento topológico en esta feature, respetando el Principio VII (Simplicidad).

### Alternativas rechazadas y por qué

1. **Matriz de adyacencia ($V \times V$)**:
   - *Por qué se evaluó*: Es una representación clásica que permite verificar la existencia de aristas en $O(1)$ indexado.
   - *Por qué fue rechazada*: Requiere $O(V^2)$ de memoria fija independientemente del número de aristas. En grafos con miles de vértices y pocas dependencias, desperdicia una enorme cantidad de memoria en ceros/falsos. Además, encontrar los sucesores de un vértice requiere escanear toda la fila en $O(V)$, en contraste con $O(\text{deg}^+(u))$ en la lista de adyacencia.

2. **Lista plana de aristas (`list[tuple[str, str]]`)**:
   - *Por qué se evaluó*: Es la representación más elemental y directa de leer desde un archivo CSV.
   - *Por qué fue rechazada*: Consultar los sucesores de un vértice o verificar si una arista ya existe cuesta $O(E)$, ya que requiere un escaneo lineal completo de la lista. Con $E = 10,000$ aristas y deduplicación en cada inserción, la construcción del grafo se degradaría a $O(E^2)$, violando el criterio de rendimiento SC-001 (< 1 segundo para 10,000 aristas). Asimismo, el cálculo de in-degrees para la Feature 2 requeriría $O(V \cdot E)$.

---

## 2. Lectura y parsing de archivos CSV

### Decisión
Utilizar el módulo estándar `csv.reader` de Python configurado para procesar archivos con decodificación `utf-8-sig` (o apertura en UTF-8 con remoción previa del carácter BOM `\ufeff`).

### Justificación
1. **Conformidad con RFC 4180**: El módulo `csv` de la biblioteca estándar de Python maneja de forma robusta las comillas dobles, comas internas en identificadores de vértices (como `"Algorithms, Part I"`), espacios y saltos de línea sin dependencias externas (Principio I).
2. **Soporte transparente de UTF-8 con y sin BOM**: Al abrir con codificación `utf-8-sig`, Python decodifica UTF-8 estándar de forma transparente y elimina automáticamente el encabezado BOM de 3 bytes (`\xef\xbb\xbf`) si está presente, garantizando que el encabezado comience exactamente con los caracteres `source,target` sin corromper la primera columna.
3. **Detección de errores y número de línea**: `csv.reader` o la lectura línea a línea permite llevar el contador exacto del número de línea en el archivo original para cumplir con la emisión de mensajes descriptivos en `stderr` (`FR-009`) y la política de detención inmediata fail-fast (`FR-012`).

### Alternativas rechazadas y por qué
1. **División manual mediante `str.split(',')`**:
   - *Por qué se evaluó*: Es simple e intuitivo para archivos CSV básicos.
   - *Por qué fue rechazada*: Falla completamente ante nombres de vértices que contienen comas legítimas entre comillas dobles (por ejemplo `"Algorithms, Part I",Compilers`), violando FR-015 y la clarificación aceptada.
2. **Expresiones regulares (`re`) para analizar CSV**:
   - *Por qué se evaluó*: Permite parsear campos con patrones complejos.
   - *Por qué fue rechazada*: Mayor propensión a errores de casos borde, menor rendimiento que el parser en C de la biblioteca estándar `csv`, y añade complejidad innecesaria violando el Principio VII.

---

## 3. Interfaz de línea de comandos (CLI)

### Decisión
Implementar el CLI en el paquete `graphcli` utilizando el módulo estándar `argparse`, estructurado con subcomandos para admitir `python -m graphcli show <archivo>`.

### Justificación
1. **Estándar y extensible**: `argparse` es parte de la biblioteca estándar de Python 3.11+. La utilización de `subparsers` permite implementar `show` de forma limpia y deja la estructura lista para futuros subcomandos (como el de orden topológico en Feature 2) sin alterar la arquitectura.
2. **Control estricto de códigos de salida**: Sobrescribir o manejar los errores de argumentos de `argparse` permite canalizar todos los mensajes de error a `stderr` con código de salida `2` (FR-010) y evitar que se emitan tracebacks o mensajes genéricos no controlados (Principio V).
3. **Punto de entrada canónico**: Crear `graphcli/__main__.py` permite la ejecución directa `python -m graphcli show <archivo>`, tal como exige la Constitución (Principio I).

### Alternativas rechazadas y por qué
1. **Parsing manual con `sys.argv`**:
   - *Por qué se evaluó*: No requiere configuración de librerías.
   - *Por qué fue rechazada*: Frágil para gestionar flags futuros (`-h`, `--help`), mensajes de uso estandarizados y validación de subcomandos.
2. **Librerías externas de CLI (`click`, `typer`)**:
   - *Por qué se evaluó*: Sintaxis decoradora cómoda y moderna.
   - *Por qué fue rechazada*: Prohibidas en `src/` por el Principio I y Principio VII de la Constitución (solo biblioteca estándar).

---

## 4. Determinismo en la salida y orden lexicográfico

### Decisión
Ordenar vértices y aristas mediante la función nativa `sorted()` de Python, la cual opera por defecto en orden ascendente basado en puntos de código Unicode estándar (donde los caracteres en mayúsculas preceden a los de minúsculas).

### Justificación
1. **Determinismo absoluto**: La función `sorted()` en Python 3 sobre cadenas de texto compara punto de código por punto de código (Unicode code point order), garantizando reproducibilidad idéntica byte a byte en cualquier plataforma (SC-002, Principio VI).
2. **Ordenación de aristas**: Al ordenar tuplas `(source, target)`, Python aplica comparación lexicográfica primaria por el primer elemento (`source`) y secundaria por el segundo elemento (`target`), coincidiendo exactamente con la especificación de `FR-006`.

---

## 5. Estrategia de pruebas y uso de oráculo

### Decisión
Utilizar `pytest` como ejecutor de pruebas y `networkx` como dependencia exclusiva de desarrollo en `tests/` para verificar los resultados como oráculo de referencia.

### Justificación
1. **Cumplimiento constitucional**: El Principio II permite y fomenta el uso de librerías de grafos (`networkx`) en `tests/` para contrastar que el número de nodos, aristas y relaciones construidas por `graphcli` coincide al 100% con el grafo equivalente cargado en NetworkX.
2. **Pruebas de aceptación automatizadas**: Cada uno de los 18 escenarios de aceptación (`AS-001` a `AS-018`) tendrá al menos una prueba unitaria o de integración etiquetada con su identificador, cumpliendo con el Principio III y SC-003.
