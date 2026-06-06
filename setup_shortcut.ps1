# Mochi Atelier — Desktop Shortcut Installer
# Right-click this file → Run with PowerShell
#
# What it does:
#   1. Generates static/mochi_icon.ico  (cat face, warm atelier palette)
#   2. Writes launch_mochi.vbs          (silent launcher — starts server if needed, opens browser)
#   3. Drops "Mochi Atelier" on your Desktop with that icon
#
# After running: right-click the Desktop shortcut → Pin to Start  (or drag to taskbar)

$ErrorActionPreference = "Stop"

$ProjectRoot  = "C:\ScottStuff\GalleryAgentAI"
$IconPath     = "$ProjectRoot\static\mochi_icon.ico"
$VbsPath      = "$ProjectRoot\launch_mochi.vbs"
$ShortcutPath = "$env:USERPROFILE\Desktop\Mochi Atelier.lnk"

Write-Host ""
Write-Host "  Mochi Atelier — Shortcut Installer" -ForegroundColor Yellow
Write-Host "  =====================================" -ForegroundColor Yellow
Write-Host ""

# ── 1. Generate icon (pure .NET — no Python required) ────────────────────────
Write-Host "  [1/3] Generating icon..."
Add-Type -AssemblyName System.Drawing

$sz    = 256
$bmp   = New-Object System.Drawing.Bitmap($sz, $sz)
$g     = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode      = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint  = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

# Palette — matches app.py CSS tokens
$cream  = [System.Drawing.Color]::FromArgb(247, 239, 226)
$amber  = [System.Drawing.Color]::FromArgb(200, 141,  90)
$dark   = [System.Drawing.Color]::FromArgb( 63,  48,  39)
$soft   = [System.Drawing.Color]::FromArgb(230, 210, 185)
$pink   = [System.Drawing.Color]::FromArgb(210, 150, 140)

function Brush($c) { New-Object System.Drawing.SolidBrush($c) }
function Pen($c,$w) { New-Object System.Drawing.Pen($c, $w) }

# Background: cream
$g.FillRectangle((Brush $cream), 0, 0, $sz, $sz)

# Cat ears (amber triangles)
$earPath = { param($pts)
    $p = New-Object System.Drawing.Drawing2D.GraphicsPath
    $p.AddPolygon($pts)
    $p
}

$earL = & $earPath @(
    [System.Drawing.Point]::new( 50, 130),
    [System.Drawing.Point]::new( 88,  44),
    [System.Drawing.Point]::new(126, 114)
)
$g.FillPath((Brush $amber), $earL)

$earR = & $earPath @(
    [System.Drawing.Point]::new(130, 114),
    [System.Drawing.Point]::new(168,  44),
    [System.Drawing.Point]::new(206, 130)
)
$g.FillPath((Brush $amber), $earR)

# Inner ears (pink)
$earLi = & $earPath @(
    [System.Drawing.Point]::new( 68, 122),
    [System.Drawing.Point]::new( 90,  74),
    [System.Drawing.Point]::new(112, 114)
)
$g.FillPath((Brush $pink), $earLi)

$earRi = & $earPath @(
    [System.Drawing.Point]::new(144, 114),
    [System.Drawing.Point]::new(166,  74),
    [System.Drawing.Point]::new(188, 122)
)
$g.FillPath((Brush $pink), $earRi)

# Head (large amber ellipse)
$g.FillEllipse((Brush $amber),  42, 106, 172, 148)

# Cheek patches (soft)
$g.FillEllipse((Brush $soft),  52, 178,  60,  36)
$g.FillEllipse((Brush $soft), 144, 178,  60,  36)

# Eyes — white sclera
$g.FillEllipse((Brush $cream),  82, 142,  38,  28)
$g.FillEllipse((Brush $cream), 136, 142,  38,  28)

# Pupils
$g.FillEllipse((Brush $dark),   95, 147,  15,  18)
$g.FillEllipse((Brush $dark),  147, 147,  15,  18)

# Eye shine (small white dot)
$g.FillEllipse((Brush $cream),  95, 147,   5,   5)
$g.FillEllipse((Brush $cream), 147, 147,   5,   5)

# Nose (small pink triangle)
$nose = & $earPath @(
    [System.Drawing.Point]::new(122, 192),
    [System.Drawing.Point]::new(128, 182),
    [System.Drawing.Point]::new(134, 192)
)
$g.FillPath((Brush $pink), $nose)

