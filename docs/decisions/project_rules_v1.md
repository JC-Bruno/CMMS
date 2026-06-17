# CMMS Enterprise — Project Rules V1

## 1. Propósito

Este documento define las reglas aprobadas para la V1 del proyecto **CMMS Enterprise**.

Su objetivo es evitar ambigüedad antes de iniciar el desarrollo de backend, frontend, base de datos, permisos, flujos de trabajo, vistas o integraciones.

Estas reglas complementan el documento maestro del proyecto y registran las decisiones tomadas para adaptar el sistema a la operación real de mantenimiento.

---

## 2. Jerarquía de fuentes del proyecto

El proyecto usará la siguiente jerarquía de fuentes:

### Prioridad 1 — Documento maestro funcional y técnico

El archivo maestro `.md` cargado para el proyecto será la fuente principal para:

* Lógica del sistema.
* Permisos.
* Flujos de trabajo.
* Reglas de negocio.
* Arquitectura general.
* Modelo multi-cliente.
* Separación entre solicitudes y órdenes de trabajo.
* Inventario por movimientos.
* Auditoría.
* Seguridad.
* Criterios de aceptación.

Cuando exista contradicción entre documentos, el documento maestro tendrá prioridad para lógica, permisos y flujos.

### Prioridad 2 — Diagramas de flujo

Los diagramas de aplicación se usarán como apoyo para entender:

* Relación entre módulos.
* Flujo correctivo.
* Flujo preventivo.
* Acciones pendientes.
* Árbol técnico.
* Secuencia general de decisiones operativas.

### Prioridad 3 — Prototipo visual generado anteriormente

El código y vistas generadas anteriormente se usarán únicamente como referencia visual aproximada.

Se permite tomar inspiración de:

* Colores.
* Sidebar.
* Topbar.
* Cards.
* Badges.
* Tablas.
* Iconos.
* Distribución de pantallas.
* Estilo visual general.
* Sensación de interfaz profesional.

No se permite tomar de ese prototipo:

* Lógica de negocio.
* Flujos de trabajo.
* Estados.
* Permisos.
* Backend.
* Estructura de datos.
* Acciones de botones.
* Manejo de API.
* Manejo de estado frontend.
* Arquitectura de carpetas.

---

## 3. Nombre del proyecto

El proyecto se llamará:

```text
CMMS Enterprise
```

La carpeta raíz local será:

```text
CMMS Enterprise
```

---

## 4. Repositorio remoto oficial

El repositorio remoto oficial será:

```text
https://github.com/JC-Bruno/CMMS.git
```

No se debe crear otro repositorio sin autorización.

---

## 5. Stack tecnológico aprobado

El stack aprobado para el proyecto es:

```text
Backend: Django + Django REST Framework
Frontend: React + TypeScript + Vite
Base de datos: PostgreSQL 16+
Infraestructura local: Docker Compose
Documentación API: drf-spectacular / OpenAPI
```

No se debe cambiar el stack tecnológico sin análisis y aprobación previa.

---

## 6. Arquitectura multi-cliente

El sistema debe prepararse para arquitectura multi-cliente desde el inicio.

El modelo aprobado será:

```text
cmms_control
cmms_client_<client_code>
```

La base `cmms_control` almacenará información de control como:

* Clientes.
* Bases de datos asociadas.
* Licencias.
* Estado de despliegue.
* Accesos de soporte.
* Auditoría global.

Cada cliente tendrá su propia base de datos operativa.

Ejemplos:

```text
cmms_control
cmms_client_monelca
cmms_client_acme
cmms_client_beta
```

Las tablas operativas de mantenimiento no deben usar `tenant_id`.

La separación principal entre clientes será por base de datos dedicada.

---

## 7. Regla de modularidad y crecimiento futuro

El CMMS debe desarrollarse pensando en crecimiento futuro.

