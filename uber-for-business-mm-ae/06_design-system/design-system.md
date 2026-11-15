# Design system de la presentación

> Versión 0.2 (aprobada: estilo Uber). Monocromático, negro sobre blanco, con un solo acento para datos. Está inspirado en Base, el design system *open source* de Uber, sin usar logos ni tipografías propietarias.
> Herramienta final: **Google Slides**. Pega la sección 8 tal cual en Claude o Codex.

## 1. Principios

1. **Una idea por slide.** El título es una conclusión, no un tema ("Closing by January secures most of H1 GB", no "Forecast").
2. **Negro, blanco y aire.** El contraste viene del tamaño y del peso tipográfico, no del color.
3. **El color significa algo.** Azul = foco o "nuestra propuesta". Verde = positivo. Rojo = riesgo. Gris = contexto.
4. **Los datos mandan.** Cada número lleva fuente o la etiqueta "Assumption".

## 2. Color

### Base (90 % de la slide)

| Token | Hex | Uso |
|---|---|---|
| `ink` | `#000000` | Títulos, texto principal, slides de sección (fondo negro con texto blanco) |
| `paper` | `#FFFFFF` | Fondo de slide |
| `content-secondary` | `#545454` | Subtítulos, notas |
| `content-tertiary` | `#757575` | Fuentes, pies de slide |
| `surface-alt` | `#F6F6F6` | Tarjetas y bloques de apoyo |
| `surface-strong` | `#EEEEEE` | Celdas de tabla alternas |
| `border` | `#E2E2E2` | Líneas divisorias |

### Acento y datos (solo en gráficas, números héroe y estados)

| Token | Hex | Uso |
|---|---|---|
| `accent` | `#276EF1` | La serie de "nuestra estrategia" o el dato clave de la slide |
| `positive` | `#05944F` | Metas alcanzadas, crecimiento |
| `warning` | `#FFC043` | Supuestos (solo rellenos, **nunca texto sobre blanco**) |
| `negative` | `#E11900` | Riesgos y brechas |

Regla: **un solo color de acento por slide**, además del negro. Escalas de intensidad (heatmaps) en grises, de `#F6F6F6` a `#000000`, como en el dashboard.

## 3. Tipografía (disponible en Google Slides)

Uber Move es propietaria; usa **Inter** (Google Slides → Fuentes → Más fuentes → Inter).

| Rol | Fuente | Tamaño (16:9) | Peso |
|---|---|---|---|
| Título de slide | Inter | 28–32 pt | Bold (700) |
| Subtítulo | Inter | 16–18 pt | Regular (400), `content-secondary` |
| Cuerpo | Inter | 14–16 pt | Regular (400) |
| Número héroe | Inter | 54–80 pt | Bold (700) |
| Etiquetas y fuentes | Inter | 9–10 pt | Medium (500), `content-tertiary` |

Una sola familia en toda la presentación. Jerarquía solo con tamaño y peso.

## 4. Layout

- Formato **16:9**, márgenes de 0.5 in.
- Título arriba a la izquierda, siempre en la misma posición.
- **Slides de sección:** fondo negro, número y nombre de la sección en blanco ("01 · Account plan"). Ahí la numeración sí es información: son las tres partes del caso.
- Pie: sección a la izquierda, número de slide a la derecha, en `content-tertiary`.
- Esquinas de tarjetas: 8 px o rectas. Sin sombras ni degradados.

## 5. Gráficas

- Sin bordes, sin 3D. Cuadrícula en `border` o ninguna.
- Etiqueta los valores directamente; evita leyendas.
- Serie protagonista en `ink` o `accent`; el resto en grises (`#AFAFAF`, `#757575`).
- Montos en **USD**: `USD 350K`, `USD 1.2M`. Una sola convención.

## 6. Tono y redacción (US English corporativo)

- **Audiencia:** líderes de empresas medianas. Directo, concreto, sin jerga de startup ni exageraciones ("game-changer", "revolutionary", "synergy").
- **Voz activa y verbos de acción:** "Reduce", "Consolidate", "Enable".
- **Títulos en sentence case:** "Mutual success plan" (excepto nombres de producto).
- **Nombres oficiales:** Uber for Business (U4B en tablas), Uber Travel, Uber Central, Uber Vouchers, Uber Eats.
- **Números:** separador de miles con coma (2,500); porcentajes sin espacio (30%); fechas "Jan 2027", "H1 2027".
- **Checklist antes de exportar:** ortografía US English, capitalización consistente, cifras iguales entre slides, fuente en cada dato externo.

## 7. Lo que no hacemos

- No usamos el logo de Uber ni la tipografía Uber Move: es una propuesta de un candidato, no material oficial.
- No mezclamos los colores de Google ni más de un acento.

## 8. Prompt listo para compartir

```
Build a 16:9 corporate deck in US English for Google Slides, in a monochrome style inspired by Uber's Base design system (no Uber logo).
- Background #FFFFFF; section-divider slides #000000 with white text.
- Text #000000 (primary), #545454 (secondary), #757575 (sources, footers). Cards #F6F6F6; dividers #E2E2E2.
- One accent per slide: #276EF1 (our strategy / key figure). Status: green #05944F positive, red #E11900 risk, yellow #FFC043 fills only.
- Heatmaps and intensity scales in greys from #F6F6F6 to #000000.
- Font: Inter only. Titles 28–32 pt Bold; body 14–16 pt Regular; hero numbers 54–80 pt Bold; sources 9–10 pt Medium.
- No gradients, shadows, clip-art or emoji. Corners 8 px or square.
- Action titles in sentence case (the title states the conclusion).
- Currency: USD 350K / USD 1.2M. Every external figure has a source line.
- Tone: concise, corporate, for mid-market business leaders; no hype words.
```
