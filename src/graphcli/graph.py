"""Grafo dirigido no ponderado (lista de adyacencia + conjunto de vértices)."""

from __future__ import annotations


class DirectedGraph:
    """Grafo dirigido no ponderado.

    - ``vertices``: todos los vértices, incluidos los aislados.
    - ``_adj``: vértice -> conjunto de sucesores. El ``set`` deduplica aristas.
    """

    def __init__(self) -> None:
        self.vertices: set[str] = set()
        self._adj: dict[str, set[str]] = {}

    def add_vertex(self, v: str) -> None:
        self.vertices.add(v)
        self._adj.setdefault(v, set())

    def add_edge(self, source: str, target: str) -> None:
        self.add_vertex(source)
        self.add_vertex(target)
        self._adj[source].add(target)

    def get_vertices(self) -> list[str]:
        """Vértices en orden ascendente por código Unicode."""
        return sorted(self.vertices)

    def get_edges(self) -> list[tuple[str, str]]:
        """Aristas ordenadas por origen y luego por destino (código Unicode)."""
        return sorted((s, t) for s, targets in self._adj.items() for t in targets)

    @property
    def vertex_count(self) -> int:
        return len(self.vertices)

    @property
    def edge_count(self) -> int:
        return sum(len(targets) for targets in self._adj.values())

    def successors(self, v: str) -> set[str]:
        """Copia de los sucesores inmediatos de ``v``."""
        return set(self._adj.get(v, set()))

    def in_degree(self, v: str) -> int:
        """Número de aristas que llegan a ``v``."""
        return sum(1 for targets in self._adj.values() if v in targets)

    def in_degrees(self) -> dict[str, int]:
        """Grado de entrada de todos los vértices en una sola pasada, O(V + E).

        Agregado en la Feature 002: llamar a ``in_degree`` por cada vértice
        costaría O(V * (V + E)).
        """
        degrees = dict.fromkeys(self.vertices, 0)
        for targets in self._adj.values():
            for t in targets:
                degrees[t] += 1
        return degrees
