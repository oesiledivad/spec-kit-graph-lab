# Quickstart & Validation Guide: Topological Sorting

**Feature**: `002-topological-sort`

## Preparación

```bash
pip install -e ".[test]"
pytest -v
```

## Validación manual

```bash
python -m graphcli order data/small-dag.csv
```
Esperado (código 0):
```text
shirt
socks
tie
undershorts
pants
belt
jacket
shoes
watch
```

```bash
python -m graphcli order data/cs-curriculum.csv
```
Esperado: los 19 vértices de AS-102, código 0.

```bash
python -m graphcli order data/build-with-cycle.csv
```
Esperado: stdout vacío, código 3, y en stderr:
```text
error: data/build-with-cycle.csv: no existe un orden topológico; el grafo tiene 2 ciclo(s):
  auth -> session -> user-profile -> auth
  metrics -> metrics
```

Ver el código de salida: `echo $?` (bash) o `echo $LASTEXITCODE` (PowerShell).
