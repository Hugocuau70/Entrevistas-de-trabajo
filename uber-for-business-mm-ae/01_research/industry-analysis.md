# Análisis de industrias: estacionalidad, tamaño y scorer

Dashboard interactivo: https://claude.ai/artifact/VByXM4daawSd27nmznpuRe (privado hasta que lo compartas).
Datos en `data/` y código reproducible en `scripts/`.

## 1. Qué medimos y por qué (accuracy)

| Capa | Fuente | Qué mide | Precisión para este caso |
|---|---|---|---|
| **Gente moviéndose** | INEGI EMS (personal ocupado), EMIM y ENEC (horas trabajadas) | Cuándo hay más gente trabajando por industria | **Alta** como dato oficial; **media** como proxy de viajes (no mide viajes directamente) |
| **Actividad de negocio** | INEGI EMS (ingresos), EMIM (volumen de ventas), ENEC (valor de producción) | Cuándo factura o produce cada industria | Alta como dato; **engañosa** para viajes, porque sigue la facturación |
| **Profundidad de mercado** | Censos Económicos 2024 | Establecimientos con 251+ empleados | Alta, con dos límites: un establecimiento no es una empresa, y el rango 251+ incluye enterprise |
| **Scores del analista** | Juicio con base en la investigación pública | Intensidad de viaje, encaje con Eats, detonador H1 2027 | **Supuesto**; validar en discovery |
| **Intención de búsqueda** (pendiente) | Google Trends / Keyword Planner / SEMrush | Cuándo busca el *comprador* | Sirve para el *timing* de prospección, no para dimensionar uso |

Método: razón contra una media móvil centrada de 12 meses (quita crecimiento e inflación), promediada por mes desde 2022 y reescalada a promedio 100.

## 2. Hallazgos (para cuestionarlos)

1. **La estacionalidad nacional es suave.** En la vista "gente", la mediana de la diferencia entre el mes pico y el mes bajo es de pocos puntos. Implicación: la historia de H1 no puede descansar en "la industria viaja más en H1"; tiene que venir de **un detonador específico de la cuenta** y de **cerrar temprano**.
2. **Auditoría: la gente se mueve en Q1, la factura llega en diciembre.** El personal ocupado tiene su pico en enero–febrero, pero los ingresos lo tienen en diciembre. Si hubieras usado ingresos (o búsquedas), habrías concluido lo contrario. Es un buen ejemplo para el panel de por qué elegiste la métrica correcta.
3. **Farmacéutica: el pico comercial es marzo** (volumen de ventas), con julio como el mes bajo. La fuerza de ventas empuja en Q1.
4. **Ingeniería: el personal se sostiene de enero a julio** y baja en H2. Sumado a los data centers de Querétaro en Q2 2027, el timing encaja.
5. **Hoteles: marzo es el pico de H1.** Semana Santa 2027 cae del 21 al 28 de marzo, así que los *go-live* deberían estar antes de mediados de marzo.
6. **El sustituto incumbente, el transporte de personal (SCIAN 4854), es plano todo el año.** Es un competidor de presupuesto, no estacional.

## 3. Preguntas para que razones tú

- Si la estacionalidad es suave, ¿qué peso real le das a "H1 seasonality" en el scorer? ¿Qué cambia en el ranking si la bajas a 0?
- ¿El detonador de tu cuenta es **fechado y verificable** (una obra, una auditoría, una planta) o es una narrativa?
- En auditoría, si la gente se mueve en Q1, ¿cuándo tiene que estar firmada la cuenta para capturar esos viajes? ¿Y qué pasa con el GB de mayo y junio?
- En farmacéutica, ¿los representantes ya tienen flotilla? ¿Uber reemplaza, complementa o cubre solo a quien no tiene auto?

## 4. Herramientas: qué sí y qué no

| Herramienta | ¿La necesitamos? | Para qué | Precisión |
|---|---|---|---|
| **Apollo / Lusha / Clay** (ya las usas) | **Sí, la prioridad** | Plantilla real, oficinas y organigrama del comité de compra de 2–3 empresas finalistas | Alta a nivel empresa |
| **Google Keyword Planner** (tu cuenta de Ads) | Sí, opcional | Volumen mensual en MX de búsquedas de compra: "uber empresas", "transporte ejecutivo", "taxi empresarial", "viajes corporativos", "DiDi empresas", "Cabify empresas" | Media: *timing* del comprador |
| **Google Trends** (exportar CSV a mano) | Alternativa gratis a Keyword Planner | Mismo uso, en escala relativa | Media-baja |
| **SEMrush** | Solo si ya lo tienes | Lo mismo, más las keywords de competidores | Media |
| **Similarweb** | No | Tráfico web de las empresas: no dice nada de viajes | Baja |
| **Apify** | No, por ahora | Podría contar vacantes por mes como proxy de contratación, pero no da tiempo antes de mañana y scrapear LinkedIn rompe sus términos | — |
| **Supermetrics** | No | Solo conecta Keyword Planner; exportar el CSV directo es más rápido | — |