# Mouth
$mouthPen = Pen $dark 2.0
$g.DrawArc($mouthPen, 108, 190,  18, 10, 0, 180)
$g.DrawArc($mouthPen, 130, 190,  18, 10, 0, 180)

# Whiskers
$wPen = Pen ([System.Drawing.Color]::FromArgb(160, 63, 48, 39)) 1.5
$g.DrawLine($wPen,  44, 194, 100, 190)
$g.DrawLine($wPen,  44, 203, 100, 200)
$g.DrawLine($wPen, 156, 190, 212, 194)
$g.DrawLine($wPen, 156, 200, 212, 203)

$g.Dispose()

# Encode as PNG, then wrap in ICO container (PNG-in-ICO, Windows Vista+)
$pngStream = New-Object System.IO.MemoryStream
$bmp.Save($pngStream, [System.Drawing.Imaging.ImageFormat]::Png)
$pngBytes  = $pngStream.ToArray()
$pngStream.Close()
$bmp.Dispose()

$icoStream = New-Object System.IO.MemoryStream
$bw = New-Object System.IO.BinaryWriter($icoStream)
$bw.Write([uint16]0)                      # Reserved
$bw.Write([uint16]1)                      # Type = ICO
$bw.Write([uint16]1)                      # Image count = 1
$bw.Write([byte]0)                        # Width  (0 = 256)
$bw.Write([byte]0)                        # Height (0 = 256)
$bw.Write([byte]0)                        # ColorCount
$bw.Write([byte]0)                        # Reserved
$bw.Write([uint16]1)                      # Planes
$bw.Write([uint16]32)                     # Bit depth
$bw.Write([uint32]$pngBytes.Length)       # Bytes in image
$bw.Write([uint32]22)                     # Offset: 6 (ICONDIR) + 16 (ICONDIRENTRY)
$bw.Write($pngBytes)
$bw.Flush()
[System.IO.File]::WriteAllBytes($IconPath, $icoStream.ToArray())
$icoStream.Close()

Write-Host "     -> $IconPath" -ForegroundColor DarkGray

# ── 2. Write the silent VBScript launcher ────────────────────────────────────
Write-Host "  [2/3] Writing launcher..."

$vbs = @'
' launch_mochi.vbs — silent launcher for Mochi Atelier
' Checks whether Streamlit is already running on :8501.
' If not, starts it silently. Then opens the browser.

Dim objShell, objHTTP, running

Set objShell = CreateObject("WScript.Shell")
Set objHTTP  = CreateObject("MSXML2.XMLHTTP")

running = False
On Error Resume Next
objHTTP.Open "GET", "http://localhost:8501", False
objHTTP.Send
If Err.Number = 0 Then
    If objHTTP.Status = 200 Then running = True
End If
On Error GoTo 0

If Not running Then
    ' Start Streamlit with no visible window (0 = hidden, False = don't wait)
    objShell.Run "cmd /c cd /d C:\ScottStuff\GalleryAgentAI && python -m streamlit run app.py --server.headless true", 0, False
    WScript.Sleep 4000
End If

objShell.Run "http://localhost:8501"
'@

[System.IO.File]::WriteAllText($VbsPath, $vbs, [System.Text.Encoding]::ASCII)
Write-Host "     -> $VbsPath" -ForegroundColor DarkGray

# ── 3. Create Desktop shortcut ────────────────────────────────────────────────
Write-Host "  [3/3] Creating Desktop shortcut..."

$wsh          = New-Object -ComObject WScript.Shell
$lnk          = $wsh.CreateShortcut($ShortcutPath)
$lnk.TargetPath        = "wscript.exe"
$lnk.Arguments         = "`"$VbsPath`""
$lnk.WorkingDirectory  = $ProjectRoot
$lnk.IconLocation      = "$IconPath,0"
$lnk.Description       = "Mochi's Atelier — Nin's career assistant"
$lnk.Save()

Write-Host "     -> $ShortcutPath" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Done! Mochi Atelier is on your Desktop." -ForegroundColor Green
Write-Host ""
Write-Host "  Right-click the shortcut -> Pin to Start" -ForegroundColor Cyan
Write-Host "  Or drag it to the taskbar." -ForegroundColor Cyan
Write-Host ""
Write-Host "  Clicking the shortcut will start the server if it isn't" -ForegroundColor DarkGray
Write-Host "  already running, then open the dashboard in your browser." -ForegroundColor DarkGray
Write-Host ""
pause