Cada módulo debe construirse como una pieza de rompecabezas que pueda acoplarse a otras piezas sin reescribir archivos completos.

Una funcionalidad estable no debe requerir ser rehacida cuando se agreguen:

* Nuevos módulos.
* Nuevos permisos.
* Nuevos campos.
* Nuevos estados.
* Nuevos flujos.
* Nuevas pantallas.
* Nuevas integraciones.
* Nuevas reglas de negocio.
* Nuevos reportes.

Cuando el sistema necesite crecer, se debe preferir agregar:

* Nuevos servicios.
* Nuevos selectores.
* Nuevos permisos.
* Nuevos modelos relacionados.
* Nuevas transiciones de workflow.
* Nuevos componentes frontend.
* Nuevos hooks.
* Nuevos adapters.
* Nuevos eventos de dominio.
* Nuevas pruebas.

No se deben hacer modificaciones invasivas a piezas estables salvo que exista una razón técnica documentada.

---

## 8. Regla de separación backend

La lógica de negocio no debe vivir en `views.py`.

Cada app Django de negocio debe respetar esta separación:

```text
models.py        -> estructura de datos y relaciones
serializers.py   -> validación de entrada y salida
selectors.py     -> consultas y lectura de datos
services.py      -> reglas de negocio y transacciones
permissions.py   -> validación de permisos
views.py         -> recepción HTTP y delegación
tests/           -> pruebas unitarias, integración y permisos
```

Las acciones críticas deben implementarse mediante servicios.

Ejemplos:

```text
create_maintenance_request()
convert_request_to_work_order()
assign_technician_to_work_order()
start_work_order()
pause_work_order()
resume_work_order()
complete_work_order_technically()
validate_work_order_by_requester()
close_work_order_final()
consume_spare_part_for_work_order()
create_pending_action()
record_audit_event()
```

`views.py` no debe contener lógica de negocio, cálculos operativos, transición de estados, reglas de inventario, reglas de cierre ni reglas de permisos complejas.

---

## 9. Regla de separación frontend

El frontend debe ser modular.

No se debe concentrar la aplicación en un `App.tsx` gigante ni en componentes con lógica mezclada.

La estructura base aprobada será:

```text
frontend/src/
├── app/
├── api/
├── components/
├── modules/
├── permissions/
├── schemas/
├── types/
├── hooks/
└── utils/
```

Cada módulo funcional podrá tener:

```text
pages/
components/
hooks/
schemas/
types/
services/
```

Ejemplo:

```text
frontend/src/modules/work-orders/
├── pages/
├── components/
├── hooks/
├── schemas/
├── types/
└── services/
```

Las pantallas deben consumir datos mediante servicios/hook controlados, no llamar lógica de negocio directamente dentro del componente visual.

---

## 10. Modelo de permisos

El CMMS no debe copiar los puestos de la empresa como reglas rígidas del sistema.

Las acciones se autorizarán por permisos, no por cargos.

Un rol será únicamente un agrupador configurable de permisos.

Un usuario podrá tener:

* Uno o más roles.
* Uno o más permisos.
* Permisos directos adicionales si se requiere.

Ejemplos de permisos iniciales:

```text
REQUEST_CREATE
REQUEST_VIEW
REQUEST_REVIEW
REQUEST_CONVERT_TO_OT
REQUEST_CANCEL
REQUEST_MARK_DUPLICATED

OT_VIEW
OT_ASSIGN_TECHNICIAN
OT_START
OT_PAUSE
OT_RESUME
OT_COMPLETE_TECHNICAL
OT_VALIDATE_REQUESTER
OT_REOPEN
OT_CLOSE_FINAL
OT_CANCEL

ASSET_VIEW
ASSET_CREATE
ASSET_UPDATE
ASSET_DELETE
ASSET_DEACTIVATE

INVENTORY_VIEW
INVENTORY_CONSUME_PART
INVENTORY_ADJUST_STOCK
INVENTORY_RESERVE_PART

AUDIT_VIEW

COST_VIEW
COST_EDIT
REPORT_VIEW
```

