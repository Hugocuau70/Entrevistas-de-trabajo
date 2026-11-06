# Hootsuite · Enterprise AE (ES/PT) — Caso Binance LATAM (post-hackeo)

Versión alternativa del assignment de Hootsuite usando a **Binance LATAM** (Brasil, México, Argentina) después del hackeo del **29 oct 2026**. El caso GBM sigue disponible en [`../hootsuite-enterprise-ae-gbm/`](../hootsuite-enterprise-ae-gbm/) como respaldo. El formato del assignment, la checklist y los tiempos son los mismos (ver el README de GBM).

## La tesis en una línea

> El dinero se recuperó en días (98% repuesto al 3 nov); **la confianza no**: ~US$5.3 mil millones de salidas netas en 3 días y una ola de estafas de "compensación" que usan el nombre de Binance. **Esa parte de la crisis ocurre en redes sociales**, y ahí es donde Hootsuite ayuda.

**Regla de oro:** Hootsuite **no** es un producto de ciberseguridad y no habría evitado el hackeo. Dilo tú primero. Vende la capa social: proteger usuarios de estafas, reconstruir confianza país por país, hablar rápido y con aprobación de Legal.

## Por qué Binance funciona (y qué cuidar)

**A favor**
- Crisis real, enorme y de hace días: muestra que sigues las noticias y que piensas como un AE ("why now" obvio).
- La **demo de social listening** será espectacular: conversación masiva y real en español y portugués.
- **Binance LATAM = Brasil + México + Argentina**, justo el territorio en español y portugués del puesto.
- Tu experiencia es relevante: **Bitso** (cripto) en Más Gallo Media y la propuesta de **Marriott para Brasil y México** en Pinterest.
- Gancho de apertura: el hackeo empezó con una **entrevista de trabajo falsa** → *"Today I'm the one in a job interview — and I promise there's no malware in this deck."*

**Riesgos (y cómo manejarlos)**
- *"¿Hootsuite habría evitado el hackeo?"* → No. Lo dices desde el inicio (ver guion).
- Historial regulatorio de Binance (CZ y la sanción en EE.UU. en 2023) → si sale: *"As an AE I'd flag it to our deal desk and legal for KYC review — today Binance operates under licenses in 20+ jurisdictions and just applied in Brazil."* No te metas a defender a Binance.
- Algunos en el panel pueden ver cripto con escepticismo → el ángulo es **protección al usuario**, que nadie puede criticar.
- Pierdes el gancho de "trabajé con GBM" → lo reemplazas con Bitso + Brasil/México.
- Las cifras siguen cambiando (salidas, % repuesto, publicación del post-mortem): **revisa noticias el día anterior** y actualiza la slide 4 si hace falta.

## Contenido

| Archivo | Para qué |
|---|---|
| [`deck/Hootsuite_x_Binance_LATAM_Value_Presentation_Diego_Cuauhtemoc.pptx`](deck/Hootsuite_x_Binance_LATAM_Value_Presentation_Diego_Cuauhtemoc.pptx) | **Deck final para enviar** (16 slides) sobre la plantilla oficial de Hootsuite, con notas del orador. Anexo: mapa de contenidos de Binance + 5 screenshots reales de **Lumen** (query "binance", 30 oct–6 nov) con hallazgos |
| [`deck/...pdf`](deck/Hootsuite_x_Binance_LATAM_Value_Presentation_Diego_Cuauhtemoc.pdf) | Respaldo PDF (fuentes sustitutas; en Google Slides se ve con Montserrat) |
| [`01_investigacion.md`](01_investigacion.md) | El hackeo, cronología, estafas, Binance en LATAM, el caso Bybit como referencia, fuentes |
| [`02_discovery_y_estrategia.md`](02_discovery_y_estrategia.md) | Notas del discovery (role play), stakeholders, MEDDICC |
| [`03_guion_presentacion.md`](03_guion_presentacion.md) | Guion en inglés con tiempos |
| [`04_demo_social_listening.md`](04_demo_social_listening.md) | Demo de 10 min con queries en ES/PT |
| [`05_preguntas_y_objeciones.md`](05_preguntas_y_objeciones.md) | Objeciones específicas de Binance + preguntas de entrevista |
| [`06_mapa_contenidos.md`](06_mapa_contenidos.md) | Qué publicó Binance desde el 29 oct (LinkedIn, X, WhatsApp), métricas, qué funcionó y oportunidades. También es slide de apéndice |
| `deck/fill_template.py` | Regenera el deck: `python3 fill_template.py template_base.pptx salida.pptx` |

## Datos para tener en la punta de la lengua
- **29 oct 2026, 20:05 UTC:** empiezan a salir fondos de hot wallets; ~**US$6.3 mil millones**, el mayor robo cripto registrado.
- **Origen:** ingeniería social que empezó en **junio**: entrevista de trabajo falsa → malware en la máquina de un ingeniero → herramienta interna de IA alterada → control de wallets. Atribución: **TraderTraitor / Lazarus (Corea del Norte)** según TRM Labs y el FBI; Corea del Norte lo niega.
- **Respuesta:** retiros pausados; ~US$3 mil millones congelados on-chain con ayuda de Tether, Circle y Ripple; Coinbase bloqueó transferencias. Disculpa pública: *"This should not have happened…"*. Binance cubre las pérdidas con fondos propios/SAFU.
- **1 nov:** reabren retiros por fases (15 activos primero). **1-3 nov:** ~US$5.3 mil millones de salidas netas. **3 nov:** 98% repuesto; los depósitos por hora ya superan a los retiros (según Binance). CZ: *"98% choose to stay!"*
- **Estafas:** falsas compensaciones, "prioridad de retiro" con cobro, falsos anuncios de "retiros reabiertos", phishing que suplanta a Trust Wallet, falsos "investigadores de recuperación". Richard Teng (co-CEO) advirtió públicamente.
- **Binance:** 323M usuarios registrados (jul 2026). Co-CEOs **Richard Teng** y **Yi He** (desde dic 2025). **Brasil:** solicitó licencia PSAV al Banco Central el **23 oct 2026** (6 días antes del hackeo). **Argentina:** registrada como PSAV ante la CNV.
- **Referencia:** en el hackeo de **Bybit** (feb 2025, ~US$1.5 mil millones) su CEO Ben Zhou publicó en ~30 min e hizo un livestream; es el estándar de comunicación de crisis en cripto.
