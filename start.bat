:1
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2%
python Apul3.py redirectors.txt 3 WindowsChrome -o "Log%ldt%.log" -ss screens -to 5 -w 10
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2%
python Apul3.py redirectors.txt 3 WindowsEdge -o "Log%ldt%.log" -ss screens -to 5 -w 10
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2%
python Apul3.py redirectors.txt 3 WindowsFirefox -o "Log%ldt%.log" -ss screens -to 5 -w 10
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2%
python Apul3.py redirectors.txt 3 WindowsIE -o "Log%ldt%.log" -ss screens -to 5 -w 10
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2%
python Apul3.py redirectors.txt 3 iPhoneSafari -o "Log%ldt%.log" -ss screens -to 5 -w 10
rem for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
rem set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2%
rem python Apul3.py redirectors.txt 3 iPadSafari -o "Log%ldt%.log" -ss screens -to 5 -w 10
goto :1