Toda acción crítica debe validar permisos en backend.

El frontend puede ocultar botones, pero nunca debe ser la única capa de seguridad.

---

## 11. Regla sobre cargos y roles empresariales

El CMMS debe poder usarse en diferentes industrias y empresas.

Por esa razón, no se crearán reglas internas amarradas a cargos específicos como:

```text
Jefe de mantenimiento
Asistente de mantenimiento
Supervisor de producción
Técnico eléctrico
Técnico mecánico
```

Esos nombres pueden existir como roles configurables por cada cliente, pero la lógica del sistema debe depender de permisos.

Ejemplo:

```text
Rol: Jefe de mantenimiento
Permisos:
- REQUEST_REVIEW
- REQUEST_CONVERT_TO_OT
- OT_ASSIGN_TECHNICIAN
- OT_CLOSE_FINAL
- COST_VIEW
```

Otra empresa podría crear:

```text
Rol: Coordinador técnico
Permisos:
- REQUEST_REVIEW
- OT_ASSIGN_TECHNICIAN
```

El sistema debe soportar ambos casos sin cambiar código.

---

## 12. Reglas V1 para solicitudes correctivas

En V1, toda solicitud correctiva debe estar asociada a un código de activo.

La infraestructura también debe codificarse como activo de infraestructura.

No se permitirá crear una solicitud correctiva sin activo o infraestructura codificada.

Ejemplos:

```text
E-001 | Compresor principal
GR-002 | Grúa puente nave 1
INF-001 | Techo bodega materia prima
INF-002 | Canal aguas lluvias nave producción
INF-003 | Portón acceso sur
```

El formulario de solicitud correctiva debe incluir como mínimo:

```text
Código de activo o infraestructura
Descripción del activo o infraestructura
Descripción de la falla
Prioridad percibida
Solicitante automático
Fecha y hora automática
Check de confirmación de falla
```

El campo de activo debe ser seleccionable desde una lista con búsqueda mientras se escribe.

La descripción de la falla debe permitir escritura manual y quedar preparada para dictado por micrófono en frontend.

---

## 13. Requester y supervisor en V1

En V1, el requester será el usuario que reporta y confirma la falla.

Operativamente, ese requester representa al supervisor o responsable autorizado que confirma la falla antes de registrarla en el CMMS.

Por lo tanto, en V1 no existirá un paso separado de aprobación por supervisor.

El flujo será:

```text
Operador detecta falla
↓
Informa al supervisor o responsable
↓
Requester autorizado confirma la falla
↓
Requester autorizado registra la solicitud en el CMMS
↓
Solicitud entra a mantenimiento
```

En una fase futura se podrá separar el flujo en:

```text
Usuario reporta
↓
Supervisor aprueba
↓
Mantenimiento recibe
```

pero no se implementará así en V1.

---

## 14. Reglas V1 para conversión de solicitud a OT

Una solicitud de mantenimiento no es una orden de trabajo.

La solicitud representa lo que el requester reportó originalmente.

La orden de trabajo representa lo que mantenimiento aceptó, clasificó, asignó, ejecutó, validó y cerró.

Reglas:

* Una solicitud puede convertirse en OT.
* Una solicitud solo puede convertirse en OT una vez.
* La información original del requester no debe modificarse después del envío.
* La conversión debe realizarse mediante un servicio de negocio.
* La conversión debe validar permisos.
* La conversión debe generar auditoría.
* La OT debe conservar vínculo con la solicitud origen.

La conversión solo puede hacerla un usuario con permiso:

```text
REQUEST_CONVERT_TO_OT
```

---

## 15. Reglas V1 para órdenes de trabajo correctivas

En V1, el técnico no necesita aceptar formalmente la OT.

La acción de inicio de OT será suficiente para indicar que el técnico inició la atención.

