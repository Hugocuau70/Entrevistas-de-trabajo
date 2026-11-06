# 01 · Investigación — Binance después del hackeo

> Corte: 6 nov 2026. Las cifras cambian a diario y las fuentes no siempre coinciden (sobre todo salidas netas y % repuesto, porque cubren ventanas de tiempo distintas). Cita siempre la fecha: "as of November 3…". Lo de Hootsuite (Social OS, Wisdom, casos) está en [`../hootsuite-enterprise-ae-gbm/01_investigacion.md`](../hootsuite-enterprise-ae-gbm/01_investigacion.md).

## A. El hackeo

### Cronología
| Fecha | Qué pasó |
|---|---|
| Jun 2026 | Primer paso de los atacantes: ingeniería social a un ingeniero de Binance |
| Sep 2026 | Contactan a otro ingeniero vía plataforma de empleo → **entrevista falsa** → instalación de malware |
| 23 oct | Binance solicita licencia de proveedor de criptoactivos al Banco Central de Brasil (BBrasil) |
| **29 oct, 20:05 UTC** | Empiezan a drenarse hot wallets (segunda ola ~23:05 UTC) en ~10 redes. Retiros pausados |
| 29-30 oct | Binance confirma ~**US$6.3 mil millones** afectados; ~US$3 mil millones congelados on-chain (Tether, Circle, Ripple ayudan; Coinbase bloquea transferencias) |
| 30 oct | Sin proceso de reclamación anunciado → cualquier "formulario de compensación" es estafa (McAfee) |
| 31 oct | Binance dice que los atacantes borraron evidencia; planea reabrir retiros el domingo |
| **1 nov** | Reapertura de retiros por fases (15 activos: BTC, ETH, SOL…). Binance advierte sobre falsas compensaciones y "prioridad de retiro" |
| 1-3 nov | Salidas netas: ~US$2.5 mil millones (1 nov, tarde) → ~US$3.6-4.65 mil millones (CNBC) → ~**US$5.28 mil millones** acumulados (FinanceFeeds) |
| 3 nov | **98%** de los activos robados repuestos; depósitos por hora superan retiros (03:00 UTC). Richard Teng explica la entrevista falsa y la herramienta de IA alterada. Binance traerá un experto independiente para revisar su respuesta |

### Mensajes oficiales (útiles para citar)
- Disculpa: *"This should not have happened, and we apologise for the concern, disruption and uncertainty it caused our users, partners and the wider industry."*
- Yi He (X): *"User funds are safe… Binance will cover all hacking losses."*
- Advertencia: *"Users should remain cautious of scams and should not trust unofficial links, messages, or requests for account information."*
- CZ (accionista mayoritario, sin rol operativo): *"98% choose to stay!"*
- Yi He: Binance detectó y frenó **57** casos de amenazas ligadas a Corea del Norte en 2026.

### La ola de estafas (el dolor central del caso)
- Falsas **compensaciones** y formularios de "víctima del hackeo"; falsos **airdrops**.
- **"Priority processing"** / prioridad de retiro con cobro (Binance lo desmintió).
- Falsos anuncios de **"retiros reabiertos"**.
- Phishing por correo **"Binance Hack Also Impacts Trust Wallet Users"** (EE.UU., UK, Australia, Irlanda, Sudáfrica).
- Falsos **"investigadores de recuperación"** que cobran o piden la frase semilla.
- Señales oficiales: el soporte real no contacta primero, nunca pide contraseña, 2FA ni frase semilla; el anti-phishing code aparece en correos legítimos.
- En LATAM esto corre en **español y portugués**, por WhatsApp, Telegram, X, Instagram y TikTok. Tu pitch: *encontrarlo antes de que el usuario caiga*.

