# Reglas para trabajar en paralelo (Claude Code + Codex)

Objetivo: que dos agentes trabajen en el mismo repositorio sin pisarse.

1. **Una carpeta por proyecto.** Cada agente edita solo dentro de la carpeta de su proyecto.
   - Claude Code → `uber-for-business-mm-ae/`
   - Codex → la carpeta que se le asigne (por ejemplo `<empresa>-<rol>/`)
2. **Una rama por agente.** Claude Code trabaja en `claude/*`; Codex en `codex/*`. Nadie hace push a la rama del otro ni a `main` sin que el usuario lo pida.
3. **Archivos compartidos en la raíz** (`README.md`, `COLLABORATION.md`, `AGENTS.md`, `CLAUDE.md`): solo se editan para agregar una fila o una línea propia. Nada de reescrituras.
4. **Antes de empezar una sesión:** `git fetch` y revisar que no haya cambios ajenos dentro de la propia carpeta.
5. **Commits pequeños y descriptivos**, con el prefijo de la carpeta, por ejemplo: `uber-mm-ae: add account shortlist`.
6. **Las decisiones del usuario** se registran en el `DECISIONS.md` de cada proyecto, para que cualquier agente retome el contexto sin preguntarlo de nuevo.