Flujo simplificado:

```text
OT creada
↓
Técnico asignado
↓
Técnico inicia OT
↓
Técnico registra diagnóstico y trabajo
↓
Técnico finaliza técnicamente
↓
Requester valida
↓
Usuario autorizado cierra definitivamente
```

La OT no puede iniciar si no tiene técnico asignado.

La finalización técnica no equivale al cierre definitivo.

El cierre definitivo solo puede hacerlo un usuario con permiso:

```text
OT_CLOSE_FINAL
```

---

## 16. Información que debe registrar el técnico

Antes de finalizar técnicamente una OT correctiva, el técnico debe registrar:

```text
Diagnóstico de la falla encontrada
Trabajo realizado
Causas probables
Repuestos usados
Evidencia si aplica
Recomendaciones
Acciones pendientes
Insumos necesarios para ejecutar acciones pendientes
```

Si no se usaron repuestos, el sistema debe permitir indicar explícitamente:

```text
No se utilizaron repuestos
```

Las acciones pendientes no deben quedar como texto perdido dentro de observaciones.

Deben registrarse como entidad controlada cuando aplique.

---

## 17. Tiempos de OT

El sistema debe calcular tiempos automáticamente.

Como mínimo debe soportar:

```text
Tiempo técnico:
Inicio de OT -> finalización técnica

Tiempo de ciclo operativo:
Inicio de OT -> validación del requester
```

En fases futuras se podrán agregar otros tiempos:

```text
Tiempo desde reporte hasta recepción
Tiempo desde recepción hasta conversión
Tiempo desde asignación hasta inicio
Tiempo desde finalización técnica hasta validación
Tiempo desde validación hasta cierre final
```

---

## 18. Validación del requester

El requester debe validar el resultado del trabajo.

Opciones mínimas:

```text
Aprobar
Rechazar
Aprobar con observaciones
```

Si el requester rechaza el trabajo, debe registrar motivo obligatorio.

El rechazo debe permitir reabrir la OT o devolverla a mantenimiento según reglas del workflow.

---

## 19. Cierre final de OT

El cierre final debe ser una acción separada de la finalización técnica y de la validación del requester.

Solo podrá cerrar definitivamente un usuario con permiso:

```text
OT_CLOSE_FINAL
```

Al cerrar definitivamente, el sistema debe:

* Registrar auditoría.
* Consolidar historial del activo.
* Bloquear edición operativa.
* Permitir solo correcciones administrativas con permiso especial.
* Preparar datos para indicadores.
* Preparar datos para costos si el usuario tiene permiso.

---

## 20. Regla de prioridad

En V1 se usará la prioridad percibida indicada en la solicitud.

Valores sugeridos:

```text
Baja
Media
Alta
Crítica
```

La prioridad técnica calculada por análisis del activo se implementará más adelante.

El modelo de datos debe quedar preparado para agregar prioridad técnica sin rediseñar el flujo.

---

## 21. Árbol técnico de activos

El sistema debe prepararse desde el inicio para el árbol técnico completo:

```text
Empresa
└── Sede
    └── Nave / Planta / Edificio
        └── Área / Proceso / Línea
            └── Activo / Infraestructura
                └── Sección
                    └── Sistema
                        └── Subsistema
                            └── Componente
                                └── Punto mantenible
```

La carga inicial puede llegar solo hasta el nivel de activo o infraestructura.

Ejemplo inicial válido:

```text
Empresa
└── Planta
    └── Nave
        └── Área
            └── Activo
```

El sistema debe permitir agregar después:

```text
Secciones
Sistemas
Subsistemas
Componentes
Puntos mantenibles
```

sin rediseñar el módulo.

---

## 22. Infraestructura como activo

La infraestructura debe tratarse como activo mantenible.

Ejemplos:

