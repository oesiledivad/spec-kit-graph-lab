# Quickstart & Validation Guide: Directed Graphs

**Feature**: Directed Graphs (`001-directed-graphs`)  
**Status**: Ready for Validation  
**Date**: 2026-11-02  

---

## 1. Requisitos Previos

- **Python 3.11** o superior instalado en el entorno (`python --version`).
- Solo biblioteca estándar para la ejecución de la aplicación (`src/`).
- Entorno de desarrollo para pruebas: `pytest` y `networkx` instalados en el entorno de pruebas.

---

## 2. Invocación Básica del CLI

El CLI se ejecuta desde la raíz del repositorio mediante el subcomando `show`:

```bash
python -m graphcli show <archivo>
```

---

## 3. Escenarios de Validación End-to-End

### Escenario 1: Carga y visualización de grafo con dependencias básicas (`small-dag.csv`)
Verifica [AS-001](spec.md#L59) y el manejo de vértices aislados [AS-004](spec.md#L99):

```bash
python -m graphcli show data/small-dag.csv
```

**Salida esperada (`stdout`)**:
```text
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
```
**Código de salida esperado**: `0`

---

### Escenario 2: Deduplicación de aristas y nombres compuestos (`cs-curriculum.csv`)
Verifica [AS-002](spec.md#L83) y [AS-005](spec.md#L100):

```bash
python -m graphcli show data/cs-curriculum.csv
```

**Comportamiento esperado**:
- Reporta exactamente `Vertices (19):` y `Edges (23):`.
- La arista duplicada `Data Structures -> Algorithms` aparece exactamente una vez.
- Código de salida: `0`.

---

### Escenario 3: Grafos con ciclos y auto-bucles (`build-with-cycle.csv`)
Verifica [AS-003](spec.md#L84) y [AS-006](spec.md#L101):

```bash
python -m graphcli show data/build-with-cycle.csv
```

**Comportamiento esperado**:
- Reporta exactamente `Vertices (11):` y `Edges (13):`.
- Muestra el auto-bucle `metrics -> metrics`.
- Código de salida: `0`.

---

### Escenario 4: Manejo de errores y política Fail-Fast

1. **Archivo no encontrado** ([AS-007](spec.md#L119)):
   ```bash
   python -m graphcli show data/archivo-inexistente.csv
   ```
   *Salida en stderr*: Mensaje de error indicando que el archivo no existe.  
   *Código de salida*: `1`

2. **Archivo vacío (0 bytes)** ([AS-008](spec.md#L120)):
   ```bash
   python -m graphcli show tests/fixtures/vacio.csv
   ```
   *Salida en stderr*: Error indicando falta de encabezado en línea 1.  
   *Código de salida*: `2`

3. **Fila inválida con detención inmediata** ([AS-013](spec.md#L124)):
   ```bash
   python -m graphcli show tests/fixtures/corrupto.csv
   ```
   *Salida en stderr*: Error indicando número de línea de la primera fila inválida.  
   *Salida en stdout*: Ninguna salida parcial.  
   *Código de salida*: `2`

---

## 4. Ejecución del Conjunto de Pruebas Automatizadas

Para validar todos los requisitos y escenarios de aceptación mediante `pytest`:

```bash
pytest
```

Para ejecutar pruebas con cobertura detallada:

```bash
pytest -v
```
