# Borrador para REFLECTION.md

Ir llenando mientras avanzamos. Al final se pasa en limpio a `REFLECTION.md` (1–2 páginas) en la raíz.

## 1. ¿Qué agente usamos? ¿Qué ayudó o estorbó?

- Agente: **Antigravity CLI (`agy`)**, integración de Spec Kit `--integration agy` (los comandos son skills: `/speckit-specify`, `/speckit-clarify`, …).
- Ayudó:
- Estorbó:

## 2. Preguntas de clarify por feature y decisiones. ¿Cuál fue la más difícil y por qué?

- Feature 001 → ver `notas/clarify-001.md`
- Feature 002 → ver `notas/clarify-002.md`
- Más difícil:

## 3. Rarezas en los datos y qué hace la app con cada una

→ ver `notas/anomalias-datos.md`

## 4. Representación del grafo

- Elegida:
- Alternativas rechazadas y por qué:
  - Matriz de adyacencia:
  - Lista de aristas:
- ¿Aguantó la Feature 2 o hubo que cambiarla?

## 5. ¿Qué reportó `/speckit-analyze` y qué cambiamos?

- Feature 001 → ver `notas/analyze-001.md`
  - Hallazgos CRITICAL/HIGH:
  - Qué cambiamos y en qué documento:
- Feature 002 → ver `notas/analyze-002.md`
  - Hallazgos CRITICAL/HIGH:
  - Qué cambiamos y en qué documento:

## 6. Un momento en que el agente hizo algo distinto a lo que queríamos

- Qué pasó:
- ¿El spec era ambiguo o el agente lo ignoró?

> Candidato ya observado: en la fase specify, el agente escribió su propia sección "Clarifications" con 3 preguntas y marcó el spec como "Ready for Planning", saltándose `/speckit-clarify`. Además dejó dos decisiones (recortar espacios y sensibilidad a mayúsculas) solo en Edge Cases, sin FR ni escenario.
