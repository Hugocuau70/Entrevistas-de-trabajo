# Modelo para construir juntos

Datos del caso: cuota H1 = USD 350,000; viaje = USD 10; pedido Eats = USD 15. Estos son supuestos proporcionados, no tarifas locales verificadas.

## Una cuenta, mes por mes
- Separar empleados totales, población elegible, usuarios activos y frecuencia.
- Viajes del mes = elegibles Travel × adopción del mes × viajes de ida por usuario activo.
- Pedidos del mes = elegibles Eats × adopción del mes × pedidos por usuario activo.
- GB del mes = viajes × 10 + pedidos × 15.
- GB H1 = suma de enero a junio; antes de la activación, consumo = 0.
- Si hay servicio parcial en un mes, ajustar solo la parte del mes activa sin duplicar el ajuste en la frecuencia.
- Contar trayectos de ida y vuelta como dos viajes. Un pedido grupal no equivale a un pedido por comensal.
- Si se usa estacionalidad, explicar si afecta población o frecuencia, sin contar el mismo efecto dos veces.
- Separar potencial total, gasto capturable y consumo esperado. No suponer captura del 100%.

## Portafolio
Agrupar cuentas por caso de uso y mes probable de cierre. Para cada cohorte: oportunidades × probabilidad de cierre × GB H1 por cuenta si cierra en ese mes, incluyendo activación y adopción.

No mezclar pipeline expresado en valor anual con cuota semestral consumida. Una cobertura de pipeline no sustituye el cálculo por cohortes. Explicar el denominador de la tasa de cierre: oportunidades calificadas, no toda la lista de 150 cuentas.

Escenarios que Diego debe escoger y defender: conservador, base y favorable. Cambiar pocos supuestos relevantes: cierres, retraso de activación, adopción y frecuencia. Evitar ajustar números solo para llegar a la cuota.

Prueba de coherencia sin propuesta comercial: toda la cuota en Travel requeriría 35,000 viajes; toda en Eats requeriría aproximadamente 23,334 pedidos. Son extremos matemáticos, no recomendaciones.
