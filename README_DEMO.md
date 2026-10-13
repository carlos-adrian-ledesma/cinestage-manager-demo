# CineStage Manager — Edición DEMO

**Versión:** 2.0.0-rc1 · **Uso:** evaluación comercial sin vencimiento.

La DEMO se distribuye separada del código FULL. Incluye información ficticia y funcionalidades representativas: dashboard con calendario real, consulta y edición de clientes, producciones, guiones (fichas), elenco, agenda y movimientos financieros de muestra.

## Cómo ejecutar
En Windows con Python 3.11+ instalado: `run_demo_windows.bat`.
También: `python demo_launcher.py` desde la carpeta del paquete.

La DEMO requiere solamente la biblioteca estándar Python (Tkinter incluido en la instalación habitual). No necesita Internet ni cuentas.

La base se genera automáticamente bajo `Documentos/CineStageManager_DEMO/demonstracion.db`. Podés borrar y regenerar los ejemplos mediante **Restablecer demostración**.

## Límites de evaluación
5 producciones, 10 clientes, 3 fichas de guion, 15 integrantes, 20 actividades y 15 movimientos financieros. Exportaciones reales y restauración de respaldos privados no se ofrecen.

Importante: el editor completo de guiones, los informes PDF/DOCX/XLSX, los asientos teatrales y multimedia se muestran en la edición PRIVATE, **no** en esta DEMO simplificada. La DEMO utiliza su propia interfaz evaluativa, manteniendo componentes comunes de calendario y estilo visual.

El código Python de la DEMO distribuido sin compilar es accesible al destinatario; los límites no constituyen DRM fuerte. Para distribución comercial habitual compilar `demo_launcher.py` en Windows y revisar términos de terceros.

## Inicio y diagnóstico V2.0.2
La DEMO muestra una alerta si falla su apertura y registra detalles en `%TEMP%\CineStageManager_DEMO\inicio_error.log`.
