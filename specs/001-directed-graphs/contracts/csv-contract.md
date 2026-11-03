# CSV File Format Contract: Directed Graphs

**Feature**: Directed Graphs (`001-directed-graphs`)  
**Status**: Completed  
**Date**: 2026-11-02  

---

## 1. Estructura y Codificación del Archivo

1. **Codificación**:
   - Codificado en UTF-8 estándar [Assumptions].
   - Se admite y descarta de forma transparente el prefijo Byte Order Mark (BOM inicial `\ufeff` / `\xef\xbb\xbf`) sin corromper el contenido [FR-002, AS-017].
2. **Encabezado**:
   - La primera línea no vacía del archivo debe ser exactamente `source,target` en minúsculas [FR-002, AS-009].
   - Los espacios en blanco al inicio o final de la línea del encabezado se ignoran.
   - Cualquier variación de mayúsculas y minúsculas (por ejemplo `Source,Target` o `SOURCE,TARGET`) o nombre de columna distinto es rechazada inmediatamente con código de salida `2`.
3. **Líneas en blanco**:
   - Líneas vacías o compuestas únicamente por espacios en blanco son ignoradas silenciosamente en cualquier posición del archivo (antes del encabezado, entre registros o al final) [FR-011, AS-011].

---

## 2. Sintaxis de Registros y Delimitadores (RFC 4180)

1. **Número de columnas**:
   - Cada registro de datos debe contener exactamente 2 columnas delimitadas por una coma [FR-003, AS-010].
2. **Entrecomillado**:
   - Se respeta el estándar de comillas dobles RFC 4180 [FR-015, AS-018].
   - Nombres de vértices que contengan comas deben ir encerrados entre comillas dobles (ejemplo: `"Algorithms, Part I",Compilers`).
   - Las comillas delimitadoras externas se remueven al extraer el identificador del vértice.
3. **Recorte de espacios (Strip)**:
   - Se eliminan los espacios en blanco iniciales y finales de cada nombre de vértice (ejemplo: `  undershorts  ,  pants  ` se convierte en `undershorts` y `pants`) [FR-013, AS-015].
4. **Vértices aislados**:
   - Una fila con origen presente y destino vacío (por ejemplo `watch,` o `watch, `) es válida y define a `watch` como un vértice sin aristas salientes [FR-005, AS-004].
5. **Filas inválidas (Fail-Fast)**:
   - Filas con origen vacío (por ejemplo `,target`, `,` o ` , `) son inválidas.
   - Filas con número de campos diferente a 2 son inválidas.
   - Ante la primera fila inválida, el parser aborta la carga inmediatamente sin continuar leyendo el archivo y emite el error en `stderr` con código de salida 2 [FR-012, AS-012, AS-013].
