# Phase 1 Data Model: Directed Graphs

**Feature**: Directed Graphs (`001-directed-graphs`)  
**Status**: Completed  
**Date**: 2026-11-02  

---

## 1. Entidades del Dominio

### 1.1 `DirectedGraph`
Representa un grafo dirigido no ponderado en memoria.

#### Estructura y Atributos internos
- **`vertices: set[str]`**: Conjunto que almacena todos los identificadores únicos de vértices presentes en el grafo, incluyendo vértices aislados (sin aristas salientes ni entrantes).
- **`_adj: dict[str, set[str]]`**: Diccionario donde cada clave es un vértice de origen (`source`) y su valor asociado es el conjunto de vértices de destino (`targets`) hacia los que existen aristas salientes.

#### Métodos y Operaciones públicas
- **`add_vertex(v: str) -> None`**:
  - Registra el vértice `v` en `self.vertices`.
  - Asegura que `self._adj[v]` esté inicializado como un conjunto vacío si aún no existe como clave.
- **`add_edge(source: str, target: str) -> None`**:
  - Registra tanto `source` como `target` en `self.vertices`.
  - Inicializa `self._adj[source]` y `self._adj[target]` si no existen.
  - Agrega `target` a `self._adj[source]`. Si la arista ya existía, el `set` la deduplica automáticamente sin duplicación ni error.
- **`get_vertices() -> list[str]`**:
  - Retorna la lista de todos los vértices en `self.vertices` ordenada lexicográficamente en orden ascendente según puntos de código Unicode estándar (donde las mayúsculas preceden a las minúsculas).
- **`get_edges() -> list[tuple[str, str]]`**:
  - Construye todas las tuplas `(source, target)` a partir de `self._adj`.
  - Retorna la lista ordenada primariamente por `source` y secundariamente por `target` según puntos de código Unicode.
- **`vertex_count -> int`**: Propiedad que retorna `len(self.vertices)`.
- **`edge_count -> int`**: Propiedad que retorna el total de aristas dirigidas únicas (`sum(len(targets) for targets in self._adj.values())`).
- **`successors(v: str) -> set[str]`**: Retorna una copia del conjunto de sucesores inmediatos de `v`. *(Diseñado para compatibilidad con Feature 2)*.
- **`in_degree(v: str) -> int`**: Retorna el número de aristas entrantes hacia `v`. *(Diseñado para compatibilidad con Feature 2)*.

---

## 2. Reglas de Validación e Invariantes

1. **Identificadores de Vértices**:
   - Todo identificador de vértice debe ser una cadena de texto no vacía tras aplicar recorte de espacios iniciales y finales (`strip()`) [FR-013].
   - No puede contener caracteres de salto de línea (`\n`, `\r`) [Assumptions].
   - Sensibilidad a mayúsculas y minúsculas: `Math` y `math` son vértices distintos e independientes con identificadores separados [FR-014, AS-016].
2. **Aristas**:
   - Toda arista conecta un `source` con un `target`.
   - Si `source == target`, se considera un auto-bucle válido y se registra en vértices y aristas [AS-006].
   - Toda arista repetida es deduplicada silenciosamente [FR-007, AS-005].
3. **Vértices aislados**:
   - Una fila con origen definido y columna de destino vacía (por ejemplo `watch,`) registra `watch` como vértice en `self.vertices` con `self._adj['watch'] = set()`, sin generar aristas salientes [FR-005, AS-004].
4. **Determinismo**:
   - El orden de salida de vértices y aristas está 100% determinado por la comparación de puntos de código Unicode estándar ascendente [FR-006, SC-002].

---

## 3. Modelo de Parsing y Flujo de Datos

```mermaid
flowchart TD
    A["Archivo CSV (Ruta en disco)"] --> B["Verificación de Existencia"]
    B -- "No existe / I/O error" --> E1["Error stderr (Código de salida 1)"]
    B -- "Existe" --> C["Apertura UTF-8 con soporte BOM (utf-8-sig)"]
    C --> D["Lectura de líneas / registros"]
    D -- "Archivo vacío (0 bytes)" --> E2["Error línea 1: Falta encabezado (Código 2)"]
    D --> F["Omitir líneas vacías / solo espacios"]
    F --> G["Validar Encabezado (primera línea no vacía)"]
    G -- "Distinto a 'source,target' en minúsculas" --> E3["Error línea N: Encabezado inválido (Código 2)"]
    G -- "Encabezado válido 'source,target'" --> H["Iteración de Filas con csv.reader (RFC 4180)"]
    H -- "Línea vacía o solo espacios" --> H
    H -- "Número de columnas != 2 (o formato corrupto)" --> E4["Fail-fast línea N: Formato inválido (Código 2)"]
    H -- "Origen vacío (',target' o ',' o ' , ')" --> E4
    H -- "Fila válida (source, target)" --> I["Trim de espacios: strip() en campos"]
    I -- "target vacío ('watch,')" --> J["DirectedGraph.add_vertex(source)"]
    I -- "source y target presentes" --> K["DirectedGraph.add_edge(source, target)"]
    J --> H
    K --> H
    H -- "Fin de archivo" --> L["Generación de Formato de Salida"]
    L --> M["Escritura en stdout (Código de salida 0)"]
```

---

## 4. Estructura de Salida Determinista

Para un objeto `DirectedGraph` cargado en memoria, el formateador de salida genera exactamente:

```text
Vertices (<N>):
  <vertice_1>
  <vertice_2>
Edges (<M>):
  <origen_1> -> <destino_1>
  <origen_2> -> <destino_2>
```

- Si el grafo no tiene vértices ni aristas (`N=0`, `M=0`), se emite:
```text
Vertices (0):
Edges (0):
```
- No hay espacios en blanco adicionales al final de las líneas ni líneas vacías intermedias no especificadas.
- Todas las salidas exitosas van a `stdout` [FR-008].
