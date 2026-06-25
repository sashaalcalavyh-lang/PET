# Playbook de Lanzamiento y Escalamiento: Máquina de Flujo de Caja Veterinaria

Este documento detalla la estrategia para tomar un local veterinario subutilizado y convertirlo en un negocio altamente rentable, aplicando el modelo de **Alex Hormozi ($100M Offers)**. Nuestro objetivo es el flujo de caja positivo, no los "Likes" en redes sociales.

## 0. La Unfair Advantage (El Equipo Fundador)
La fortaleza de esta clínica radica en el triángulo de los socios:
*   **Alfonso (El Capital Inversor):** Inyección de capital y resguardo financiero. Logró negociar **3 meses de gracia** en el arriendo, lo que reduce el estrés de caja inicial a casi cero. A partir del Mes 4, el arriendo subirá a ~$700.000 y la meta al Año 1 es de $1.000.000. Además, luego del primer año, se estructurará el pago de **Retorno de Inversión (ROI) + Porcentaje acordado** sobre el capital inyectado.
*   **Daniela:** Doctora, cirujana y anestesista con experiencia previa como dueña de clínica. Supervisará los protocolos médicos, compras de equipos y reclutamiento del talento (evitando cuellos de botella operativos).
*   **Sasha:** Data Science y Automatizaciones. En lugar de delegar el marketing a ciegas, inyectará sistemas automatizados (n8n/Shopify) y campañas hiper-optimizadas con el apoyo de su pareja especialista, garantizando que cada peso invertido sea medible.

## 1. Autopsia Clínica: Por qué quebró la administración anterior
Los datos históricos (2023-2026) revelan que la clínica no falló por mala suerte, sino por una completa negligencia administrativa y tecnológica. Su fracaso se resume en tres factores estructurales:
*   **El Sangrado de Invierno (Fijos Inflexibles):** La clínica cargaba con un lastre de ~$7.5M mensuales (arriendos sin negociar, nóminas abultadas). Al no tener marketing, el flujo peatonal caía un 50% todos los inviernos (ej. de 195 ventas en Febrero 2026 a solo 89 en Junio), ahogando su caja al operar consistentemente en "rojo".
*   **Cero Control de Inventario y Pricing:** Los reportes de stock y márgenes estaban completamente defectuosos. Perdían dinero con los alimentos para hurones vendiendo bajo costo, y un grosero error de digitación en el POS (alimento de pájaros registrado a más de $300.000 de costo) arruinaba la fiabilidad de sus métricas. Operaban a ciegas.
*   **Falta de Retención y Fidelización:** Ausencia total de seguimiento a pacientes. Confiaban al 100% en el tráfico inercial de la calle, ignorando la minería de su base de datos. Sin un Director Médico ni un Administrador analítico al mando, tomaron decisiones de contratación basadas en falsas percepciones de liquidez.

## 2. Diagnóstico Financiero Realista (La Línea de Flotación)
Olvídate de buscar 400 pacientes el Mes 1. Asumiremos una "Fuga por Transición de Marca" y un escenario **Ajustado (Lean)** para garantizar supervivencia con bajo volumen.

**Costos Fijos Iniciales Sincerados (Mes 1 a 3):**
*   Arriendo: $0 (Periodo de gracia, luego $700.000 al Mes 4)
*   Daniela (Veterinario/Cirujano/Anestesista - Sueldo de Supervivencia) Full-Time: ~$1.200.000
*   1 Técnico Full-Time: ~$600.000
*   Sasha (recepcionMarketing/Data - Sueldo de Supervivencia)Full-Time: ~$800.000
*   Ecosistema Tecnológico e Internet (PMS, POS, n8n, Hosting): ~$140.000
*   Insumos / Inventario Histórico: ~$1.140.000 (Dato real extraído del promedio 2024 de facturas de compras)
*   Suministros Básicos (Luz, Agua): ~$100.000 (Estimación provisional, *Dato Desconocido* en facturas electrónicas)
*   **TOTAL LÍNEA DE FLOTACIÓN:** **~$3.980.000 CLP / mes**

**La Matemática de Supervivencia:**
*   Flujo inercial proyectado (con caída del 30% por marca nueva): **110 pacientes/mes**.
*   Para cubrir los $3.980.000 con 110 pacientes, nuestro ticket debe ser superior a **$36.181 CLP** (sigue siendo menor a los 42k esperados). 
*   Punto de Equilibrio con ticket de $42.000: **95 pacientes/mes**.
*   *Conclusión:* La supervivencia del negocio está asegurada si logramos el Upsell, quitando toda la presión a Daniela.

