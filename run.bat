REM �q���W��
call script\envs_compName.bat

REM ��: Python
IF "%compName%" == "PC3"         set work_path="G:\�{��\Python\RO_�Ķ����"
IF "%compName%" == "SIN-HAO-PC2" set work_path="D:\A0244\Program\Python\workspace"
echo "%compName%"
REM 
cd /D %work_path%

call script\init.bat
start pythonw.exe run.py