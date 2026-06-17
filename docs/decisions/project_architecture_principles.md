# Principios de arquitectura del CMMS

## 1. Diseño modular y extensible

El CMMS debe construirse como un sistema de piezas acoplables.

Cada módulo debe poder crecer sin reescribir archivos completos ni romper funcionalidades existentes.

## 2. Separación de responsabilidades

La lógica de negocio no debe vivir en vistas HTTP ni en componentes visuales.

Backend:
- models.py define datos.
- serializers.py valida entrada y salida.
- selectors.py concentra consultas.
- services.py ejecuta reglas de negocio.
- permissions.py valida permisos.
- views.py recibe HTTP y delega.

Frontend:
- pages organizan pantallas.
- components renderizan UI.
- hooks manejan estado de consulta.
- schemas validan formularios.
- api centraliza comunicación.
- permissions controla visibilidad.

## 3. Extender antes que reescribir

Cuando el sistema necesite nuevas funciones, se debe preferir:
- agregar nuevos servicios;
- agregar nuevos modelos relacionados;
- agregar nuevas transiciones;
- agregar nuevos permisos;
- agregar nuevos componentes;
- agregar nuevos adapters;
- agregar nuevos eventos.

No se debe modificar de forma invasiva una pieza estable salvo que exista una razón técnica documentada.

## 4. Reglas de negocio centralizadas

Toda acción crítica debe pasar por un servicio de dominio.

Ejemplos:
- convertir solicitud en OT;
- asignar técnico;
- iniciar OT;
- finalizar técnicamente;
- validar por requester;
- cerrar definitivamente;
- consumir repuesto;
- crear acción pendiente.

## 5. Permisos desacoplados de puestos

El sistema no debe codificar puestos de una empresa como reglas fijas.

Las acciones se autorizan por permisos.
Los roles son agrupadores configurables de permisos.

## 6. Preparación para crecimiento

Desde V1 se debe preparar la base para:
- árbol técnico completo;
- acciones pendientes;
- inventario por movimientos;
- auditoría;
- costos protegidos;
- notificaciones por eventos;
- multi-cliente;
- reportes;
- preventivos por componente y punto mantenible.