"""Interfaz de línea de comandos de graphcli."""

from __future__ import annotations

import argparse
import sys

from graphcli.csv_parser import GraphFileError, GraphFormatError, load_graph
from graphcli.graph import DirectedGraph
from graphcli.topo import CycleError, topological_order

EXIT_OK = 0
EXIT_FILE_ERROR = 1
EXIT_FORMAT_ERROR = 2
EXIT_CYCLE = 3


def format_graph(graph: DirectedGraph) -> str:
    """Formato de salida de `show` (FR-006)."""
    lines = [f"Vertices ({graph.vertex_count}):"]
    lines += [f"  {v}" for v in graph.get_vertices()]
    lines.append(f"Edges ({graph.edge_count}):")
    lines += [f"  {s} -> {t}" for s, t in graph.get_edges()]
    return "\n".join(lines) + "\n"


def cmd_show(args: argparse.Namespace) -> int:
    graph = load_graph(args.file)
    sys.stdout.write(format_graph(graph))
    return EXIT_OK


def cmd_order(args: argparse.Namespace) -> int:
    graph = load_graph(args.file)
    try:
        order = topological_order(graph)
    except CycleError as exc:
        lines = [
            f"error: {args.file}: no existe un orden topológico; "
            f"el grafo tiene {len(exc.cycles)} ciclo(s):"
        ]
        lines += ["  " + " -> ".join(cycle) for cycle in exc.cycles]
        sys.stderr.write("\n".join(lines) + "\n")
        return EXIT_CYCLE
    sys.stdout.write("".join(f"{v}\n" for v in order))
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="graphcli",
        description="Carga grafos dirigidos desde archivos CSV (source,target).",
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="subcomando")

    show = sub.add_parser("show", help="muestra los vértices y aristas del grafo")
    show.add_argument("file", help="ruta al archivo CSV")
    show.set_defaults(func=cmd_show)

    order = sub.add_parser("order", help="muestra un orden topológico del grafo")
    order.add_argument("file", help="ruta al archivo CSV")
    order.set_defaults(func=cmd_order)
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):  # evita errores de codificación en consolas Windows
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    args = parser.parse_args(argv)  # errores de uso: argparse sale con código 2
    try:
        return args.func(args)
    except GraphFileError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_FILE_ERROR
    except GraphFormatError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_FORMAT_ERROR
