"""Pruebas unitarias de orden topológico y ciclos, con NetworkX como oráculo (solo en tests)."""

import random

import networkx as nx
import pytest

from conftest import DATA
from graphcli.csv_parser import load_graph
from graphcli.graph import DirectedGraph
from graphcli.topo import CycleError, find_cycles, topological_order


def _graph(edges, isolated=()):
    g = DirectedGraph()
    for v in isolated:
        g.add_vertex(v)
    for s, t in edges:
        g.add_edge(s, t)
    return g


def _nx(g: DirectedGraph) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_nodes_from(g.get_vertices())
    G.add_edges_from(g.get_edges())
    return G


def _random_graph(rng, n, m, acyclic):
    names = [f"n{i:02d}" for i in range(n)]
    rng.shuffle(names)
    max_edges = n * (n - 1) // 2 if acyclic else n * n
    m = min(m, max_edges)
    edges = set()
    while len(edges) < m:
        i, j = rng.randrange(n), rng.randrange(n)
        if acyclic:
            if i == j:
                continue
            i, j = min(i, j), max(i, j)  # solo "hacia adelante" en el orden barajado
        edges.add((names[i], names[j]))
    return _graph(edges, isolated=names)


# ---------- in_degrees (T102) ----------

def test_in_degrees_all_vertices():
    g = _graph([("a", "b"), ("c", "b"), ("b", "d")], isolated=["z"])
    assert g.in_degrees() == {"a": 0, "b": 2, "c": 0, "d": 1, "z": 0}


# ---------- orden (US1) ----------

def _assert_valid(order, g):
    pos = {v: i for i, v in enumerate(order)}
    assert sorted(order) == g.get_vertices()  # cada vértice exactamente una vez
    for s, t in g.get_edges():
        assert pos[s] < pos[t], (s, t)


@pytest.mark.parametrize("name", ["small-dag.csv", "cs-curriculum.csv"])
def test_sample_dags_match_oracle(name):  # AS-101, AS-102, SC-101
    g = load_graph(DATA / name)
    order = topological_order(g)
    _assert_valid(order, g)
    assert order == list(nx.lexicographical_topological_sort(_nx(g)))


def test_tie_break_is_lexicographic():  # AS-103
    assert topological_order(_graph([("c", "d"), ("a", "b")])) == ["a", "b", "c", "d"]


def test_isolated_vertex_included():  # AS-106
    order = topological_order(_graph([("b", "c")], isolated=["a", "z"]))
    assert order == ["a", "b", "c", "z"]


def test_empty_graph():  # AS-107
    assert topological_order(DirectedGraph()) == []


def test_random_dags_match_oracle():  # SC-101
    rng = random.Random(2026)
    for _ in range(50):
        g = _random_graph(rng, n=rng.randint(1, 25), m=rng.randint(0, 40), acyclic=True)
        order = topological_order(g)
        _assert_valid(order, g)
        assert order == list(nx.lexicographical_topological_sort(_nx(g)))


# ---------- ciclos (US2) ----------

def _assert_real_cycle(cycle, g):
    assert cycle[0] == cycle[-1]
    edges = set(g.get_edges())
    for s, t in zip(cycle, cycle[1:]):
        assert (s, t) in edges


def test_build_with_cycle_reports_both_groups():  # AS-104
    g = load_graph(DATA / "build-with-cycle.csv")
    with pytest.raises(CycleError) as exc:
        topological_order(g)
    assert exc.value.cycles == [
        ["auth", "session", "user-profile", "auth"],
        ["metrics", "metrics"],
    ]


def test_self_loop_is_cycle():  # AS-108
    assert find_cycles(_graph([("a", "a")])) == [["a", "a"]]


def test_one_cycle_per_group():  # AS-109
    g = _graph([("a", "b"), ("b", "a"), ("b", "c"), ("c", "a")])
    assert find_cycles(g) == [["a", "b", "a"]]


def test_equal_length_cycles_tie_break():  # T115b, FR-106
    g = _graph([("a", "c"), ("c", "a"), ("a", "b"), ("b", "a")])
    assert find_cycles(g) == [["a", "b", "a"]]


def test_dag_has_no_cycles():
    assert find_cycles(load_graph(DATA / "small-dag.csv")) == []


def test_random_graphs_cycles_match_oracle():  # SC-102
    rng = random.Random(7)
    for _ in range(80):
        g = _random_graph(rng, n=rng.randint(1, 15), m=rng.randint(0, 25), acyclic=False)
        G = _nx(g)
        is_dag = nx.is_directed_acyclic_graph(G)
        if is_dag:
            _assert_valid(topological_order(g), g)
            continue
        with pytest.raises(CycleError) as exc:
            topological_order(g)
        cycles = exc.value.cycles
        expected_groups = sorted(
            min(c)
            for c in nx.strongly_connected_components(G)
            if len(c) > 1 or G.has_edge(next(iter(c)), next(iter(c)))
        )
        assert [c[0] for c in cycles] == expected_groups
        for c in cycles:
            _assert_real_cycle(c, g)


def test_long_chain_no_recursion_error():  # SC-103 (Tarjan iterativo)
    n = 5000
    edges = [(f"v{i:05d}", f"v{i + 1:05d}") for i in range(n)] + [(f"v{n:05d}", "v00000")]
    cycles = find_cycles(_graph(edges))
    assert len(cycles) == 1 and len(cycles[0]) == n + 2
