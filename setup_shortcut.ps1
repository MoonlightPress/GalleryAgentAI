# Mochi Atelier — Desktop Shortcut Installer
# Right-click this file → Run with PowerShell
#
# What it does:
#   1. Converts Content/Icon.png → static/mochi_icon.ico
#   2. Writes launch_mochi.vbs  (silent launcher — starts API + React, opens browser)
#   3. Drops "Mochi Atelier" on your Desktop with that icon
#
# After running: drag the Desktop shortcut onto the taskbar to pin it.

$ErrorActionPreference = "Stop"

$ProjectRoot  = "C:\ScottStuff\GalleryAgentAI"
$SourcePng    = "$ProjectRoot\Content\Icon.png"
$IconPath     = "$ProjectRoot\static\mochi_icon.ico"
$VbsPath      = "$ProjectRoot\launch_mochi.vbs"
$ShortcutPath = [System.IO.Path]::Combine([Environment]::GetFolderPath("Desktop"), "Mochi Atelier.lnk")

Write-Host ""
Write-Host "  Mochi Atelier — Shortcut Installer" -ForegroundColor Yellow
Write-Host "  =====================================" -ForegroundColor Yellow
Write-Host ""

# ── 1. Convert source image to ICO via Python/Pillow ─────────────────────────
Write-Host "  [1/3] Generating icon..."

$py = @"
from PIL import Image
img = Image.open(r'$SourcePng').convert('RGBA')
w, h = img.size
s = min(w, h)
img = img.crop(((w-s)//2, (h-s)//2, (w+s)//2, (h+s)//2))
img.save(r'$IconPath', format='ICO', sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
print('ok')
"@

$result = python -c $py 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Could not generate icon. Is Pillow installed? (pip install Pillow)" -ForegroundColor Red
    Write-Host "  $result" -ForegroundColor Red
    pause; exit 1
}
Write-Host "     -> $IconPath" -ForegroundColor DarkGray

# ── 2. Write the silent VBScript launcher ────────────────────────────────────
Write-Host "  [2/3] Writing launcher..."

$vbs = @'
' launch_mochi.vbs — silent launcher for Mochi Atelier
' Checks :5177 (React/Vite) and :8001 (FastAPI). Starts both if needed. Opens browser.

Dim objShell, objHTTP, frontendRunning, apiRunning

Set objShell = CreateObject("WScript.Shell")
Set objHTTP  = CreateObject("MSXML2.XMLHTTP")
Dim root : root = "C:\ScottStuff\GalleryAgentAI"

frontendRunning = False
On Error Resume Next
objHTTP.Open "GET", "http://localhost:5177", False
objHTTP.Send
If Err.Number = 0 Then
    If objHTTP.Status > 0 Then frontendRunning = True
End If
Err.Clear
On Error GoTo 0

apiRunning = False
On Error Resume Next
objHTTP.Open "GET", "http://localhost:8001/api/health", False
objHTTP.Send
If Err.Number = 0 Then
    If objHTTP.Status = 200 Then apiRunning = True
End If
Err.Clear
On Error GoTo 0

If Not apiRunning Then
    objShell.Run "cmd /c cd /d " & root & " && python api.py", 0, False
End If

If Not frontendRunning Then
    objShell.Run "cmd /c cd /d " & root & "\frontend && npm run dev", 0, False
    WScript.Sleep 5000
ElseIf Not apiRunning Then
    WScript.Sleep 2000
End If

objShell.Run "http://localhost:5177"
'@

[System.IO.File]::WriteAllText($VbsPath, $vbs, [System.Text.Encoding]::ASCII)
Write-Host "     -> $VbsPath" -ForegroundColor DarkGray

# ── 3. Create Desktop shortcut ────────────────────────────────────────────────
Write-Host "  [3/3] Creating Desktop shortcut..."

if (Test-Path $ShortcutPath) { Remove-Item $ShortcutPath -Force }

$wsh = New-Object -ComObject WScript.Shell
$lnk = $wsh.CreateShortcut($ShortcutPath)
$lnk.TargetPath       = "wscript.exe"
$lnk.Arguments        = "`"$VbsPath`""
$lnk.WorkingDirectory = $ProjectRoot
$lnk.IconLocation     = "$IconPath,0"
$lnk.Description      = "Mochi's Atelier — Nin's career assistant"
$lnk.Save()

Write-Host "     -> $ShortcutPath" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Done! Mochi Atelier is on your Desktop." -ForegroundColor Green
Write-Host ""
Write-Host "  Drag the shortcut onto your taskbar to pin it." -ForegroundColor Cyan
Write-Host ""
pause
