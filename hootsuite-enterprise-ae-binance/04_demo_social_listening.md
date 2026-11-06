# 04 · Demo de social listening — Binance (10 min)

> Herramienta: **Lumen by Talkwalker** y el **Lumen agent** dentro de **Wisdom**. Con el free trial tendrás Wisdom y al menos Quick Search de 7 días: para Binance alcanza perfecto, porque la crisis está dentro de esa ventana (si la entrevista es después del ~5 nov, el pico del 29 oct puede quedar fuera de los 7 días → di "in Lumen Enterprise you'd see the full history since October 29" y enséñalo con screenshots tomados ANTES).
>
> **Toma los screenshots cuanto antes**, mientras el pico sigue dentro de la ventana de datos. Cancela el trial al terminar el proceso.

## Queries (copiar/pegar; ajusta la sintaxis si la herramienta lo pide)

**1. Pulso de marca en LATAM (ES/PT)**
```
("Binance" OR "#Binance" OR "hackeo Binance" OR "hack da Binance" OR "Binance hackeada" OR "Binance hack")
```
Filtra por idioma **español** y **portugués** (y/o país: Brasil, México, Argentina).

**2. Radar de estafas**
```
("Binance") AND ("compensación" OR "compensação" OR "reembolso" OR "indemnización" OR "indenização"
OR "soporte" OR "suporte" OR "frase semilla" OR "frase de recuperação" OR "seed phrase"
OR "retiro prioritario" OR "saque prioritário" OR "airdrop" OR "recuperar fondos" OR "recuperar fundos")
```

**3. Rumores y miedo (para "rebuild trust")**
```
("Binance") AND ("quiebra" OR "falência" OR "congelaron" OR "congelou" OR "no puedo retirar" OR "não consigo sacar"
OR "es seguro" OR "é seguro" OR "FTX")
```
(El "FTX" es clave: la comparación con FTX es el miedo número uno; enséñalo como tema a contrarrestar.)

**4. Share of voice / sentimiento vs competencia**
```
"Binance"  vs  "Coinbase"  vs  "OKX"  vs  "Bybit"  vs  "Bitso"  vs  "Mercado Bitcoin"
```

## Guion minuto a minuto
| Min | Qué muestras | Qué dices (EN) |
|---|---|---|
| 0:00-0:45 | Inicio | "Let's look at Binance's real conversation in Spanish and Portuguese. Same story as the deck: protect users, rebuild trust, and then we ask Wisdom what to do." |
| 0:45-2:30 | **Query 1**: volumen (pico del 29 oct), sentimiento, temas | "Here's the spike on October 29 and the reopening on November 1. Notice the split by language — Portuguese and Spanish conversations don't peak at the same time, and they don't worry about the same things." → señala un tema real. |
| 2:30-4:30 | **Query 2**: posts/cuentas de estafa, autores, redes; imágenes con logo si está disponible | "This is the scam radar. 'Compensação', 'reembolso', 'seed phrase'. These are the posts that turn a security incident into victims. In Lumen we'd turn this into an alert, so Security and Comms see a new fake support account in minutes — not when a victim DMs you." |
| 4:30-6:00 | **Query 3**: rumores, comparación con FTX | "And here's the fear: 'is Binance going bankrupt?', comparisons with FTX. This is exactly where the 98%-replenished story needs to land. Each of these rumors is a message your team should answer — by country." |
| 6:00-7:30 | **Query 4**: share of voice y sentimiento vs. competidores | "Competitors are part of the conversation too. This is the share-of-voice and sentiment view I'd bring to your LATAM leadership every week until things normalize." |
| 7:30-9:15 | **Wisdom** | Prompt abajo. "Notice it cites the posts behind its answer — so your team can verify before acting." |
| 9:15-10:00 | Cierre | "In ten minutes: a scam we'd escalate, the rumor to answer, a competitive view and a recommended next step — in Spanish and Portuguese. **What would you want to monitor first?**" |

### Prompts para Wisdom
1. `What are the top rumors and concerns about the Binance hack among Portuguese-speaking users in Brazil this week? What should Binance tell users?`
2. `Summarize scam and impersonation signals mentioning Binance in Spanish and Portuguese over the last 7 days.`
3. `How did sentiment about Binance change after withdrawals reopened on November 1?`
4. En español: `¿Qué dicen los usuarios en México sobre el hackeo de Binance y qué mensaje recomiendas publicar hoy?`

## Cuidados específicos de este caso
- **No hagas clic en links de estafas** durante la demo (ni para "mostrar"). Muestra el post, no el destino.
- Si sale contenido ofensivo o muy negativo: *"This is exactly the noise your team is dealing with; let me filter to what's actionable."*
- No afirmes que un post es de Corea del Norte ni nada técnico; quédate en lo que la herramienta muestra.
- **Plan B / C:** el anexo del deck ya trae tus 5 screenshots de Lumen (Key Metrics, Sentimiento, Temáticas, Resultados, Influencers) con los hallazgos. Si la demo en vivo falla, recórrelos en ese orden: es la misma historia.

## Hallazgos de tus screenshots (30 oct – 6 nov, query "binance")
- **1.3M resultados** (+102%), **8.1M interacciones**, alcance potencial 178.8B; pico el 30 oct (~470K en un día; 32K en una sola hora el viernes).
- **Sentimiento:** 35.8% negativo · 51.5% neutral · 12.7% positivo. Temas negativos: magnitud del robo, atribución a Corea del Norte, miedo sistémico (CZ: "banks are in a worse position"). **Ningún tema positivo detectado** → el 98% repuesto no está generando conversación positiva.
- **Temáticas:** hack, crypto, billion, North Korea, funds, security. binance.com compartido 2.4K veces vs. 91.2K links de X; #Binance 12.9K posts (+106%).
- **Resultados por engagement:** Al Jazeera (73.4K), **Chumel Torres** (MX, 48.5K, negativo), Watcher.Guru (48.1K), **g1 Globo** (BR). Ningún post top es de Binance.
- **Canales y autores:** X = 1.2M de 1.3M resultados (~92%); 137.3K autores; los "autores" con más volumen son agregadores automáticos (thebittimes.com) → hay que filtrar ruido.
