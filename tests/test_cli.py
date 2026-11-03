"""Pruebas de aceptación end-to-end del subcomando `show` (Feature 001)."""

import time

from conftest import DATA, FIXTURES

SMALL_DAG_EXPECTED = """\
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
"""


def _assert_no_traceback(result):
    assert "Traceback" not in result.stderr
    assert "Traceback" not in result.stdout


# ---------- User Story 1 ----------

def test_as001_small_dag_exact_output(cli):
    r = cli("show", DATA / "small-dag.csv")
    assert r.returncode == 0
    assert r.stdout == SMALL_DAG_EXPECTED
    assert r.stderr == ""


def test_as002_cs_curriculum_counts_and_names(cli):
    r = cli("show", DATA / "cs-curriculum.csv")
    assert r.returncode == 0
    lines = r.stdout.splitlines()
    assert lines[0] == "Vertices (19):"
    assert "Edges (23):" in lines
    assert "  Object-Oriented Programming" in lines
    assert "  Calculus I -> Calculus II" in lines
    # orden determinista
    edges = lines[lines.index("Edges (23):") + 1:]
    assert edges == sorted(edges)


def test_as003_build_with_cycle_counts(cli):
    r = cli("show", DATA / "build-with-cycle.csv")
    assert r.returncode == 0
    assert r.stdout.splitlines()[0] == "Vertices (11):"
    assert "Edges (13):" in r.stdout.splitlines()
    assert "  user-profile -> auth" in r.stdout.splitlines()


def test_as014_unicode_order(cli):
    r = cli("show", FIXTURES / "case_order.csv")
    assert r.returncode == 0
    assert r.stdout == (
        "Vertices (2):\n  Beta\n  alpha\n"
        "Edges (2):\n  Beta -> alpha\n  alpha -> Beta\n"
    )


def test_output_is_deterministic(cli):  # SC-002
    outputs = {cli("show", DATA / "cs-curriculum.csv").stdout for _ in range(3)}
    assert len(outputs) == 1


# ---------- User Story 2 ----------

def test_as004_isolated_vertex(cli):
    r = cli("show", DATA / "small-dag.csv")
    lines = r.stdout.splitlines()
    assert "  watch" in lines
    assert not any("watch ->" in l or "-> watch" in l for l in lines)


def test_as005_duplicate_edge_shown_once(cli):
    r = cli("show", DATA / "cs-curriculum.csv")
    assert r.stdout.splitlines().count("  Data Structures -> Algorithms") == 1


def test_as006_self_loop(cli):
    r = cli("show", DATA / "build-with-cycle.csv")
    lines = r.stdout.splitlines()
    assert "  metrics" in lines
    assert "  metrics -> metrics" in lines


def test_as011_blank_lines(cli):
    r = cli("show", FIXTURES / "blank_lines.csv")
    assert r.returncode == 0
    assert r.stdout == "Vertices (3):\n  a\n  b\n  c\nEdges (2):\n  a -> b\n  b -> c\n"


def test_as015_whitespace_trimmed(cli):
    r = cli("show", FIXTURES / "whitespace_names.csv")
    assert r.returncode == 0
    assert "  undershorts -> pants" in r.stdout.splitlines()
    assert "  pants -> belt" in r.stdout.splitlines()


def test_as016_case_sensitive(cli):
    r = cli("show", FIXTURES / "case_sensitive_names.csv")
    assert r.returncode == 0
    assert r.stdout == "Vertices (2):\n  Math\n  math\nEdges (1):\n  Math -> math\n"


def test_as017_bom(cli):
    r = cli("show", FIXTURES / "bom_utf8.csv")
    assert r.returncode == 0
    assert r.stdout == "Vertices (2):\n  a\n  b\nEdges (1):\n  a -> b\n"


def test_as018_quoted_names(cli):
    r = cli("show", FIXTURES / "quoted_names.csv")
    assert r.returncode == 0
    assert "  Algorithms, Part I -> Compilers" in r.stdout.splitlines()


def test_header_only_is_empty_graph(cli):  # Edge case
    r = cli("show", FIXTURES / "header_only.csv")
    assert r.returncode == 0
    assert r.stdout == "Vertices (0):\nEdges (0):\n"


# ---------- User Story 3 ----------

def test_as007_missing_file(cli):
    r = cli("show", "no-existe.csv")
    assert r.returncode == 1
    assert "no-existe.csv" in r.stderr
    assert r.stdout == ""
    _assert_no_traceback(r)


def test_as008_empty_file(cli):
    r = cli("show", FIXTURES / "empty.csv")
    assert r.returncode == 2
    assert "source,target" in r.stderr and "línea 1" in r.stderr
    assert r.stdout == ""
    _assert_no_traceback(r)


def test_as009_invalid_header(cli):
    for name in ("invalid_header.csv", "header_uppercase.csv"):
        r = cli("show", FIXTURES / name)
        assert r.returncode == 2, name
        assert "encabezado" in r.stderr and "línea 1" in r.stderr, name
        assert r.stdout == ""
        _assert_no_traceback(r)


def test_as009_invalid_header_reports_real_line(cli):
    r = cli("show", FIXTURES / "header_after_blanks_invalid.csv")
    assert r.returncode == 2
    assert "línea 3" in r.stderr


def test_as010_wrong_column_count(cli):
    for name in ("malformed_columns.csv", "single_column.csv"):
        r = cli("show", FIXTURES / name)
        assert r.returncode == 2, name
        assert "línea 3" in r.stderr, name
        assert r.stdout == ""
        _assert_no_traceback(r)


def test_as012_only_comma(cli):
    r = cli("show", FIXTURES / "empty_fields_comma.csv")
    assert r.returncode == 2
    assert "línea 3" in r.stderr
    assert r.stdout == ""


def test_as013_fail_fast(cli):
    r = cli("show", FIXTURES / "fail_fast_intermediate.csv")
    assert r.returncode == 2
    assert "línea 4" in r.stderr
    assert r.stdout == ""  # sin grafo parcial


def test_as019_missing_argument(cli):
    r = cli("show")
    assert r.returncode == 2
    assert "usage" in r.stderr.lower() or "uso" in r.stderr.lower()
    assert r.stdout == ""
    _assert_no_traceback(r)


def test_as020_non_utf8_file(cli):
    r = cli("show", FIXTURES / "latin1.csv")
    assert r.returncode == 1
    assert "latin1.csv" in r.stderr and "UTF-8" in r.stderr
    assert r.stdout == ""
    _assert_no_traceback(r)


def test_directory_path_is_read_error(cli):  # FR-010
    r = cli("show", FIXTURES)
    assert r.returncode == 1
    _assert_no_traceback(r)


# ---------- Rendimiento ----------

def test_sc001_10000_edges_under_one_second(cli, tmp_path):
    path = tmp_path / "big.csv"
    rows = ["source,target"] + [f"v{i},v{i + 1}" for i in range(10_000)]
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    start = time.perf_counter()
    r = cli("show", path)
    elapsed = time.perf_counter() - start
    assert r.returncode == 0
    assert "Edges (10000):" in r.stdout
    assert elapsed < 1.0
