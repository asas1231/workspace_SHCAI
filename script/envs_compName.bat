If defined compName (Goto End) Else (Goto Start)

:Start

REM ¹q¸£¦WºÙ
for /f "skip=1 delims=" %%A in (
  'wmic computersystem get name'
) do for /f "delims=" %%B in ("%%A") do set "compName=%%A"
set abc=%compName%
:delright
if "%abc:~-1%"==" " set abc=%abc:~0,-1%&&goto delright
set compName=%abc%

:End