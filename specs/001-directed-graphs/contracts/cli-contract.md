# CLI Interface Contract: Directed Graphs

**Feature**: Directed Graphs (`001-directed-graphs`)  
**Package**: `graphcli`  
**Execution Command**: `python -m graphcli show <archivo>`  
**Status**: Completed  
**Date**: 2026-11-02  

---

## 1. Interfaz de Invocación

### Subcomando `show`
Visualiza la lista ordenada de vértices y aristas dirigidas de un grafo a partir de un archivo CSV.

```bash
python -m graphcli show <path-to-csv-file>
```

### Argumentos de línea de comandos
- **`show`**: Subcomando obligatorio de visualización [FR-001].
- **`<archivo>`**: Argumento posicional obligatorio que especifica la ruta al archivo CSV que contiene la definición del grafo.

---

## 2. Contrato de Salida Estándar (`stdout`)

Toda salida de operación exitosa se emite estrictamente a `stdout` con código de retorno `0`.

### Formato determinista
```text
Vertices (<N>):
  <vertice_1>
  <vertice_2>
...
Edges (<M>):
  <source_1> -> <target_1>
  <source_2> -> <target_2>
...
```

### Reglas de formateo
1. Cabecera de vértices: `Vertices (<N>):` donde `<N>` es la cantidad entera de vértices únicos.
2. Cada vértice se imprime en una línea independiente precedido por dos espacios de indentación (`  `).
3. Vértices ordenados estrictamente por puntos de código Unicode estándar en orden ascendente (mayúsculas antes de minúsculas).
4. Cabecera de aristas: `Edges (<M>):` donde `<M>` es la cantidad entera de aristas dirigidas únicas.
5. Cada arista se imprime en formato `  <source> -> <target>` con dos espacios de indentación.
6. Aristas ordenadas primariamente por vértice de origen (`source`) y secundariamente por vértice de destino (`target`) bajo el criterio de puntos de código Unicode.
7. Grafo vacío (por ejemplo archivo solo con encabezado `source,target`):
   ```text
   Vertices (0):
   Edges (0):
   ```

---

## 3. Contrato de Salida de Errores (`stderr`) y Códigos de Salida

Ningún mensaje de error se escribe en `stdout`. Todos los errores se dirigen exclusivamente a `stderr` sin mostrar tracebacks de Python al usuario [Principio V, SC-004].

| Condición | Código de salida | Formato / Destino del mensaje |
|-----------|------------------|-------------------------------|
| Ejecución exitosa | `0` | Salida del grafo en `stdout`. `stderr` vacío. |
| Archivo no encontrado o no legible por permisos | `1` | `stderr`: Mensaje descriptivo indicando el nombre del archivo no encontrado o inaccesible. |
| Invocación sin argumentos requeridos (ej. sin archivo o sin subcomando) | `2` | `stderr`: Mensaje de uso y sintaxis de línea de comandos. |
| Archivo vacío (0 bytes) | `2` | `stderr`: Error indicando que el archivo carece del encabezado requerido `source,target` en la línea 1. |
| Encabezado inválido o faltante en la primera línea no vacía | `2` | `stderr`: Error indicando encabezado inválido en la línea N correspondiente. |
| Fila con formato inválido (columnas != 2, origen vacío, comas malformadas) | `2` | `stderr`: Error indicando número de línea que contiene el formato inválido (aplicando detención inmediata fail-fast). |
