# Phase 0 Research: Topological Sorting

**Feature**: `002-topological-sort` · **Date**: 2026-11-03

## 1. Algoritmo de orden topológico

### Decisión
**Kahn con cola de prioridad (heap)**: se insertan en un heap los vértices con grado de entrada 0; en cada paso se extrae el menor, se agrega al orden y se decrementa el grado de sus sucesores, insertando los que lleguen a 0.

### Por qué
- Produce directamente el **menor orden lexicográfico** (FR-103) si la cola es un heap ordenado por código Unicode.
- **Detecta ciclos de forma natural**: si al final quedan vértices sin procesar, existe al menos un ciclo (SC-102).
- Complejidad O((V + E) log V) con la lista de adyacencia de la Feature 001.

### Alternativas rechazadas
| Alternativa | Por qué se rechazó |
|-------------|--------------------|
| DFS con post-orden invertido | Produce un orden válido pero no el menor lexicográfico; lograrlo exige trucos que complican el código. Detecta ciclos (arista de retroceso), pero solo el primero que encuentra. |
| Kahn con cola FIFO (`deque`) | Determinista, pero el orden depende del orden de inserción y no es "el menor lexicográfico" que pide la spec; más difícil de explicar al usuario. |
| Probar permutaciones | Factorial; inviable. |

## 2. Información de ciclos para el usuario

### Decisión
Cuando Kahn no procesa todos los vértices:
1. Calcular las **componentes fuertemente conexas** (Tarjan iterativo) del grafo.
2. Un grupo es "circular" si tiene más de un vértice o si su único vértice tiene auto-lazo.
3. Para cada grupo circular, el ciclo reportado es el **camino más corto** (BFS) desde el vértice menor del grupo de vuelta a sí mismo, recorriendo solo vértices del grupo y sucesores en orden Unicode.

### Por qué
- Los vértices que quedan sin procesar en Kahn incluyen también a los que solo **dependen** de un ciclo (en `build-with-cycle.csv`: `api` y `web`). Listarlos confundiría al usuario: no son la causa. Las componentes fuertemente conexas aíslan exactamente la causa.
- Listar **todos** los ciclos simples puede ser exponencial; un ciclo por grupo es finito, determinista y suficiente para que el usuario sepa qué arista romper en cada grupo.
- Tarjan **iterativo** (no recursivo) evita el límite de recursión de Python con grafos grandes.

### Alternativas rechazadas
| Alternativa | Por qué se rechazó |
|-------------|--------------------|
| Reportar solo "hay un ciclo" | No ayuda a arreglar los datos (pregunta de APPROACH.md). |
| Reportar todos los vértices sin procesar por Kahn | Incluye vértices que no están en ningún ciclo (`api`, `web`). |
| Reportar todos los ciclos simples (Johnson) | Exponencial en el peor caso; salida enorme. |
| Reportar solo el primer ciclo encontrado por DFS | Si hay varios grupos (como `auth…` y `metrics`), el usuario tendría que corregir y volver a correr varias veces. |

## 3. Representación del grafo (revisión desde la Feature 001)

La lista de adyacencia + conjunto de vértices **se mantuvo**. Lo único insuficiente fue `in_degree(v)`, que cuesta O(V + E) por vértice. Se agregó `in_degrees()` en O(V + E) total. No hubo que cambiar la estructura de datos ni la spec de la Feature 001.

## 4. Verificación con oráculo (solo tests)

- Orden válido: para cada arista `(u, v)`, `pos[u] < pos[v]`.
- Igualdad exacta con `nx.lexicographical_topological_sort(G)` (NetworkX usa el mismo criterio de desempate por orden natural de strings).
- Ciclo reportado ⇔ `not nx.is_directed_acyclic_graph(G)`.
- Grupos reportados = componentes de `nx.strongly_connected_components` con más de un vértice o con auto-lazo.
