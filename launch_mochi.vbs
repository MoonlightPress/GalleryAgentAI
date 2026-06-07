' launch_mochi.vbs ??silent launcher for Mochi Atelier
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