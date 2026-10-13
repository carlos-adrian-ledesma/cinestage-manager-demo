@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
 echo Falta Python 3.11 o superior. Instala Python con Tkinter y agrega Python a PATH.
 pause
 exit /b 1
)
python -c "import tkinter; from demo.demo_runtime import init_demo; init_demo(); print('CineStage DEMO inicializada')"
if errorlevel 1 (
 echo No se pudo inicializar la demostracion.
 pause
 exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0create_demo_shortcut.ps1"
echo DEMO lista. Ejecuta run_demo_windows.bat o el acceso directo.
pause
