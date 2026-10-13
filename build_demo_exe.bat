@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (echo Primero instala Python 3.11 o superior & exit /b 1)
python -m pip install pyinstaller
if errorlevel 1 exit /b 1
python -m PyInstaller --noconfirm --clean --windowed ^
 --name CineStageManager_DEMO ^
 --icon "assets\CineStageManager.ico" ^
 --add-data "assets;assets" ^
 demo_launcher.py
if errorlevel 1 exit /b 1
echo Resultado: dist\CineStageManager_DEMO\CineStageManager_DEMO.exe
