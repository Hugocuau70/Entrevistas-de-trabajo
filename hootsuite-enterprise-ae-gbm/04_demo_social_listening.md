# 04 · Demo de social listening (10 min)

> El assignment pide *"a 10 min demonstration of our social listening tool"*. En 2026 eso es **Lumen by Talkwalker** (y el **Lumen agent** dentro de **Wisdom**). Con un **free trial** de Hootsuite tendrás Wisdom y, como mínimo, listening básico (Quick Search de 7 días); el Lumen completo (historial largo, virality maps, alertas avanzadas) suele ser Enterprise. **Practica en el trial y prepara screenshots de respaldo.**
>
> Regla de la demo: **cuenta una historia, no hagas un tour.** La historia es la misma del deck: confianza → activación → competencia → acción.

## Preparación (día antes)

1. Crea el trial en hootsuite.com con tu correo. Conecta (si quieres) una cuenta tuya de prueba; para listening no necesitas conectar las redes de GBM.
2. Prueba las queries de abajo en Quick Search / Lumen y en Wisdom. Anota qué sale de verdad (temas, picos, ejemplos de posts).
3. Toma **screenshots** de cada paso → pégalos en 4 slides ocultas al final del deck o tenlas en una carpeta. Si el trial no muestra algo, presentas con screenshots y lo dices con naturalidad: *"In the trial I only have 7 days of data — in Lumen Enterprise you'd see the full history."*
4. Ten las queries copiadas en un bloc de notas para pegarlas rápido (escribir en vivo es lento y propenso a errores).
5. Al terminar el proceso: **cancela/downgradea el trial** (lo pide el assignment).

## Queries booleanas (copiar/pegar)

> La sintaxis exacta puede variar (Lumen usa booleanos tipo Talkwalker: `AND`, `OR`, `NOT`, comillas, paréntesis). Ajusta si la herramienta marca error.

**1. Marca GBM (limpia de ruido)** — "GBM" también es *glioblastoma multiforme* (tumor cerebral) y otras cosas; mostrar que filtras eso es un gran momento de demo.
```
("GBM" OR "GBM+" OR "Grupo Bursátil Mexicano" OR "GBM Advisors" OR "fondo GBM" OR "@GBMmx")
AND NOT ("glioblastoma" OR "tumor" OR "cáncer" OR "cancer" OR "brain")
```

**2. Radar de riesgo / fraude**
```
("GBM" OR "Grupo Bursátil Mexicano") AND ("estafa" OR "fraude" OR "perfil falso" OR "me robaron"
OR "no puedo retirar" OR "rendimiento garantizado" OR "duplica tu dinero" OR "asesor por WhatsApp")
```

**3. Activación / dudas de inversionistas nuevos (Mercado Pago)**
```
("GBM" OR "fondo GBM") AND ("Mercado Pago") AND ("rendimiento" OR "tasa" OR "seguro" OR "bajó" OR "cómo invierto" OR "qué es")
```

**4. Competencia (share of voice)** — crea un tema/proyecto por marca:
```
"GBM"            vs   "Nu México" OR "Cajitas Nu"
"Bitso"          vs   "Mercado Pago rendimientos"
"Hey Banco"      vs   "Kuspit" OR "Flink"
```

## Guion minuto a minuto

| Min | Qué muestras | Qué dices (EN) |
|---|---|---|
| 0:00-0:45 | Pantalla de inicio de Lumen / Wisdom | "Let's look at GBM's real conversation. I'll follow the same story as the deck: trust, activation, competition — and then we'll ask Wisdom what to do about it." |
| 0:45-2:30 | **Query 1** · volumen, sentimiento, temas principales. Enseña el `NOT glioblastoma` | "First, a clean picture of the brand. Notice I'm excluding 'glioblastoma' — in medicine GBM is a brain tumor, and without this filter a third of your 'mentions' would be noise. Clean data is the difference between insight and guesswork. Here's volume, net sentiment and the top themes this week." → señala 1 tema real que veas. |
| 2:30-4:30 | **Query 2** · picos, fuentes, autores, posts ejemplo; si existe: reconocimiento de imagen/logo | "Now the risk radar. This is what keeps your Director of Social up at night. We look for GBM next to words like 'estafa', 'perfil falso', 'no puedo retirar'. We can see where it's happening — which network, which accounts — and who's amplifying it. In Lumen Enterprise, image recognition also catches your **logo** inside scam ads, even when the text never says 'GBM'. And we'd set an **alert** so Security and Comms hear about a spike in minutes." |
| 4:30-6:00 | **Query 3** · temas y preguntas recurrentes | "Third, activation. Here's what first-time investors coming from Mercado Pago are actually asking. Every one of these questions is a piece of content GBM should publish — and a reply template for Care in Nest. This is how listening turns into activation, not just reporting." |
| 6:00-7:30 | **Query 4** · share of voice y sentimiento vs. Nu, Bitso, Mercado Pago | "Fourth, competition. Share of voice and sentiment versus Nu, Bitso and Mercado Pago in the 'investing for beginners' conversation. This is the metric I'd bring to your CMO every month." |
| 7:30-9:15 | **Wisdom** (Lumen agent) — escribe el prompt | "Finally, the part your team will love. Instead of building a report, they just ask." → prompts abajo. Lee la respuesta en voz alta, resalta las **citas** a posts reales: "Notice it cites its sources — so you can trust and verify before you act." |
| 9:15-10:00 | Cierre | "So in ten minutes we went from raw conversation to: a risk we'd escalate, content ideas to activate investors, a competitive benchmark, and a recommended next step. Imagine your team getting this every morning instead of a monthly agency report. **What would you want to monitor first?**" |

### Prompts para Wisdom (elige 1-2)
1. `Summarize the main conversation themes about GBM in Mexico over the last 7 days, including sentiment and any risk signals.`
2. `Why did negative sentiment about GBM change this week, and what should my social team do in the next 48 hours?`
3. `What are the most common questions first-time investors ask about GBM and Mercado Pago? Suggest 5 educational post ideas.`
4. `Compare GBM's share of voice and sentiment against Nu México and Bitso this week.`

(Puedes escribirlos en español también — muestra que funciona en ambos idiomas: *"¿Cuáles son las principales quejas sobre GBM esta semana y qué recomiendas hacer?"*)

## Plan B / C

- **Plan B (trial limitado):** usa Quick Search de 7 días + Wisdom, y muestra las capacidades Enterprise con screenshots: *"This is what you'd see in Lumen Enterprise."*
- **Plan C (todo falla: internet, login):** quédate en la slide "Let’s listen" y recorre tus screenshots (las notas de esa slide tienen los 5 pasos). Di: *"Live demos have a mind of their own — let me walk you through what I prepared."* Mantén la calma; evalúan cómo comunicas, no el Wi-Fi.
- Si aparece un resultado vergonzoso o irrelevante en vivo: *"That's actually a good example of why we refine queries — let me exclude that."* → convierte el problema en demostración.

## Qué evitar
- Hacer clic en todo el menú. Máximo 4 vistas.
- Leer métricas sin decir "so what" para GBM.
- Prometer features que no viste en la herramienta.
- Pasarte de 10 min.
