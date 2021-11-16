ECHO OFF
FOR /F "delims=" %%A IN ('cscript now_time_from_NTP.vbs') DO (
    ECHO %%A
    SET TIME_STR=%%A
)
ECHO ON