@echo off
setlocal
cd /d "%~dp0"
title CineStage Manager DEMO - Diagnostico
where python.exe >nul 2>nul
if errorlevel 1 (echo Python no disponible. & pause & exit /b 1)
python.exe "%~dp0demo_launcher.py"
if errorlevel 1 echo Revisa el log: %%TEMP%%\CineStageManager_DEMO\inicio_error.log
pause
