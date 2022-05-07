ECHO OFF
REM tasklist /FI “IMAGENAME eq EXE1.exe” /FO CSV > D:\log\log.log
REM FOR /F %%A IN (F:\log\log.log) do if %%A == 資訊: goto process_off

REM FOR /F "delims=" %%A IN ('cscript now_time_from_NTP.vbs') DO (
    REM ECHO %%A
    REM SET TIME_STR=%%A
REM )

cscript now_time_from_NTP.vbs
ECHO ON