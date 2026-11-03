# Clarify — Feature 002: Topological Sorting

Rama: `002-...` (se crea después de mergear la 001 a `main`) · Spec: `specs/002-.../spec.md`

Cómo usar este archivo: igual que `clarify-001.md`. Antes de `/speckit-clarify`, esta es nuestra lista; después, llenar **Decisión final** y **Origen** (`agente` / `nosotros`), y verificar que cada decisión quedó en un FR y en un AS.

---

## A. Sesión 1 de `/speckit-clarify`

| # | Pregunta | Opciones | Recomendación | Decisión final | Origen | FR / AS |
|---|----------|----------|---------------|----------------|--------|---------|
| A1 | ¿Cómo pide el usuario el orden topológico? | Subcomando nuevo `order` / `topo` / opción de `show` (`show --order`) | Subcomando `order` | | | |
| A2 | ¿Cuál es el formato de salida? | Un vértice por línea / en una línea separado por ` -> ` / numerado | Un vértice por línea | | | |
| A3 | Si hay varios órdenes válidos, ¿cuál se muestra? | El menor en orden lexicográfico (siempre el mismo) / cualquiera válido | El menor en orden lexicográfico (mismo orden Unicode que la Feature 1) | | | |
| A4 | Si no existe orden (hay ciclo), ¿qué ve el usuario? | Solo "hay ciclo" / un ciclo concreto / todos los ciclos / todos los vértices involucrados | Un ciclo concreto en stderr, p. ej. `auth -> session -> user-profile -> auth` | | | |
| A5 | ¿Qué código de salida se usa cuando hay ciclo? | 1 / 2 / 3 (nuevo) | 3 (distinto de "archivo no existe" = 1 y "formato" = 2) | | | |

---

## B. Sesión 2 de `/speckit-clarify`

| # | Pregunta | Opciones | Recomendación | Decisión final | Origen | FR / AS |
|---|----------|----------|---------------|----------------|--------|---------|
| B1 | ¿Un auto-lazo (`metrics,metrics`) cuenta como ciclo? | Sí / se ignora para el orden | Sí (ciclo de longitud 1: `metrics -> metrics`) | | | |
| B2 | `build-with-cycle.csv` tiene **dos** ciclos (`auth→session→user-profile→auth` y `metrics→metrics`). ¿Se muestra uno o todos? | Uno (¿cuál, de forma determinista?) / todos | **Decidirlo nosotros** — buena pregunta para la reflexión | | | |
| B3 | ¿Se incluyen los vértices aislados (`watch`) en el orden? | Sí / no | Sí, en la posición que les toque por el desempate | | | |
| B4 | Si hay ciclo, ¿se imprime algo en stdout (orden parcial)? | Nada / orden parcial de lo que sí se pudo ordenar | Nada en stdout; solo el error en stderr | | | |
| B5 | ¿Grafo vacío (solo encabezado)? | Salida vacía, código 0 / error | Salida vacía, código 0 | | | |

---

## C. ¿Cambia algo de la Feature 1?

| # | Pregunta | Decisión final |
|---|----------|----------------|
| C1 | ¿Hubo que cambiar el **spec** de la 001 o solo el código? | |
| C2 | ¿La representación del grafo de la 001 sirvió tal cual (sucesores + grados de entrada)? | |
| C3 | ¿Se reutiliza el mismo cargador/validación de CSV con los mismos errores y códigos? | |

---

## Salidas esperadas (con desempate lexicográfico, para los AS)

Calculadas a mano / verificables con `nx.lexicographical_topological_sort`:

- **small-dag.csv** (9):
  `shirt, socks, tie, undershorts, pants, belt, jacket, shoes, watch`
- **cs-curriculum.csv** (19):
  `Calculus I, Calculus II, Computer Networks, Discrete Mathematics, Linear Algebra, Probability and Statistics, Programming Fundamentals, Computer Architecture, Object-Oriented Programming, Data Structures, Algorithms, Databases, Machine Learning, Operating Systems, Distributed Systems, Software Engineering, Capstone Project, Theory of Computation, Compilers`
- **build-with-cycle.csv**: no existe orden → error en stderr, código de ciclo.

---

## Pregunta más difícil (para REFLECTION.md)

> Escribir aquí cuál fue y por qué:

