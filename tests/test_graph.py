"""Pruebas unitarias de DirectedGraph, con NetworkX como oráculo (solo en tests)."""

import networkx as nx

from conftest import DATA
from graphcli.csv_parser import load_graph
from graphcli.graph import DirectedGraph


def _to_nx(path):
    """Oráculo: construye el grafo con NetworkX a partir del CSV (sin pasar por graphcli)."""
    import csv

    g = nx.DiGraph()
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))[1:]
    for row in rows:
        if not row:
            continue
        s, t = (x.strip() for x in row)
        g.add_node(s)
        if t:
            g.add_edge(s, t)
    return g


def test_add_edge_registers_both_vertices():
    g = DirectedGraph()
    g.add_edge("a", "b")
    assert g.get_vertices() == ["a", "b"]
    assert g.get_edges() == [("a", "b")]


def test_isolated_vertex_has_no_edges():  # AS-004
    g = DirectedGraph()
    g.add_vertex("watch")
    assert g.vertex_count == 1
    assert g.edge_count == 0
    assert g.successors("watch") == set()


def test_duplicate_edges_are_deduplicated():  # AS-005
    g = DirectedGraph()
    for _ in range(3):
        g.add_edge("Data Structures", "Algorithms")
    assert g.edge_count == 1


def test_self_loop_is_a_valid_edge():  # AS-006
    g = DirectedGraph()
    g.add_edge("metrics", "metrics")
    assert g.get_vertices() == ["metrics"]
    assert g.get_edges() == [("metrics", "metrics")]


def test_case_sensitive_vertices():  # AS-016
    g = DirectedGraph()
    g.add_edge("Math", "math")
    assert g.get_vertices() == ["Math", "math"]


def test_unicode_code_point_order():  # AS-014
    g = DirectedGraph()
    g.add_edge("alpha", "Beta")
    g.add_edge("Beta", "alpha")
    assert g.get_vertices() == ["Beta", "alpha"]
    assert g.get_edges() == [("Beta", "alpha"), ("alpha", "Beta")]


def test_successors_and_in_degree():
    g = DirectedGraph()
    g.add_edge("a", "b")
    g.add_edge("c", "b")
    assert g.successors("a") == {"b"}
    assert g.in_degree("b") == 2
    assert g.in_degree("a") == 0


def test_successors_returns_copy():
    g = DirectedGraph()
    g.add_edge("a", "b")
    g.successors("a").add("zzz")
    assert g.successors("a") == {"b"}


def test_all_sample_files_match_networkx_oracle():  # AS-001, AS-002, AS-003
    for name in ("small-dag.csv", "cs-curriculum.csv", "build-with-cycle.csv"):
        ours = load_graph(DATA / name)
        oracle = _to_nx(DATA / name)
        assert set(ours.get_vertices()) == set(oracle.nodes), name
        assert set(ours.get_edges()) == set(oracle.edges), name
        assert ours.vertex_count == oracle.number_of_nodes(), name
        assert ours.edge_count == oracle.number_of_edges(), name
