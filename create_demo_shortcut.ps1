$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Desktop = [Environment]::GetFolderPath('Desktop')
$Shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $Desktop 'CineStage Manager DEMO.lnk'))
$PyW = Join-Path $ProjectDir '.venv\Scripts\pythonw.exe'
if (-not (Test-Path -LiteralPath $PyW)) {
  $cmd = Get-Command pythonw.exe -ErrorAction SilentlyContinue
  if ($cmd) { $PyW = $cmd.Source }
}
if (Test-Path -LiteralPath $PyW) {
  $Shortcut.TargetPath = $PyW
  $Shortcut.Arguments = '"' + (Join-Path $ProjectDir 'demo_launcher.py') + '"'
} else {
  $Shortcut.TargetPath = Join-Path $ProjectDir 'run_demo_windows.bat'
}
$Shortcut.WorkingDirectory = $ProjectDir
$icon = Join-Path $ProjectDir 'assets\CineStageManager.ico'
if (Test-Path -LiteralPath $icon) { $Shortcut.IconLocation = "$icon,0" }
$Shortcut.Description = 'CineStage Manager — DEMO artística'
$Shortcut.Save()
Write-Host 'Acceso directo DEMO actualizado.'
