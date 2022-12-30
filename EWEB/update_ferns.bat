@echo off
activate geoenv & python download_FERNS.py & conda deactivate & C:\Users\clid1852\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone\python.exe FERNS_for_AGO_step2.py