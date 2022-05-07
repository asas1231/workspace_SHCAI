' https://www.w3schools.com/asp/asp_ref_vbscript_functions.asp
Function NTP()
  ' WScript.Echo "Get NTP time..."
  offsetSeconds = 28800 + 0
  changeLimit = 60000
  set objXML = CreateObject( "Microsoft.XMLHTTP" )
  ' objXML.Open "PUT", "http://utcnist.colorado.edu:13", False
  webURL = "http://time-a-g.nist.gov:13"
  webURL = "http://tock.stdtime.gov.tw:13"
  webURL = "http://time.chttl.com.tw:13?randombit=" & Timer
  webURL = "time.windows.com"
  ' webURL = "https://www.google.com?randombit=" & Rnd()
  WScript.Echo webURL
  objXML.Open "GET", webURL, False
  objXML.Send
  If objXML.Status = 200 Then
    WScript.Echo "Response Headers:"
    WScript.Echo objXML.getAllResponseHeaders
    ' WScript.Echo objXML.statusText
    WScript.Echo ""
    WScript.Echo "Response Text"
    WScript.Echo objXML.responsetext
    ' WScript.Echo "Computer time: " & Now()
    ' WScript.Echo "Computer time: " & %time%
    str = objXML.getAllResponseHeaders
    arr = Split( str , vbCrLf )
    For i = 0 To UBound( arr )
        ' WScript.Echo i & " " & InStr( LCase( arr( i ) ) , "date:" ) & ": " & arr( i )
        If InStr( LCase( arr( i ) ) , "date:" ) > 0 Then
            dateTime = Trim( Right( arr( i ) , Len( arr( i ) ) - ( 4 + InStr( LCase( arr( i ) ) , "date:" ) ) ) )
        End If
    Next
    ' WScript.Echo "Date time: " & dateTime
    serverTime = Mid( dateTime , InStr( dateTime , ":" ) - 2 , 8 )
    ' WScript.Echo "Server time: " & serverTime
    serverHour   = CInt( Mid( serverTime , 1 , 2 ) )
    serverMinute = CInt( Mid( serverTime , 4 , 2 ) )
    serverSecond = CInt( Mid( serverTime , 7 , 2 ) ) + offsetSeconds
    serverMinute = serverMinute + serverSecond \ 60
    serverSecond = serverSecond Mod 60
    serverHour   = serverHour   + serverMinute \ 60
    serverMinute = serverMinute Mod 60
    serverHour   = serverHour   Mod 24
    ' WScript.Echo serverHour & ":" & serverMinute & ":" & serverSecond
    If serverHour < 23 And serverHour > 0 And False Then
        ' WScript.Echo "Now time: " & Timer
        If Abs( ( ( serverHour * 60 + serverMinute ) * 60 + serverSecond ) - Timer ) < changeLimit Then
            ' WScript.Echo Hour( dateTime ) & ":" & Minute( dateTime )  & ":" & Second( dateTime )
            NewLocalTime = serverHour & ":" & serverMinute & ":" & serverSecond
            ' WScript.Echo NewLocalTime
            Set oShell = CreateObject ( "WScript.Shell" )
            oShell.run "cmd.exe /C TIME " & NewLocalTime
        End If
    End If
  End If
  ' Set oShell = CreateObject ( "WScript.Shell" )
  ' oShell.run "cmd.exe /C TIME 23:59:59"
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

' call NTP
call RequestTimeFromNTP

Function RequestTimeFromNTP()
    Set objSkt = CreateObject( "MSWINSOCK.Winsock" )
    WScript.Echo "End Request Time From NTP"
End Function

' import socket
' import struct
' import sys
' import time
' def RequestTimefromNtp(addr='time.windows.com'):
'     REF_TIME_1970 = 2208988800  # Reference time
'     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
'     data = b'\x1b' + 47 * b'\0'
'     client.sendto(data, (addr, 123))
'     data, address = client.recvfrom(1024)
'     if data:
'         t = struct.unpack('!12I', data)[10]
'         t -= REF_TIME_1970
'     return time.ctime(t), t
' 
' >>> RequestTimefromNtp()
' ('Sat Apr  9 18:55:47 2022', 1649501747)