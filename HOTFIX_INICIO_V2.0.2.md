# CineStage Manager 2.0.2 — HOTFIX de inicio

## Problema confirmado
Al crear el menú artístico en la versión 2.0.1 se utilizó `tk.Frame(..., pady=(6, 4))`.
En Tkinter el padding del propio Frame debe ser un número (no una tupla):
`_tkinter.TclError: bad screen distance "6 4"`.
El lanzador `pythonw.exe` ocultaba el traceback, por eso se cerraba CMD sin ventana visible.

## Soluciones
- En `demo/demo_runtime.py (sin cambios funcionales)`, `pady=4` y navegación compacta. El sidebar ya no tiene barra vertical.
- Arranque con registro persistente: `%TEMP%/CineStageManager_DEMO/inicio_error.log`.
- Si falla el inicio mediante `pythonw.exe` en Windows, aparece una alerta con el motivo y ruta del registro.
- Acceso directo al Pythonw del entorno virtual, sin paso por ventanas CMD.
- Nuevos `REPARAR_ACCESO_DIRECTO.bat` y `VERIFICAR_INICIO_GUI.bat`.
- DEMO: diagnóstico de inicio y acceso directo propio.

## Actualizar sin perder datos
1. Cerrar CineStage Manager.
2. Descomprimir el paquete nuevo en una carpeta nueva (no reutilizar el ZIP antiguo).
3. Ejecutar `install_windows.bat` y al finalizar usar el acceso directo.
4. Los datos se mantienen en Documentos/CineStageManager, separados del código; no borrar esas carpetas.
5. Si sigue sin abrir, ejecutar `run_debug_windows.bat` o `VERIFICAR_INICIO_GUI.bat`.

## Validación
Prueba de arranque gráfico en display virtual, navegación de 14 módulos, navegación del calendario y suite de tests automatizados.
La verificación real en Windows debe realizarse en el equipo del usuario; no se entrega ejecutable compilado para Windows.
