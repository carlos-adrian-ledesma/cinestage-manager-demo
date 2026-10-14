# CineStage Manager — Guía de la DEMO

**Versión actual:** 2.1.0-RC1 · **Estado:** demostración pública / evaluación.

Esta edición permite explorar una muestra funcional de CineStage Manager utilizando datos ficticios y una base SQLite independiente de PRIVATE/FULL.

## Requisitos y ejecución

- Windows con Python 3.11 o superior y Tkinter.
- Ejecutar `INSTALAR_DEMO.bat` para inicializar el entorno.
- Abrir `run_demo_windows.bat`.
- Si no abre, ejecutar `run_demo_debug_windows.bat`.
- Alternativamente: `python demo_launcher.py`.

El sistema guarda sus datos ficticios en `Documentos/CineStageManager_DEMO/` y permite restablecerlos desde la aplicación.

## Funciones disponibles

Dashboard, calendario mensual, producciones, clientes, fichas básicas de guiones, elenco/equipo, agenda y registros financieros de muestra.

Los límites actuales son: 5 producciones, 10 clientes, 3 fichas de guion, 15 integrantes, 20 actividades y 15 movimientos financieros.

## Funciones exclusivas de FULL

La edición privada incluye funcionalidades no disponibles en esta DEMO simplificada, como editor completo de guiones, multimedia, gestión teatral de asientos, respaldos y exportaciones avanzadas.

La versión DEMO no contiene la carpeta `app/` ni el código fuente PRIVATE/FULL.

## Alcance y seguridad

- Todos los datos iniciales son ficticios.
- No se requieren credenciales ni acceso a Internet.
- La edición DEMO distribuye su código Python necesario para funcionar; no constituye una protección anticopia invulnerable.
- No introducir datos personales reales durante una evaluación pública.

## Estado de validación

La versión se identifica como RC1 (release candidate). Las pruebas finales de instalación, escalado y distribución en Windows deben documentarse antes de una publicación comercial definitiva.

Revisar `LICENSE_DEMO.txt` y `THIRD_PARTY_NOTICES.txt` antes de distribuir como producto final.