## B. Binance en contexto
- **323M** usuarios registrados (14 jul 2026, 9º aniversario); dice tener ~43% de los 741M de holders de cripto del mundo.
- Co-CEOs: **Richard Teng** (desde fines de 2023) y **Yi He** (cofundadora, co-CEO desde el 3 dic 2025; antes a cargo de servicio al cliente/marketing). CZ se declaró culpable en EE.UU. en 2023 (anti-lavado) y no puede tener rol activo.
- **Brasil:** solicitud de licencia PSAV el 23 oct 2026; desde el 27 oct recortó 8 servicios y 22 tokens; desde el 1 nov, los usuarios deben declarar finalidad y contraparte en movimientos internacionales (Res. 521/2025 BCB). → **Cada mensaje público está bajo la lupa del regulador.**
- **Argentina:** Binance Services Latinoamérica S.A., PSAV registrado ante la CNV (n.º 76); depósitos en pesos y P2P.
- **México:** no encontré información regulatoria específica confiable → no afirmes nada concreto.
- Competidores en LATAM para share of voice: **Coinbase, OKX, Bybit, Bitso, Mercado Bitcoin**, Lemon, Ripio, Mercado Pago (cripto).

## C. Referencia de crisis: Bybit (feb 2025)
- Hackeo de ~US$1.46-1.5 mil millones (también atribuido a Lazarus).
- Ben Zhou publicó en X en ~**30 min** y luego hizo un livestream de ~2 h; actualizaciones diarias después.
- Lecciones citadas: velocidad, lenguaje llano ("institutional language reads as evasion"), combinar canales oficiales con la voz del CEO, infraestructura de transparencia preparada **antes** de la crisis.
- Úsalo como **estándar del mercado**, no para criticar a Binance (Binance también se movió rápido en lo financiero).

## D. Ángulo Hootsuite (cómo conecta)
| Dolor | App | Valor |
|---|---|---|
| Estafas que suplantan a Binance en ES/PT | **Lumen by Talkwalker** (150M+ fuentes, 187 idiomas, reconocimiento de imagen/logo) + alertas | Detectar antes, advertir desde canales oficiales, pedir takedown |
| Miles de DMs ("¿mi dinero está seguro?", "¿cuándo puedo retirar?") | **Nest** + **Wisdom** | Una bandeja, ruteo, SLAs, respuestas verificadas |
| El "98% repuesto" no llega a la gente; rumores por país | **Lumen** + **Wisdom** | Sentimiento por hora y por país; qué rumor mover |
| Legal tiene que aprobar todo (licencia en Brasil) | **Perch** | Aprobaciones en minutos, publicación simultánea |
| Mensaje oficial sepultado por el ruido | **Parliament** | Empleados/embajadores comparten la versión oficial |

