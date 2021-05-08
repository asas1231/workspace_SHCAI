If defined RO_envs (Goto End) Else (Goto Start)

:Start

title python FTP

REM 電腦名稱
call script\envs_compName.bat

REM 羽: Python
IF "%compName%" == "PC3" call D:\System\Users\A0244\anaconda3\Scripts\activate.bat D:\System\Users\A0244\anaconda3
IF "%compName%" == "SIN-HAO-PC2" call D:\A0244\anaconda3\Scripts\activate.bat D:\A0244\anaconda3

REM set PATH=%PATH%;.\script\adb\sed-4.2.1-bin\bin;
REM echo %compName%
REM 羽: 夜神 ADB
REM IF "%compName%" == "PC3   " set PATH=%PATH%;.\script\adb\platform-tools;

REM call conda.bat activate small-tools

Set RO_envs=1

:End