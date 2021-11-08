echo on
set dns1=8.8.8.8
set dns2=8.8.4.4
REM SET interface[0]=0

REM change code page
chcp 65001 > nul

REM setting file name
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set dt=%%a
set FileName=%dt:~0,4%_%dt:~4,2%_%dt:~6,2%_DNS_information.txt
ECHO Status:Old setting>>%FileName%
ECHO TIME:%dt%>>%FileName%
ECHO.>>%FileName%

REM output error code(stderr) to file. check DNS status using file size.
nslookup %dns1% 2>temp_01.txt >>%FileName%
FOR /F "usebackq" %%A IN (temp_01.txt) DO set Temp_01_size=%%~zA
del temp_01.txt
IF %Temp_01_size%==0 (SET dns1_status=OK) ELSE (set dns1_status=NO)
if %dns1_status% == NO (
    echo Can not connect DNS, Please check network and DNS status
    PAUSE
    EXIT /b
)

REM chcp 950 > nul

call :GetWindowsVersion
REM check windows version exceptional
If not defined WindowsVersion (
    echo windows verion not setting: %VersionInformation%
    PAUSE
    EXIT /b
)

call :GetComputerName

REM del %FileName%

call :GetDNSList

FOR /F "" %%A IN ("%FileName%") DO set DNS_File_size=%%~zA
REM If 150 gtr %DNS_File_size% (
    REM ECHO Windows Version(%WindowsVersion%) isn't define interface.
    REM pause
    REM EXIT /b
REM )
ECHO.>>%FileName%
ECHO.>>%FileName%
ECHO.>>%FileName%
ECHO Status:New setting>>%FileName%
set For01_status=0
set For01_interface=""
for /F "delims=: tokens=1-2" %%a in (%FileName%) do (
    set For01_str=%%a
    :For01_Start
        if "%For01_status%"=="0" goto :For01_00
        if "%For01_status%"=="1" goto :For01_01
        if "%For01_status%"=="2" goto :For01_02

        goto :For01_End
    
    :For01_00
        if not "%For01_str%"=="%For01_str:Interface=%" (
            set For01_status=1
            set For01_interface=%%b
        )
        goto :For01_End
    
    :For01_01
        if /i "%For01_str%"=="DNS" (
            set For01_str02=%%b
            if /i "%For01_str02%"=="NONE" (
                set For01_status=0
            ) ELSE (
                if "%For01_str02:~0,3%" == "10." (
                    set For01_status=2
                )
            )
        ) ELSE (
            set For01_status=0
            goto :For01_Start
        )
        goto :For01_End
    
    :For01_02
        netsh interface %interface_type% set %dns_type% %For01_interface% static %dns1% primary
        netsh interface %interface_type% add %dns_type% %For01_interface% %dns2% index=2
        set For01_status=0
        goto :For01_End
    
    
    :For01_End
)

REM Record new DNS
netsh interface %interface_type% show %dns_type%>>%FileName%


echo Windows version: %WindowsVersion%
echo Computer name: %ComputerName%
REM PAUSE
EXIT /b

