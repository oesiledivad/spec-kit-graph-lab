"""Lector de archivos CSV `source,target` hacia un DirectedGraph.

Reglas (spec 001): UTF-8 con o sin BOM, encabezado exacto `source,target`,
líneas en blanco ignoradas, comillas RFC 4180, recorte de espacios,
`origen,` = vértice aislado, y detención en el primer error (fail-fast).
"""

from __future__ import annotations

import csv
from pathlib import Path

from graphcli.graph import DirectedGraph

HEADER = ["source", "target"]


class GraphFileError(Exception):
    """El archivo no existe o no se puede leer (código de salida 1)."""


class GraphFormatError(Exception):
    """El contenido del archivo no cumple el formato (código de salida 2)."""

    def __init__(self, path: Path, line: int, message: str) -> None:
        super().__init__(f"{path}: línea {line}: {message}")
        self.path = path
        self.line = line


def _read_text(path: Path) -> str:
    try:
        with open(path, encoding="utf-8-sig", newline="") as fh:
            return fh.read()
    except FileNotFoundError:
        raise GraphFileError(f"{path}: el archivo no existe") from None
    except IsADirectoryError:
        raise GraphFileError(f"{path}: es una carpeta, no un archivo") from None
    except PermissionError:
        # En Windows abrir una carpeta también da PermissionError.
        if path.is_dir():
            raise GraphFileError(f"{path}: es una carpeta, no un archivo") from None
        raise GraphFileError(f"{path}: sin permiso de lectura") from None
    except UnicodeDecodeError:
        raise GraphFileError(f"{path}: no se puede leer como UTF-8") from None
    except OSError as exc:
        raise GraphFileError(f"{path}: no se puede leer ({exc.strerror})") from None


def _parse_fields(path: Path, line_no: int, line: str) -> list[str]:
    try:
        fields = next(csv.reader([line], skipinitialspace=True, strict=True))
    except (csv.Error, StopIteration):
        raise GraphFormatError(path, line_no, "fila CSV mal formada") from None
    return [f.strip() for f in fields]


def load_graph(path: str | Path) -> DirectedGraph:
    """Carga el grafo del archivo o lanza GraphFileError / GraphFormatError."""
    path = Path(path)
    text = _read_text(path)
    graph = DirectedGraph()
    header_seen = False

    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:  # FR-011: líneas en blanco o solo espacios
            continue
        fields = _parse_fields(path, line_no, line)

        if not header_seen:  # FR-002
            if fields != HEADER:
                raise GraphFormatError(
                    path, line_no, "encabezado inválido, se esperaba 'source,target'"
                )
            header_seen = True
            continue

        if len(fields) != 2:  # FR-012 / AS-010
            raise GraphFormatError(
                path, line_no, f"se esperaban 2 columnas y hay {len(fields)}"
            )
        source, target = fields
        if not source:  # FR-005 / AS-012
            raise GraphFormatError(path, line_no, "el origen (source) está vacío")
        if target:
            graph.add_edge(source, target)
        else:  # vértice aislado, p. ej. `watch,`
            graph.add_vertex(source)

    if not header_seen:  # AS-008: archivo vacío o solo líneas en blanco
        raise GraphFormatError(
            path, 1, "falta el encabezado requerido 'source,target'"
        )
    return graph
