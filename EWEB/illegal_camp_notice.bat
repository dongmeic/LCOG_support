@echo off
C:\Users\clid1852\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone\python.exe illegal_camp_notice_1.py
set YYYYMMDD=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%
if exist T:\DCProjects\GitHub\LCOG_support\EWEB\%YYYYMMDD%.txt (
del "T:\DCProjects\GitHub\LCOG_support\EWEB\%YYYYMMDD%.txt"
echo "No further steps needed"
) else (
activate geoenv & python illegal_camp_notice_2.py & conda deactivate 
)