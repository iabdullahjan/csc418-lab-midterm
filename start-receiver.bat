@echo off
cd /d "%~dp0"
title Report Receiver
set "PATH=%LOCALAPPDATA%\Python\bin;%PATH%"
python receiver\receiver.py
pause
