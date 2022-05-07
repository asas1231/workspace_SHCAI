if /i "%~1"=="--min" start /MIN cmd /c %0 & goto :end


echo Hello world!

:end
    exit /B