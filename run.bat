REM 電腦名稱
call script\envs_compName.bat

REM 羽: Python
IF "%compName%" == "PC3"         set work_path="G:\程式\Python\RO_採集資料"
IF "%compName%" == "SIN-HAO-PC2" set work_path="D:\A0244\Program\Python\workspace"
echo "%compName%"
REM 
cd /D %work_path%

call script\init.bat
start pythonw.exe run.py