:GetWindowsVersion
    REM systeminfo
    for /f "delims=" %%A in ('ver') do set VersionInformation="%%A"
    REM https://zh-yue.wikipedia.org/wiki/Windows%E5%98%85%E7%89%88%E6%9C%AC%E4%B8%80%E8%A6%BD
    REM windows version is Windows 10
    echo %VersionInformation% | find " 10.0" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win10&& set HaveNetsh=netsh_01
    echo %VersionInformation% | find " 6.3" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win8.1&& set HaveNetsh=Yes
    echo %VersionInformation% | find " 6.2" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win8&& set HaveNetsh=Yes
    echo %VersionInformation% | find " 6.1" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win7&& set HaveNetsh=netsh_02
    echo %VersionInformation% | find " 6.0" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=WinVista&& set HaveNetsh=netsh_02
    REM Windows XP Professional x64 Edition
    echo %VersionInformation% | find " 5.2" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=WinXP&& set HaveNetsh=netsh_02
    echo %VersionInformation% | find " 5.1" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=WinXP&& set HaveNetsh=netsh_02
    echo %VersionInformation% | find " 5.0" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win2k&& set HaveNetsh=Yes
    echo %VersionInformation% | find " 4.9" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=WinMe&& set HaveNetsh=None
    echo %VersionInformation% | find " 4.1" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win98&& set HaveNetsh=None
    echo %VersionInformation% | find " 4.0" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win4&& set HaveNetsh=None
    echo %VersionInformation% | find " 4.00" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win95&& set HaveNetsh=None
    echo %VersionInformation% | find " 3.5" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win3.5&& set HaveNetsh=None
    echo %VersionInformation% | find " 3.51" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win3.51&& set HaveNetsh=None
    echo %VersionInformation% | find " 3.2" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win3.2&& set HaveNetsh=None
    echo %VersionInformation% | find " 3.1" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win3.1&& set HaveNetsh=None
    echo %VersionInformation% | find " 3.11" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win3.11&& set HaveNetsh=None
    echo %VersionInformation% | find " 3.10" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win3.10&& set HaveNetsh=None
    echo %VersionInformation% | find " 3.00" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win3.0&& set HaveNetsh=None
    echo %VersionInformation% | find " 2.11" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win2.11&& set HaveNetsh=None
    echo %VersionInformation% | find " 2.10" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win2.10&& set HaveNetsh=None
    echo %VersionInformation% | find " 2.03" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win2.03&& set HaveNetsh=None
    echo %VersionInformation% | find " 2.01" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win2.01&& set HaveNetsh=None
    echo %VersionInformation% | find " 1.04" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win1.04&& set HaveNetsh=None
    echo %VersionInformation% | find " 1.03" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win1.03&& set HaveNetsh=None
    echo %VersionInformation% | find " 1.02" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win1.02&& set HaveNetsh=None
    echo %VersionInformation% | find " 1.01" > nul
    if %ERRORLEVEL% == 0 set WindowsVersion=Win1.01&& set HaveNetsh=None
goto :eof


:GetComputerName
    REM Return ComputerName: 電腦名稱

    for /f "skip=1 delims=" %%A in (
      'wmic computersystem get name'
    ) do for /f "delims=" %%B in ("%%A") do set "ComputerName=%%A"
    set abc=%ComputerName%
    :DelRight_01
    if "%abc:~-1%"==" " (
        set abc=%abc:~0,-1%
        goto :DelRight_01
    )
    set ComputerName=%abc%
goto :eof


