@echo off
cd /d "%~dp0"
title Report Receiver
python receiver\receiver.py
pause
