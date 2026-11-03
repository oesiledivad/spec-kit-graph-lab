"""Pruebas unitarias del lector de CSV (formato, BOM, comillas, fail-fast)."""

import pytest

from conftest import FIXTURES
from graphcli.csv_parser import GraphFileError, GraphFormatError, load_graph


def test_isolated_vertex_row():  # AS-004
    g = load_graph(FIXTURES / "isolated_vertex.csv")
    assert "watch" in g.get_vertices()
    assert all("watch" not in e for e in g.get_edges())


def test_blank_lines_are_ignored():  # AS-011
    g = load_graph(FIXTURES / "blank_lines.csv")
    assert g.get_vertices() == ["a", "b", "c"]
    assert g.get_edges() == [("a", "b"), ("b", "c")]


def test_whitespace_is_trimmed():  # AS-015
    g = load_graph(FIXTURES / "whitespace_names.csv")
    assert g.get_vertices() == ["belt", "pants", "undershorts"]
    assert ("undershorts", "pants") in g.get_edges()


def test_bom_is_removed():  # AS-017
    g = load_graph(FIXTURES / "bom_utf8.csv")
    assert g.get_edges() == [("a", "b")]


def test_quoted_names_keep_commas():  # AS-018
    g = load_graph(FIXTURES / "quoted_names.csv")
    assert g.get_edges() == [("Algorithms, Part I", "Compilers")]


def test_header_only_is_empty_graph():
    g = load_graph(FIXTURES / "header_only.csv")
    assert g.vertex_count == 0 and g.edge_count == 0


@pytest.mark.parametrize(
    "fixture, line",
    [
        ("empty.csv", 1),  # AS-008
        ("invalid_header.csv", 1),  # AS-009
        ("header_uppercase.csv", 1),  # AS-009
        ("header_after_blanks_invalid.csv", 3),  # AS-009 (línea real)
        ("malformed_columns.csv", 3),  # AS-010
        ("single_column.csv", 3),  # AS-010
        ("empty_fields_comma.csv", 3),  # AS-012
        ("empty_source.csv", 3),  # FR-005
        ("fail_fast_intermediate.csv", 4),  # AS-013
    ],
)
def test_format_errors_report_line(fixture, line):
    with pytest.raises(GraphFormatError) as exc:
        load_graph(FIXTURES / fixture)
    assert exc.value.line == line


def test_missing_file_is_file_error():  # AS-007
    with pytest.raises(GraphFileError):
        load_graph(FIXTURES / "no-existe.csv")


def test_directory_is_file_error():  # FR-010
    with pytest.raises(GraphFileError):
        load_graph(FIXTURES)


def test_non_utf8_is_file_error():  # AS-020
    with pytest.raises(GraphFileError):
        load_graph(FIXTURES / "latin1.csv")
