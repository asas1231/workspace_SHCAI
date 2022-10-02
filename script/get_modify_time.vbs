Option Explicit

Function GetRecentFile( path )
    Dim fso, file
    Set fso = CreateObject( "Scripting.FileSystemObject" )
    Set GetRecentFile = Nothing
    For Each file in fso.GetFolder( path ).Files
        WScript.Echo file.DateLastModified & ", " & file.Name
    Next
End Function

Function GetFileModifyDate( file_path )
    Set GetFileModifyDate = Nothing
    Dim fso, file
    Set fso = CreateObject( "Scripting.FileSystemObject" )
    If fso.FileExists( file_path ) Then
        set file = fso.GetFile( file_path )
        WScript.Echo file.DateLastModified & ", " & file.Name
    Else
        WScript.Echo "File not exist. File: " & file_path
    End If
End Function

Dim recentFile
' Set recentFile = GetFileModifyDate( "C:\get_modify_time.vbs" )
Set recentFile = GetFileModifyDate( "get_modify_time.vbs" )
Set recentFile = GetFileModifyDate( "get_modify_time2.vbs" )
