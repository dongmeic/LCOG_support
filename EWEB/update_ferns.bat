@echo off
activate geoenv & python download_FERNS.py & conda deactivate & for %%n in (1,2,3) do C:\Users\clid1852\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone\python.exe FERNS_for_AGO_step%%n.py & activate geoenv & python report_FERNS.py & conda deactivate
