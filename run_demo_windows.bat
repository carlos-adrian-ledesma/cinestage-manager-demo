@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
    start "" /D "%~dp0" "%CD%\.venv\Scripts\pythonw.exe" "%CD%\demo_launcher.py"
    exit /b 0
)
where pythonw.exe >nul 2>nul
if not errorlevel 1 (
    start "" /D "%~dp0" pythonw.exe "%CD%\demo_launcher.py"
    exit /b 0
)
call "%~dp0run_demo_debug_windows.bat"