```text
INF-TECHO-001 | Techo bodega principal
INF-DRENAJE-001 | Canal de aguas lluvias nave norte
INF-PORTON-001 | Portón acceso principal
INF-LUMINARIA-001 | Luminaria nave producción
INF-OFICINA-001 | Sistema de ventilación oficina productiva
```

Esto permitirá:

* Historial técnico.
* Reincidencias.
* Costos por infraestructura.
* Preventivos de infraestructura.
* Pendientes asociados.
* Documentos y evidencias.

---

## 23. Inventario

El stock no debe modificarse directamente.

Todo cambio de stock debe pasar por movimientos transaccionales.

Tipos mínimos de movimiento:

```text
Entrada
Salida
Consumo en OT
Devolución
Ajuste
Reserva
```

Cuando se consuma un repuesto en una OT, el sistema debe:

* Validar stock disponible.
* Crear movimiento de inventario.
* Asociar consumo a la OT.
* Actualizar stock.
* Registrar auditoría.
* Evitar stock negativo.

Los costos de repuestos deben estar protegidos por permisos.

---

## 24. Acciones pendientes

Una acción pendiente no es un comentario.

Debe ser una entidad controlada.

Puede originarse por:

* Correctivo con trabajo pendiente.
* Preventivo incompleto.
* Falta de repuesto.
* Hallazgo de inspección.
* Medición fuera de rango.
* Recomendación del técnico.
* Revisión de mantenimiento.
* Análisis de causa raíz.

Toda acción pendiente debe tener como mínimo:

```text
Origen
Activo o infraestructura asociada
Descripción
Motivo
Responsable
Prioridad o criticidad
Fecha objetivo o justificación
Estado
```

Si requiere insumos, debe registrar:

```text
Insumo requerido
Cantidad estimada
Observaciones
```

---

## 25. Auditoría

Toda acción crítica debe generar auditoría.

Ejemplos:

```text
Login/logout
Creación de usuario
Cambio de rol
Cambio de permisos
Creación de activo
Modificación de activo
Desactivación de activo
Creación de solicitud
Conversión de solicitud a OT
Asignación de técnico
Inicio de OT
Pausa de OT
Reanudación de OT
Finalización técnica
Validación del requester
Rechazo del requester
Reapertura de OT
Cierre final
Movimiento de inventario
Exportación de reporte sensible
```

Cada evento de auditoría debe registrar como mínimo:

```text
Usuario
Fecha y hora
Acción
Entidad afectada
Valor anterior si aplica
Valor nuevo si aplica
Comentario si aplica
```

---

## 26. Costos protegidos

Los costos no deben mostrarse si el usuario no tiene permiso.

Esto aplica a:

* API.
* UI.
* Reportes.
* Exportaciones.
* Ficha de activo.
* Detalle de OT.
* Inventario.

Permisos relacionados:

```text
COST_VIEW
COST_EDIT
OT_VIEW_COSTS
REPORT_VIEW_COSTS
```

El frontend no debe renderizar costos si el usuario no tiene permiso.

El backend no debe devolver costos si el usuario no tiene permiso.

---

## 27. UI/UX V1

El diseño visual debe ser sobrio, moderno y funcional.

Se aprueba usar como base visual:

```text
Fondo general: #F8FAFC
Superficie: #FFFFFF
Sidebar / navegación oscura: #0F172A
Primario: #1D4ED8
Texto principal: #111827
Texto secundario: #64748B
Borde: #E2E8F0
Éxito: #16A34A
Advertencia: #D97706
Peligro: #DC2626
Información: #2563EB
```

Reglas visuales:

* Usar color solo con significado funcional.
* No depender solo del color.
* Usar texto, icono y tooltip cuando aplique.
* Mantener labels visibles.
* No sustituir labels con placeholders.
* Usar badges para estados, prioridad y criticidad.
* Mostrar estados loading, empty, error y sin permisos.
* Las acciones críticas deben pedir confirmación.
* La navegación debe depender de permisos.
* El backend debe validar siempre, aunque el frontend oculte acciones.

