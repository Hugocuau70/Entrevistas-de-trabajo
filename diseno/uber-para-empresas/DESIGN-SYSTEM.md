# Uber para Empresas · Sistema de diseño para entrevista

México · Kit de entrevista · Deck ejecutivo, piezas audiovisuales, storyboards y prototipos.

La identidad se basa en los recursos publicados por Uber para Empresas México, la guía de Base y la captura de campaña compartida. Las reglas de encuadre y movimiento son propuestas para el caso.

## Preparación del caso y presentación ejecutiva

Usa [BUSINESS-CASE.md](BUSINESS-CASE.md) para armar y revisar cualquier entregable de entrevista. Ahí están el alcance de México, la estructura y el idioma del panel, los tres bloques evaluados, las reglas de Gross Bookings y el modelo de cuenta y portafolio.

Usa la firma **Uber for Business** en el deck en inglés y aplica la escala de Uber Move a títulos y datos clave. En el forecast, usa negro y blanco para lectura, con menta como acento para destacar cuota, brecha o un hito. Mantén a la vista el periodo, la unidad y si cada dato es un supuesto o un forecast. Los ejemplos audiovisuales de esta guía sirven como referencia visual.

## Identidad y firmas de marca

| Recurso | Archivo | Aplicación |
| --- | --- | --- |
| Uber para Empresas, firma apilada blanca | [SVG en español](assets/uber-para-empresas-blanco.svg) | Versión principal de este kit para cierre, portada y fondos negros. |
| Uber for Business, firma apilada blanca | [SVG en inglés](assets/uber-for-business-blanco.svg) | Variante de la captura y opción cuando el brief pide inglés. |
| Demostración en negro | [Muestrario HTML](referencia-visual.html#identidad) | Prueba de contraste con filtro CSS. Para producción sobre fondo claro, usa el archivo aprobado por el equipo de marca. |

La unidad de marca es la **firma tipográfica apilada**. Conserva el archivo en bloque y su proporción aproximada de **3.1:1**. Los pictogramas de producto viven fuera de la firma. Aplica una sola versión lingüística por pieza.

Para este prototipo, reserva alrededor de la firma un margen mínimo igual a **¼ de su altura** y pruébala desde **120 px de ancho** en web. Estos son valores de implementación del kit. Para video, parte de un ancho de **288 px en un lienzo de 1920 × 1080** y valida el cierre en reproducción móvil.

## Tipografía y acceso a archivos

| Rol | Familia y peso | Tamaño / interlínea |
| --- | --- | --- |
| Titular principal | Uber Move Bold · 700 | 36/44 móvil · 44/52 mediano · 52/64 amplio |
| Encabezado | Uber Move Bold · 700 | 28/36 móvil · 32/40 mediano · 36/44 amplio |
| Título de beneficio | Uber Move Text Medium · 500 | 18/24 |
| Cuerpo | Uber Move Text Regular · 400 | 16/24 |
| CTA | Uber Move Text Medium · 500 | 16/20 |
| Legal | Uber Move Text Regular · 400 | 14/20 |

El HTML carga los archivos WOFF2 que publica Uber. Para uso offline, el CSS también reconoce las fuentes instaladas con el nombre correspondiente. Para software de diseño o edición, obtén tu copia de escritorio en el portal de marca de Uber y usa el formato que requiera tu aplicación. La previsualización PDF o PNG que se genere a partir del HTML debe renderizarse con la fuente cargada.

- [Uber Move Bold · WOFF2 de Uber](https://tb-static.uber.com/prod/uber-static/UberMove-Bold.woff2)
- [Uber Move Text Regular · WOFF2 de Uber](https://tb-static.uber.com/prod/uber-static/UberMoveText-Regular.woff2)
- [Uber Move Text Medium · WOFF2 de Uber](https://tb-static.uber.com/prod/uber-static/UberMoveText-Medium.woff2)
- [Tipografía oficial de Base](https://base.uber.com/6d2425e9f/p/976582-typography/b/98142c)
- [Portal de marca de Uber](https://brand.uber.com/)

## Color

| Token | Valor | Aplicación | Origen |
| --- | --- | --- | --- |
| Negro | `#000000` | Firma sobre negro, texto y cierre | Referencias web y captura |
| Blanco | `#FFFFFF` | Fondo y texto invertido | Referencias web y captura |
| Acción oscura | `#121212` | CTA de alto contraste | Captura |
| Acción clara | `#F5F5F5` | CTA secundario sobre fondo oscuro | Captura |
| Fondo menta | `#EAFAEB` | Franja contextual | Captura |
| Acción menta | `#A4D9C3` | CTA de la franja | Captura |
| Carbón | `#232B32` | Campo dominante del hero | Captura |
| Gris del hero | `#454A50` | Plano secundario del hero | Captura |

Usa texto negro sobre blanco o menta. En carbón y gris del hero, usa blanco y verifica el contraste sobre el plano más claro cuando haya fotografía. Reserva el menta para una llamada contextual. El color de la captura se mide en píxeles planos.

## Íconos y fotografía

| Rol | Recursos reutilizables | Tamaño de partida |
| --- | --- | --- |
| Pictogramas de beneficio | [Costos](assets/icono-costes.svg) · [Vehículos](assets/icono-viajes.svg) · [Monitoreo](assets/icono-panel.svg) · [Calendario](assets/icono-calendario.png) | 48 × 48 px |
| Íconos de navegación y orientación | [Casos de uso](assets/icono-programas.svg) · [Industrias](assets/icono-industria.svg) · [Soporte](assets/icono-soporte.svg) | 24 × 24 px |
| Imagen editorial de movilidad | [Fotografía publicada para Uber Central](assets/fotografia-central.jpg) | Recorte de referencia 3:2 |

Los pictogramas del kit proceden de las páginas públicas de Uber. La captura aporta el patrón de tres beneficios con un pictograma sobre cada título. La selección incluida ilustra los casos de uso con recursos verificables de las páginas públicas actuales. Mantén el estilo consistente en cada fila. Cuando el rótulo ya describe el concepto, deja el ícono decorativo fuera del nombre accesible. Usa fotografías que muestren a la persona, el vehículo y la acción en relación entre sí. Conserva el rostro y la puerta visibles en recortes verticales.

## Componentes

| Componente | Especificación | Uso |
| --- | --- | --- |
| Franja contextual | Superficie menta, título 18/24, nota legal 14/20, acción menta de 48 px en forma de píldora | Información temporal con condiciones visibles. |
| Bloque principal | Titular 52/64 y cuerpo 16/24 en escritorio, fondo carbón y acciones de 48 px | Presenta la promesa, un apoyo y hasta dos rutas. |
| CTA | Texto 16/20, alto mínimo 48 px, relleno horizontal 24 px, radio 8 px | Oscuro sobre claro, claro sobre oscuro y menta para campaña. |
| Trío de beneficios | Ícono 48 px, título 18/24, cuerpo 16/24, separación base 16 px | En escritorio, tres columnas. En móvil, apiladas. |
| Cierre audiovisual | Firma blanca sobre negro, beneficio y un CTA por pieza | Mantén la firma y el CTA legibles durante dos segundos como punto de partida. |

La muestra HTML aplica anchos de contenido de hasta 1152 px y puntos de quiebre en 600 y 1136 px. La versión estática está en [referencia-visual.png](referencia-visual.png).

## Aplicación al caso audiovisual

| Tiempo | Imagen | Mensaje |
| --- | --- | --- |
| 0–3 s | Plano de acceso o recepción. Inserto de una persona que espera el traslado. | ¿Cómo organizas los viajes de tus invitados? |
| 3–8 s | Corte entre recepción y vehículo. Pictograma de calendario como apoyo. | Programa el traslado desde un solo lugar. |
| 8–12 s | Composición de ejemplo con estado del viaje. Rotula cualquier pantalla conceptual como «Visualización ilustrativa». | Consulta el estado del traslado. |
| 12–15 s | Placa negra, firma y CTA. | Conoce Uber Central. |

Para adaptar a 9:16, centra la acción dentro del tercio medio y coloca los rótulos en una zona que siga siendo legible con los controles de la plataforma. Para 1:1, reduce el texto antes de reducir el tamaño. Los tiempos de transición, fotogramas y cierre en [tokens.json](tokens.json) son valores de partida para el storyboard. Si el brief requiere cifras, testimonios u ofertas, agrega el respaldo, mercado y vigencia antes de incorporarlos al guion.

## Fuentes de los recursos

- [Uber Central México](https://www.uber.com/mx/es/business/products/central/) · Firma española, pictogramas vectoriales, íconos de navegación y fotografía.
- [Uber Central EE. UU.](https://www.uber.com/us/en/business/products/central/) · Firma inglesa.
- [Uber para Empresas México](https://www.uber.com/mx/es/business/) · Pictograma de calendario para viajes de cortesía y posicionamiento del producto.
- [Base, lenguaje de diseño](https://base.uber.com/6d2425e9f/v/0/p/76be65-design-language) · Familias y funciones del sistema visual.
- Captura compartida para el caso, 1279 × 934 px · Paleta de campaña, disposición de la franja, acciones y fila de beneficios.
- [Inventario de archivos y procedencia](assets/FUENTES.md).
