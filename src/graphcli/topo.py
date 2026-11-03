"""Orden topológico (Kahn con heap) y detección de ciclos (Tarjan + BFS).

Implementación propia: no usa librerías de grafos (Principio II).
"""

from __future__ import annotations

import heapq
from collections import deque

from graphcli.graph import DirectedGraph


class CycleError(Exception):
    """El grafo tiene ciclos; no existe orden topológico."""

    def __init__(self, cycles: list[list[str]]) -> None:
        super().__init__(f"el grafo tiene {len(cycles)} ciclo(s)")
        self.cycles = cycles


def topological_order(graph: DirectedGraph) -> list[str]:
    """Menor orden topológico lexicográfico (FR-102, FR-103).

    Kahn: en cada paso se toma, del heap de vértices sin predecesores
    pendientes, el menor por código Unicode. O((V + E) log V).
    """
    in_deg = graph.in_degrees()
    heap = [v for v, d in in_deg.items() if d == 0]
    heapq.heapify(heap)
    order: list[str] = []
    while heap:
        v = heapq.heappop(heap)
        order.append(v)
        for w in graph.successors(v):
            in_deg[w] -= 1
            if in_deg[w] == 0:
                heapq.heappush(heap, w)
    if len(order) != graph.vertex_count:
        raise CycleError(find_cycles(graph))
    return order


def _strongly_connected_components(graph: DirectedGraph) -> list[set[str]]:
    """Tarjan iterativo (sin recursión, para no chocar con el límite de Python)."""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    components: list[set[str]] = []
    counter = 0

    for root in graph.get_vertices():
        if root in index:
            continue
        # Pila de trabajo: (vértice, iterador de sucesores ordenados)
        work = [(root, iter(sorted(graph.successors(root))))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(sorted(graph.successors(w)))))
                    advanced = True
                    break
                if w in on_stack:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[v])
            if low[v] == index[v]:
                comp: set[str] = set()
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    comp.add(w)
                    if w == v:
                        break
                components.append(comp)
    return components


def _shortest_cycle_from(graph: DirectedGraph, start: str, group: set[str]) -> list[str]:
    """Ciclo más corto start -> ... -> start dentro del grupo (BFS, sucesores ordenados)."""
    parent: dict[str, str] = {}
    queue = deque([start])
    seen = {start}
    while queue:
        v = queue.popleft()
        for w in sorted(graph.successors(v)):
            if w not in group:
                continue
            if w == start:
                path = [v]
                while path[-1] != start:
                    path.append(parent[path[-1]])
                return path[::-1] + [start]
            if w not in seen:
                seen.add(w)
                parent[w] = v
                queue.append(w)
    raise AssertionError("un grupo circular siempre contiene un ciclo")  # pragma: no cover


def find_cycles(graph: DirectedGraph) -> list[list[str]]:
    """Un ciclo por cada grupo de dependencia circular (FR-106), ordenados."""
    cycles = []
    for comp in _strongly_connected_components(graph):
        start = min(comp)
        if len(comp) > 1 or start in graph.successors(start):
            cycles.append(_shortest_cycle_from(graph, start, comp))
    return sorted(cycles, key=lambda c: c[0])