## E. Fuentes
- [Binance pauses withdrawals as hackers suspected of stealing billions — TechCrunch (29 oct)](https://techcrunch.com/2026/10/29/binance-pauses-withdrawals-as-hackers-suspected-of-stealing-billions-in-crypto/)
- [$6.3 billion Binance hack is largest crypto theft on record — CNBC](https://www.cnbc.com/2026/10/29/circle-tether-freeze-funds-impacted-by-potential-binance-security-issue.html)
- [Binance halts trading after biggest-ever crypto hack — Axios](https://www.axios.com/2026/10/29/binance-cyberattack-crypto-heist)
- [Suspected Binance hack sets off scramble to lock down billions — Washington Post](https://www.washingtonpost.com/technology/2026/10/29/suspected-binance-hack-sets-off-scramble-lock-down-billions-crypto/)
- [What happens to customer funds on exchanges — CNBC Make It](https://www.cnbc.com/make-it/2026/10/30/binance-crypto-hack-customer-funds.html)
- [Binance says hackers wiped evidence, aims to reopen withdrawals Sunday — Northeast Times](https://northeasttimes.com/2026/10/31/binance-says-hackers-wiped-evidence-aims-to-reopen-withdrawals-sunday/)
- [Binance withdrawals resume following $6 billion hack — CNN (1 nov)](https://www.cnn.com/2026/11/01/business/binance-withdrawals-crypto-heist)
- [Binance resumes withdrawals following $6.3 billion breach — TechCrunch](https://techcrunch.com/2026/11/01/binance-resumes-withdrawals-following-6-3-billion-breach/)
- [Binance restarts withdrawals as questions linger — Insurance Journal](https://www.insurancejournal.com/news/international/2026/11/01/891003.htm)
- [Binance sees $3.64 billion in net outflows as withdrawals resume — CNBC (2 nov)](https://www.cnbc.com/2026/11/02/binance-outflow-hack-bitcoin.html)
- [Binance: $5.28B net outflows, 95% of $6.3B hack replaced — FinanceFeeds](https://financefeeds.com/binance-says-withdrawals-have-normalized-after-6-3-billion-crypto-hack/)
- [Binance inflows flip positive after post-hack exodus — Cryptonews](https://cryptonews.net/news/market/33698473/)
- [Binance co-CEO Richard Teng says hackers used fake job interviews, AI tool — CNBC (3 nov)](https://www.cnbc.com/2026/11/03/binance-co-ceo-teng-says-hackers-used-fake-job-interviews-to-steal-6point3-billion-in-crypto.html)
- [Hackers used fake job interview before $6.3 billion hack — NBC News](https://www.nbcnews.com/business/markets/binance-hack-fake-job-interview-heist-rcna607238)
- [Binance revela que uno de sus ingenieros descargó malware — La Jornada](https://www.jornada.com.mx/noticia/2026/11/03/economia/binance-revela-que-uno-de-sus-ingenieros-descargo-malware-que-propicio-hackeo)
- [Falsa entrevista de trabajo habría gatillado histórico hackeo — Emol](https://www.emol.com/noticias/Economia/2026/11/03/1216030/binance-hackeo-entrevista-falsa-trabajo.html)
- [Hackeo a Binance: el paso a paso — MDZ](https://mdzol.com/tecnologia/2026/11/4/hackeo-a-binance-el-paso-a-paso-del-millonario-ataque-que-comenzo-con-una-falsa-entrevista-de-trabajo-1993067.html)
- [How Binance’s $6.3 billion hack went down — Khaleej Times](https://www.khaleejtimes.com/business/how-binances-63-billion-hack-went-down-across-the-world?amp=1)
- [2026 Binance hack — Wikipedia](https://en.wikipedia.org/wiki/2026_Binance_hack)
- [Binance warns of fake compensation offers as withdrawals resume — Bitcoin.com](https://news.bitcoin.com/featured/binance-warns-of-fake-compensation-offers-as-withdrawals-resume/)
- [Binance warns of withdrawal scams — Crypto Times](https://www.cryptotimes.io/2026/11/02/binance-warns-of-withdrawal-scams-as-crypto-services-resume/)
- [Binance crypto heist: how to protect your crypto — McAfee](https://www.mcafee.com/blogs/security-news/binance-crypto-heist/)
- [Binance breach fuels crypto phishing scams — Bitdefender](https://www.bitdefender.com/en-us/blog/hotforsecurity/binance-breach-crypto-phishing-scams)
- [Binance hack fallout: scams and account takeovers — Fingerprint](https://fingerprint.com/blog/binance-hack-scams-account-takeover/)
- [Binance marks nine years: nearly half of all crypto holders — Gulf News](https://gulfnews.com/gn-focus/company-news/binance-marks-nine-years-nearly-half-of-all-crypto-holders-use-binance-1.500610143)
- [Binance appoints co-founder Yi He as co-CEO — The Block](https://www.theblock.co/post/381196/binance-appoints-co-founder-yi-he-as-co-ceo-alongside-richard-teng)
- [Binance names cofounder Yi He as new co-CEO — Fortune](https://fortune.com/2025/12/03/binance-names-cofounder-yi-he-as-new-co-ceo)
- [Binance presenta solicitud de licencia cripto en Brasil — Cointelegraph](https://cointelegraph.es/news/binance-brazil-crypto-license-oct-30-deadline)
- [Binance pide licencia en Brasil y recorta servicios y tokens — Criptoinforme](https://criptoinforme.com/intercambios/binance-licencia-brasil-servicios-tokens/)
- [Binance en Argentina: regulación — Finantres](https://finantres.com/binance-argentina/)
- [How Bybit didn’t waste a good crisis — CryptoSlate](https://cryptoslate.com/how-bybit-didnt-waste-a-good-crisis/)
- [Who is Ben Zhou — Cointelegraph](https://cointelegraph.com/learn/articles/who-is-ben-zhou)
- [Crypto exchange hack communications: the first 6 hours playbook — DEV Community](https://dev.to/shilika/crypto-exchange-hack-communications-the-first-6-hours-playbook-post-bybit-7d)