## 3. Fase 1: Estructuración de la "Oferta Irresistible" (Grand Slam Offer)
El error es competir vendiendo "Consulta General" como un commodity.

### El Lead Magnet (Front-End)
*   **El Gancho:** Auditoría Integral para Perros y Gatos a **$15.000 CLP**. Consulta Especializada de Exóticos a **$25.000 CLP** (Ambos con pago 100% anticipado para agendar).
*   **El Entregable (Valor Tangible):** El cliente recibe un "Scorecard de Longevidad" impreso/PDF (automatizado vía n8n) con nota sobre Peso, Dentadura, Piel, Corazón y Articulaciones, más un Roadmap de 3 pasos.
*   **La Garantía Inversa (Risk Reversal):** *"Si sientes que no te dimos un plan de salud superior al de tu clínica anterior, te devolvemos el 100% de tu dinero"*. (El Scorecard hace que el valor percibido sea tan alto que los reembolsos tenderán a cero).
*   **Inversión Inicial de Marketing:** Presupuesto de **$1.000.000 CLP** el primer mes en Meta Ads para liquidar el CAC.

### El Upsell de Farmacia (El Verdadero Back-End)
*   La data histórica revela que **el Upsell promedio es de $26.988 CLP**.
*   Apenas termine la "Auditoría", el paciente NO se va con una receta de papel. Pasa directo a nuestra farmacia interna donde se le ofrecen exámenes de sangre en 15 min y entrega de medicamentos empaquetados.
*   **LTV Esperado Inicial:** $15.000 (Consulta) + $27.000 (Upsell) = **$42.000 CLP**. 
*   *Facturación proyectada (110 pacientes): $4.620.000 CLP (Margen positivo desde el Día 1).*

## 4. Fase 2: Automatización y Eliminación de Fricción (El Stack Tecnológico)
*   **Stack Elegido:** Se descartó Dodozooft por su rigidez. Sasha liderará el armado de un ecosistema ágil conectando **Shopify** (Pagos) + **n8n** (Automatizaciones) + **CRM Customizado** para la ficha clínica (aprovechando sus conocimientos técnicos).
*   **Cero No-Shows:** Shopify cobra los $15.000/$25.000 al momento de agendar. Si no asisten, el dinero ya está en la cuenta.
*   **Reactivación Automática (El Puente de los 421):** Para asegurar los 110 pacientes el primer mes, atacaremos la base histórica de **421 contactos** vía WhatsApp/Mailing con la campaña "Te Extrañamos" ofreciendo la Auditoría, absorbiendo así el shock inicial de la transición de marca.

## 5. Táctica Estacional: Sobreviviendo a Septiembre
La base de datos revela que Septiembre es el peor mes históricamente (caída del 35% de ingresos).
*   **La Estrategia Hormozi:** Durante los feriados (semana del 18 de Septiembre), no cerraremos ni abriremos para consultas de bajo valor. Se activará el modelo **"Turnos de Urgencia Premium"**.
*   **Ejecución:** Se atiende a puertas cerradas. El ticket mínimo de urgencia sube a un multiplicador 2x o 3x (Ej. $45.000 Base). Las personas pagan precios irracionales cuando su mascota se intoxica con asado en Fiestas Patrias. Alto ticket, bajo volumen, misma facturación.

## 6. Frenando el Balde Agujereado: MRR desde el Día 1
La antigua clínica perdía al 73.8% de sus clientes tras la primera visita. Para evitar esto, no podemos esperar al "mes 4" para vender suscripciones.
*   **El Club de Protección Continua:** Ofrecido en la *misma primera visita* como Upsell. Suscripción de ~$6.990 - $9.990/mes.
*   **El Valor:** La clínica se encarga de administrar o enviar la dosis exacta de **Desparasitación Interna y Externa** mensual/trimestral, quitándole la carga mental al dueño.
*   **El Bono de Retención:** Si completan 12 meses, la Vacuna Anual va 100% gratis.
*   **Objetivo:** Crear Flujo de Caja Predecible (MRR) que cubra los costos fijos (incluido el arriendo de $700k en el Mes 4) de manera automática.
