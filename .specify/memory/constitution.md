<!--
SYNC IMPACT REPORT
==================
- Version change: Unversioned template -> 1.0.0
- Ratification date: 2026-10-30
- Last amended date: 2026-10-30
- Principles defined:
  * I. Stack y estructura (Added)
  * II. Grafos y algoritmos propios (NO NEGOCIABLE) (Added)
  * III. Pruebas obligatorias (NO NEGOCIABLE) (Added)
  * IV. La spec y el código siempre coinciden (Added)
  * V. Comportamiento del CLI (Added)
  * VI. Salida determinista (Added)
  * VII. Simplicidad (Added)
- Added sections:
  * Core Principles
  * Flujo de desarrollo
  * Governance
- Removed sections:
  * [SECTION_2_NAME], [SECTION_3_NAME] (scaffold placeholders replaced)
- Follow-up TODOs:
  * None (all placeholders resolved)
-->

# Dependency Graph CLI Constitution

## Core Principles

### I. Stack y estructura
- Python 3.11 o superior. Solo biblioteca estándar en el código de la aplicación.
- Pruebas con pytest.
- Estructura fija: `src/` para la aplicación, `tests/` para las pruebas, `data/` para los CSV de ejemplo, `tests/fixtures/` para CSV creados para pruebas.
- El CLI se ejecuta con `python -m <paquete> <subcomando> <archivo>`.

### II. Grafos y algoritmos propios (NO NEGOCIABLE)
- Prohibido en `src/`: NetworkX, igraph, graph-tool, `graphlib`, `scipy.sparse.csgraph` o cualquier librería que implemente grafos o algoritmos sobre grafos.
- Esas librerías SOLO se permiten en `tests/`, como oráculo para verificar resultados.
- La representación del grafo en memoria se elige en el plan y debe justificarse en `research.md`, incluyendo las alternativas rechazadas y por qué.

### III. Pruebas obligatorias (NO NEGOCIABLE)
- Cada escenario de aceptación de cada `spec.md` tiene al menos una prueba automatizada que lo referencia por su identificador.
- Cada requisito funcional tiene al menos una tarea y una prueba.
- En `tasks.md`, las pruebas van antes del código que prueban.
- Todas las pruebas pasan antes de hacer merge a `main`.

### IV. La spec y el código siempre coinciden
- `spec.md` es la fuente de verdad del comportamiento.
- Si se encuentra un bug, primero se decide si está mal la spec o el código. Si es la spec, se corrige primero la spec y luego el código. Nunca quedan en desacuerdo.
- Las specs describen QUÉ hace el sistema, nunca CÓMO: no mencionan Python, clases, estructuras de datos, módulos ni algoritmos.

### V. Comportamiento del CLI
- Los resultados se escriben en stdout. Los errores y advertencias se escriben en stderr.
- Los mensajes de error dicen qué falló y, cuando aplica, el archivo y el número de línea.
- Código de salida 0 si todo sale bien y distinto de 0 si hay error; cada código se define en la spec.
- Nunca se muestra un traceback de Python al usuario.

### VI. Salida determinista
- La misma entrada produce siempre exactamente la misma salida.
- Cuando existan varios resultados válidos, la spec define cuál se muestra.

### VII. Simplicidad
- Solo se implementa lo que pide la spec actual: sin configuración extra, plugins, capas de abstracción ni features especulativas.
- Toda dependencia externa en `src/` está prohibida salvo que se justifique en el plan y se apruebe.

## Flujo de desarrollo
- Cada feature pasa por todas las fases en su propia rama: specify → clarify → plan → tasks → analyze → implement.
- La feature N+1 no se especifica hasta que la feature N esté terminada y mergeada a `main`.
- Al menos un commit por fase y por feature.
- Todo hallazgo CRITICAL o HIGH de analyze se corrige en el documento donde se origina antes de implementar.
- Nunca se suben API keys ni secretos al repositorio.

## Governance
- Esta constitución tiene prioridad sobre cualquier otro documento.
- Se modifica solo si una feature lo exige; cada cambio sube la versión (semver) y se registra en el Sync Impact Report.
- Política de versionado (SemVer):
  - **MAJOR**: Modificaciones incompatibles, eliminación de principios o cambios estructurales en la gobernanza.
  - **MINOR**: Incorporación de nuevos principios o secciones, o ampliación material de las reglas existentes.
  - **PATCH**: Correcciones de formato, ortografía o precisiones de redacción no semánticas.
- Cumplimiento: Toda revisión de pull request y avance de fase debe verificar el cumplimiento estricto de esta constitución antes de fusionar cambios a `main`.

**Version**: 1.0.0 | **Ratified**: 2026-10-30 | **Last Amended**: 2026-10-30
