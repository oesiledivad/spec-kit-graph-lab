# Rarezas encontradas en `data/`

Revisión línea por línea de los tres CSV. Se verificó además que **no** hay espacios extra, tabs, `\r` (CRLF), BOM ni caracteres no ASCII en ninguno.

| Archivo | Línea | Contenido | Rareza | Qué hace la app (llenar con la decisión final) |
|---------|-------|-----------|--------|-----------------------------------------------|
| `small-dag.csv` | 11 | `watch,` | Destino vacío → vértice sin aristas | F1: vértice aislado (FR-005, AS-004). F2: aparece en el orden, al final por desempate (AS-106). |
| `cs-curriculum.csv` | 11 y 25 | `Data Structures,Algorithms` | Arista duplicada | F1: se deduplica en silencio (FR-007, AS-005). F2: no afecta el orden. |
| `cs-curriculum.csv` | varias | `Calculus I`, `Object-Oriented Programming`… | Nombres con espacios y guiones | F1: el nombre se conserva completo (AS-002). |
| `build-with-cycle.csv` | 14 | `metrics,metrics` | Auto-lazo | F1: se muestra `metrics -> metrics` (AS-006). F2: es un ciclo de longitud 1, se reporta (AS-104, AS-108). |
| `build-with-cycle.csv` | 8, 9, 10 | `auth,session` · `session,user-profile` · `user-profile,auth` | Ciclo `auth → session → user-profile → auth` | F1: se muestra normal (AS-003). F2: código 3, se reporta `auth -> session -> user-profile -> auth`; `api` y `web` dependen del ciclo pero no se listan (AS-104). |

## Conteos

| Archivo | Filas de datos | Vértices | Aristas únicas |
|---------|----------------|----------|----------------|
| `small-dag.csv` | 10 | 9 | 9 |
| `cs-curriculum.csv` | 24 | 19 | 23 |
| `build-with-cycle.csv` | 13 | 11 | 13 |

## Casos que NO están en los datos pero el spec debe cubrir (fixtures en `tests/fixtures/`)

- Línea en blanco / solo espacios
- Fila `,` (ambos vacíos) y fila `,target`
- Fila con 3 columnas y fila con 1 columna sin coma
- Encabezado faltante, distinto o con mayúsculas (`Source,Target`)
- Archivo vacío (0 bytes) y archivo con solo el encabezado
- Archivo con BOM UTF-8
- Nombres con espacios alrededor (` pants `) y con mayúsculas distintas (`Math` / `math`)
- Nombre entre comillas con coma (`"Smith, J",X`)
- Archivo inexistente / ruta que es una carpeta
