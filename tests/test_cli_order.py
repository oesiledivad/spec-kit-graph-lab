"""Pruebas de aceptación end-to-end del subcomando `order` (Feature 002)."""

import time

from conftest import DATA, FIXTURES

SMALL_DAG_ORDER = "shirt\nsocks\ntie\nundershorts\npants\nbelt\njacket\nshoes\nwatch\n"

CS_ORDER = [
    "Calculus I", "Calculus II", "Computer Networks", "Discrete Mathematics",
    "Linear Algebra", "Probability and Statistics", "Programming Fundamentals",
    "Computer Architecture", "Object-Oriented Programming", "Data Structures",
    "Algorithms", "Databases", "Machine Learning", "Operating Systems",
    "Distributed Systems", "Software Engineering", "Capstone Project",
    "Theory of Computation", "Compilers",
]


def _no_traceback(r):
    assert "Traceback" not in r.stderr and "Traceback" not in r.stdout


# ---------- User Story 1 ----------

def test_as101_small_dag(cli):
    r = cli("order", "data/small-dag.csv")
    assert r.returncode == 0
    assert r.stdout == SMALL_DAG_ORDER
    assert r.stderr == ""


def test_as102_cs_curriculum(cli):
    r = cli("order", "data/cs-curriculum.csv")
    assert r.returncode == 0
    assert r.stdout.splitlines() == CS_ORDER


def test_as103_lexicographic_tie_break(cli):
    outs = {cli("order", FIXTURES / "two_chains.csv").stdout for _ in range(3)}
    assert outs == {"a\nb\nc\nd\n"}


def test_as106_isolated_vertex_once(cli):
    r = cli("order", "data/small-dag.csv")
    assert r.stdout.splitlines().count("watch") == 1


def test_as107_header_only(cli):
    r = cli("order", FIXTURES / "header_only.csv")
    assert r.returncode == 0
    assert r.stdout == ""


# ---------- User Story 2 ----------

def test_as104_build_with_cycle(cli):
    r = cli("order", "data/build-with-cycle.csv")
    assert r.returncode == 3
    assert r.stdout == ""
    assert r.stderr == (
        "error: data/build-with-cycle.csv: no existe un orden topológico; "
        "el grafo tiene 2 ciclo(s):\n"
        "  auth -> session -> user-profile -> auth\n"
        "  metrics -> metrics\n"
    )


def test_as108_self_loop(cli):
    r = cli("order", FIXTURES / "self_loop_only.csv")
    assert r.returncode == 3
    assert "  a -> a\n" in r.stderr
    assert r.stdout == ""


def test_as109_one_cycle_per_group(cli):
    r = cli("order", FIXTURES / "multi_cycle_group.csv")
    assert r.returncode == 3
    assert "1 ciclo(s)" in r.stderr
    assert r.stderr.endswith("  a -> b -> a\n")


# ---------- User Story 3 ----------

def test_as105_missing_file(cli):
    r = cli("order", "no-existe.csv")
    assert r.returncode == 1
    assert "no-existe.csv" in r.stderr
    assert r.stdout == ""
    _no_traceback(r)


def test_as110_format_error(cli):
    r = cli("order", FIXTURES / "malformed_columns.csv")
    assert r.returncode == 2
    assert "línea 3" in r.stderr
    assert "ciclo" not in r.stderr
    assert r.stdout == ""


def test_as111_missing_argument(cli):
    r = cli("order")
    assert r.returncode == 2
    assert "usage" in r.stderr.lower()
    assert r.stdout == ""
    _no_traceback(r)


def test_show_unchanged(cli):  # Assumption: `show` no cambia
    r = cli("show", DATA / "build-with-cycle.csv")
    assert r.returncode == 0
    assert r.stdout.startswith("Vertices (11):")


# ---------- Polish ----------

def test_sc103_10000_edges_under_one_second(cli, tmp_path):
    path = tmp_path / "big.csv"
    rows = ["source,target"] + [f"v{i:05d},v{i + 1:05d}" for i in range(10_000)]
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    start = time.perf_counter()
    r = cli("order", path)
    elapsed = time.perf_counter() - start
    assert r.returncode == 0
    assert len(r.stdout.splitlines()) == 10_001
    assert elapsed < 1.0


def test_sc104_deterministic(cli):
    runs = {(cli("order", "data/build-with-cycle.csv").stderr,
             cli("order", "data/cs-curriculum.csv").stdout) for _ in range(3)}
    assert len(runs) == 1
