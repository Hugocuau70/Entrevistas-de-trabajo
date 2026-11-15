# Design system de la presentación

> Versión 0.1 (borrador). Inspirado en el lenguaje visual de Google (Material Design / Google Workspace): neutros limpios, un azul como acento principal y los otros tres colores de Google solo para datos.
> Está escrito para pegarlo tal cual en Claude, Codex o cualquier herramienta que genere slides.

## 1. Principios

1. **Una idea por slide.** El título es una conclusión, no un tema ("Closing by January secures 70% of H1 GB", no "Forecast").
2. **Aire antes que adornos.** Mucho espacio en blanco; nada de sombras, degradados ni clip-art.
3. **El color significa algo.** Azul = foco o "nuestra propuesta". Verde = positivo. Rojo = riesgo. Gris = contexto.
4. **Los datos mandan.** Cada número lleva fuente o la etiqueta "Assumption".

## 2. Color

### Neutros (90 % de la slide)

| Token | Hex | Uso |
|---|---|---|
| `text-primary` | `#202124` | Títulos y texto principal |
| `text-secondary` | `#5F6368` | Subtítulos, notas, fuentes |
| `surface` | `#FFFFFF` | Fondo de slide |
| `surface-alt` | `#F8F9FA` | Tarjetas, bloques de apoyo |
| `outline` | `#DADCE0` | Líneas divisorias, bordes de tabla |

### Acento y datos

| Token | Hex | Uso |
|---|---|---|
| `primary` | `#1A73E8` | Acento principal, serie "nuestra estrategia", números héroe |
| `primary-container` | `#E8F0FE` | Fondo de cajas destacadas |
| `positive` | `#188038` | Crecimiento, metas alcanzadas |
| `warning` | `#F9AB00` | Supuestos y alertas (solo rellenos, **nunca texto sobre blanco**: no tiene contraste) |
| `negative` | `#D93025` | Riesgos y brechas |

Regla: máximo **dos colores de acento por slide**. Los cuatro colores juntos solo en la portada o en una gráfica categórica que lo necesite.

## 3. Tipografía

| Rol | Fuente | Tamaño (16:9) | Peso |
|---|---|---|---|
| Título de slide | Google Sans Flex [verificar disponibilidad en Google Fonts]; alternativa: **Roboto** | 28–32 pt | Medium (500) |
| Subtítulo | Roboto | 16–18 pt | Regular (400) |
| Cuerpo | Roboto | 14–16 pt | Regular (400) |
| Número héroe | Google Sans Flex / Roboto | 48–72 pt | Medium (500) |
| Fuente y notas | Roboto | 9–10 pt | Regular, color `text-secondary` |

Si construyes en Google Slides, Roboto viene incluida. No mezcles más de dos familias.

## 4. Layout

- Formato **16:9**. Márgenes de 0.5 in (≈ 48 px a 1920 × 1080).
- Retícula de **12 columnas**; el título siempre en la misma posición.
- Pie de slide: sección a la izquierda ("1 · Account Plan"), número de slide a la derecha, en `text-secondary`.
- Fuentes de datos abajo a la izquierda, 9–10 pt.

## 5. Gráficas

- Sin bordes, sin 3D, sin fondo gris. Líneas de cuadrícula en `outline` o ninguna.
- Etiqueta los valores directamente; evita leyendas cuando puedas.
- La serie protagonista en `primary`; el resto en grises (`#BDC1C6`, `#9AA0A6`).
- Montos en **USD**: `USD 350K`, `USD 1.2M`. Una sola convención en toda la presentación.

## 6. Tono y redacción (US English corporativo)

- **Audiencia:** líderes de empresas medianas. Directo, concreto, sin jerga de startup ni exageraciones ("game-changer", "revolutionary", "synergy").
- **Voz activa y verbos de acción:** "Reduce", "Consolidate", "Enable".
- **Títulos en sentence case:** "Mutual success plan", no "Mutual Success Plan" (excepción: nombres de producto como *Uber for Business*, *Uber Eats*, *Uber Central*).
- **Nombres oficiales:** Uber for Business (U4B en tablas), Uber Travel, Uber Central, Uber Vouchers, Uber Eats.
- **Números:** separador de miles con coma (2,500); porcentajes sin espacio (30%); fechas "Jan 2027" o "H1 2027".
- **Checklist antes de exportar:** ortografía en inglés de EE. UU., títulos con la misma capitalización, cifras consistentes entre slides, fuente en cada dato externo.

## 7. Alternativa por decidir: estilo monocromático tipo Uber

Negro `#000000`, blanco `#FFFFFF`, grises `#545454` / `#EEEEEE` y un solo acento para datos. Ventaja: el panel lo reconoce como "su" lenguaje visual. Riesgo: puede verse como imitación de marca; sin logos oficiales es seguro.

## 8. Prompt listo para compartir

```
Build a 16:9 corporate deck in US English following this design system:
- Background #FFFFFF; cards #F8F9FA; dividers #DADCE0.
- Text #202124 (primary) and #5F6368 (secondary).
- Accent #1A73E8 (focus, our strategy). Data: green #188038 positive, red #D93025 risk, yellow #F9AB00 fills only.
- Max two accent colors per slide. No gradients, shadows or clip-art.
- Fonts: Roboto (body 14–16 pt), titles 28–32 pt Medium; hero numbers 48–72 pt.
- Action titles in sentence case (the title states the conclusion).
- Currency format: USD 350K / USD 1.2M. Every external figure has a source in 9–10 pt.
- Tone: concise, corporate, for mid-market business leaders; no hype words.
```