---

## 28. Ramas Git

Las ramas usarán nombres técnicos en inglés.

Ramas principales:

```text
main
develop
```

Ramas de soporte:

```text
docs/*
feature/*
fix/*
test/*
refactor/*
release/*
```

Ramas iniciales aprobadas:

```text
docs/project-rules-v1
feature/repository-bootstrap
feature/backend-core-foundation
feature/auth-users-roles-permissions
feature/multiclient-control-panel
feature/asset-technical-hierarchy
feature/corrective-maintenance-workflow
feature/preventive-maintenance-workflow
feature/inventory-spares-movements
feature/pending-actions-backlog
feature/reports-kpis-dashboard
feature/frontend-visual-system
release/v1.0.0
```

Flujo general:

```text
feature/*
↓
develop
↓
release/*
↓
main
```

No se debe hacer merge a `main` sin autorización.

---

## 29. Convención de commits

El proyecto usará Conventional Commits.

Formato:

```text
type(scope): message
```

Tipos aceptados:

```text
docs
chore
feat
fix
test
refactor
ci
perf
security
```

Ejemplos:

```text
docs(architecture): define modular architecture principles
docs(project): define CMMS V1 project rules
chore(repo): bootstrap monorepo structure
feat(auth): implement users roles and permissions
feat(assets): implement technical hierarchy base models
feat(work-orders): implement corrective workflow transitions
fix(inventory): prevent direct stock modification
test(work-orders): validate requester approval flow
```

---

## 30. Orden recomendado de implementación

El orden técnico aprobado para iniciar será:

```text
1. Repository bootstrap
2. Backend core foundation
3. Auth, users, roles and permissions
4. Multiclient control panel
5. Asset technical hierarchy
6. Corrective maintenance workflow
7. Preventive maintenance workflow
8. Inventory, spares and movements
9. Pending actions and backlog
10. Reports and KPIs
11. Frontend visual system
```

El primer módulo funcional de negocio será:

```text
Asset technical hierarchy
```

Pero antes deben existir:

```text
Auth, users, roles and permissions
Multiclient control panel
```

porque los activos, solicitudes y OT deben operar dentro de un cliente y bajo permisos.

---

## 31. Definition of Done

Una funcionalidad no se considera terminada si solo “funciona visualmente”.

Debe cumplir como mínimo:

* Modelo definido si aplica.
* Migración creada si aplica.
* Servicio implementado.
* Selector implementado si aplica.
* Serializer validado si aplica.
* Endpoint implementado si aplica.
* Permisos backend aplicados.
* Auditoría aplicada si corresponde.
* Pruebas unitarias.
* Pruebas de integración para flujos críticos.
* Pruebas de permisos.
* Documentación actualizada.
* UI con loading, empty, error y sin permisos si aplica.
* Validaciones frontend y backend si aplica.
* Commit claro.
* Push al repositorio remoto cuando corresponda.

---

## 32. Decisiones futuras pendientes

Quedan pendientes para fases posteriores:

* Separar requester y supervisor como roles funcionales distintos.
* Implementar aprobación previa de supervisor cuando aplique.
* Implementar prioridad técnica por análisis de activo.
* Implementar criticidad formal de activos.
* Implementar cálculo avanzado de salud del activo.
* Implementar integración con correo, Telegram o WhatsApp.
* Implementar integración futura con ERP o sistema externo.
* Implementar análisis causa raíz completo.
* Implementar reportes ejecutivos avanzados.
* Implementar costos completos por activo, OT y repuesto.
* Implementar control avanzado de ventanas de producción.
* Implementar preventivos por condición y mediciones.

---

## 33. Regla final

Antes de programar cualquier funcionalidad, se debe validar:

```text
¿Esta pieza podrá crecer sin obligarnos a rehacerla?
```

Si la respuesta es no, la funcionalidad debe rediseñarse antes de ser implementada.
