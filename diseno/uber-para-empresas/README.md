# Uber para Empresas · Kit para Claude Design

1. Descomprime el ZIP. Abre `referencia-visual.html` localmente para ver los componentes y reproducir la toma de ejemplo. Puedes revisar la lámina estática en `referencia-visual.png`.
2. En Claude, crea un artefacto de diseño. Si tu cuenta muestra la opción de importar un sistema, carga los archivos del kit que acepte esa opción. Como alternativa, adjunta `referencia-visual.png`, `DESIGN-SYSTEM.md` y `tokens.json` al chat del artefacto. Si el selector rechaza Markdown o JSON, pega el contenido de la guía directamente en el chat. El ZIP sirve para entregar los archivos juntos.
3. Pega el bloque de abajo. Sustituye los campos entre corchetes cuando tengas el brief. Puedes adjuntar `referencia-visual.html` como ejemplo de implementación si el flujo acepta código. La guía contiene enlaces a las referencias públicas.

## Prompt para pegar

> Usa los archivos adjuntos como sistema de diseño audiovisual para un concepto de entrevista de Uber para Empresas México. Aplica DESIGN-SYSTEM.md para dirección visual y tokens.json para tamaños y tiempos. La referencia visual muestra componentes reutilizables. Usa «Uber para Empresas» como firma textual si no adjunto un lockup de marca autorizado.
>
> Mi brief es: objetivo [objetivo]; audiencia [audiencia]; caso de uso [producto]; canal [canal]; formato [16:9, 9:16 o 1:1]; duración [segundos]; acción final [CTA]. Si falta una decisión que afecte la propuesta, pregúntame por el objetivo y la audiencia antes de diseñar. Si solo te pido explorar, presenta tres conceptos distintos y describe qué fricción aborda cada uno.
>
> Entrega un storyboard con tiempos, encuadre, copy en pantalla, voz o sonido, transición y componente usado por escena. Después crea un prototipo editable de los cuadros clave. Si el entorno permite motion, anima una secuencia de muestra aplicando los tokens; si el entregable es estático, anota el movimiento en el storyboard. No inventes resultados, testimonios, interfaces oficiales ni ofertas. Etiqueta las visualizaciones de producto ilustrativas y el concepto de entrevista.