:GetDNSList
    if /i "%HaveNetsh%"=="netsh_01" (
        set interface_type=ipv4
        set dns_type=dnsservers
    )
    if /i "%HaveNetsh%"=="netsh_02" (
        set interface_type=ip
        set dns_type=dns
    )
    
    If not defined interface_type (
        goto :eof
    )
    REM netsh interface %interface_type% show %dns_type% > temp_01.txt
    REM interface[%interface_length%], set /a "interface_length+=1", echo %%Arr[%x%]%%
    REM interface[]='interface name',DNS 1 ip,DNS 2 ip,...,DNS n ip
    REM set interface_length=-1=interface[0]
    REM echo DBG_00
    set adapterfound_status=0
    REM for /f "delims=" %%a in (temp_01.txt) DO (
    set item_02=
    
    SETLOCAL ENABLEDELAYEDEXPANSION
    for /f "usebackq delims=" %%a in (`netsh interface %interface_type% show %dns_type%`) DO (
        set item=%%a
        set item=!item:"='!
        REM Configuration for interface "區域連線* 12"
        call :ProcessDNSInformation "!item!"
    )
    
    endlocal
goto :eof


:ProcessDNSInformation
    set DNSInformation=%~1
    REM echo %adapterfound_status% - %DNSInformation%
    REM goto :GetDNSList_For01_If01_End
    
    :GetDNSList_For01_If01_Start
    if "%adapterfound_status%"=="1" goto :GetDNSList_For01_If01_01
    if not "%DNSInformation%"=="%DNSInformation:interface=%" goto :GetDNSList_For01_If01_02
    if not "%DNSInformation%"=="%DNSInformation:DNS=%" goto :GetDNSList_For01_If01_03
 
    goto :GetDNSList_For01_If01_End
    
    :GetDNSList_For01_If01_01
        REM set adapterfound_status=0
        REM exit /b
        REM echo If01_01
        REM setlocal enableDelayedExpansion
        REM echo [OUT] !interface[%interface[0]%]!
        REM ECHO DNS:%DNS%>>%FileName%
        REM endlocal
        :DelLeft_03
        if "%DNSInformation:~0,1%"==" " (
            set DNSInformation=%DNSInformation:~1%
            goto :DelLeft_03
        )
        REM echo DBG_00: %DNSInformation%
        if "%DNSInformation%"=="%DNSInformation:.=%" (
            set adapterfound_status=0
            ECHO.>>%FileName%
            REM echo DBG_01
            goto :GetDNSList_For01_If01_Start
        ) ELSE (
            ECHO DNS:%DNSInformation%>>%FileName%
            REM echo DBG_02
        )
        goto :GetDNSList_For01_If01_End
    
    :GetDNSList_For01_If01_02
        REM echo If01_02
        REM echo DBG_01: %DNSInformation%
        call :GetInterfaceNameByParse "%DNSInformation:"='%"
        REM call echo %%interface[%interface[0]%]%%
        goto :GetDNSList_For01_If01_End
    
    :GetDNSList_For01_If01_03
        REM echo If01_03
        for /f "delims=: tokens=1-2" %%i in ("%DNSInformation%") do set DNS=%%j
        :DelLeft_02
        if "%DNS:~0,1%"==" " (
            set DNS=%DNS:~1%
            goto :DelLeft_02
        )
        if "%DNS%"=="%DNS:.=%" (
            REM setlocal enableDelayedExpansion
            REM set interface[%interface[0]%]=!interface[%interface[0]%]!,NONE
            ECHO DNS:NONE>>%FileName%
            ECHO.>>%FileName%
            REM endlocal
        ) ELSE (
            REM setlocal enableDelayedExpansion
            ECHO DNS:%DNS%>>%FileName%
            REM set interface[%interface[0]%]=!interface[%interface[0]%]!,!DNS!
            REM endlocal
            set adapterfound_status=1
        )
        goto :GetDNSList_For01_If01_End
    
    :GetDNSList_For01_If01_End
    
    REM echo DBG_00: "%DNSInformation%"

goto :eof

:GetInterfaceNameByParse
    set InterfaceInformation=%~1
    REM ECHO %InterfaceInformation%
    SET GetInterfaceNameByParseCompareString='
    REM :~start,length
    REM %item% = %item:~0,1%%item:~1,-1%%item:~-1% = %item:~0,1%%item:~1%=%item:~0,-1%%item:~-1%
    REM ECHO Length: %interface[0]%
    :DelLeft_01
    REM echo %InterfaceInformation%
    IF "%InterfaceInformation:~0,1%"== "%GetInterfaceNameByParseCompareString%" (
        REM set /a "interface[0]+=1"
        REM set interface[%interface[0]%]=%InterfaceInformation%
        REM ECHO %InterfaceInformation%
        REM set InterfaceInformation=%InterfaceInformation:'=%
        REM ECHO %InterfaceInformation:~1,-1%
        ECHO Interface:"%InterfaceInformation:~1,-1%">>%FileName%
        ECHO Interface:"%InterfaceInformation:~1,-1%"
        REM echo InterfaceInformation=%InterfaceInformation%
        REM echo IN01: !interface[%interface[0]%]! _ %interface[0]%
    ) else (
        set InterfaceInformation=%InterfaceInformation:~1%
        goto :DelLeft_01
    )
    
    REM echo IN02: !interface[%interface[0]%]!

goto :eof


:GetTemp
    FOR /F "delims=: tokens=2" %a in ('ipconfig ^| find "IPv4"') do set _IPAddress=%a
    for /f "delims=" %A in ('ver') do set Version=%A
    for /f "tokens=2 delims==" %a in ('wmic OS Get localdatetime /value') do set "dt=%a"
    set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
    set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
goto :eof