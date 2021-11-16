Function NTP()
  ' WScript.Echo "Get NTP time..."
  set objXML = CreateObject( "Microsoft.XMLHTTP" )
  ' objXML.Open "PUT", "http://utcnist.colorado.edu:13", False
  ' objXML.Open "PUT", "http://time-a-g.nist.gov:13", False
  objXML.Open "GET", "https://www.google.com", False
  objXML.Send
  If objXML.Status = 200 Then
    ' WScript.Echo objXML.getAllResponseHeaders
    ' WScript.Echo objXML.statusText
    ' WScript.Echo objXML.responsetext
    ' WScript.Echo "Computer time: " & Now()
    ' WScript.Echo "Computer time: " & %time%
  End If
  Set oShell = CreateObject ( "WScript.Shell" )
  oShell.run "cmd.exe /C TIME 23:59:59"
  ' WScript.Echo objXML.Status

  ' If objXML.Status = 200 Then  ' If HTTP request OK
  ' Set objADO = CreateObject("ADODB.Stream")
  ' objADO.Type = 1  ' Binary
  ' objADO.Open
  ' objADO.Write objXML.ResponseBody
  ' objADO.Position = 0  ' Set the stream position to the beginning
  ' On Error Resume Next
  ' objADO.SaveToFile strExceptionList, 2  ' Overwrite existing file
  ' If Err.Number <> 0 Then
    ' WScript.Echo Now() & ", ERROR [" & Err.Number & "] The file download failed. Check file location, no permissions or folder doesn't exist. " & Err.Description
    ' Exit Function
  ' Else
    ' WScript.Echo "  Success..."
  ' End If
  ' On Error GoTo 0
  ' objADO.Close : Set objADO = Nothing
  ' Else
  ' If HTTP request fails
  ' WScript.Echo Now() & ", ERROR [" & objXML.Status & " " & objXML.StatusText & "] The exception list download failed. Check file URL or access permissions. " & Err.Description
  ' Exit Function
  ' End If
  Set objXML = Nothing
End Function

call NTP