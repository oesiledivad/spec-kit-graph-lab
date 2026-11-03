# CLI Interface Contract: Topological Sorting

**Feature**: `002-topological-sort` · **Package**: `graphcli`

## Invocación

```bash
python -m graphcli order <archivo>
```

- `order`: subcomando nuevo (FR-101). `show` no cambia.
- `<archivo>`: CSV con las mismas reglas de la Feature 001 (`specs/001-directed-graphs/contracts/csv-contract.md`).

## stdout (éxito, código 0)

Un vértice por línea, sin encabezado, en el menor orden topológico lexicográfico (FR-103, FR-104). Grafo vacío → salida vacía.

## stderr y códigos de salida

| Condición | Código | stderr | stdout |
|-----------|--------|--------|--------|
| Éxito | 0 | vacío | orden |
| Archivo inexistente / carpeta / sin permisos / no UTF-8 | 1 | igual que `show` | vacío |
| Formato inválido / falta argumento | 2 | igual que `show` | vacío |
| El grafo tiene ciclos | 3 | `error: <archivo>: no existe un orden topológico; el grafo tiene <K> ciclo(s):` + un ciclo por línea (`  v1 -> ... -> v1`) | vacío |
