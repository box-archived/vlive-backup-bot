chcp 65001
@echo off
TITLE VLIVE-BACKUP-BOT
CLS

ECHO LOADING...
IF EXIST venv (
rmdir /S /Q venv
)

python -m venv venv

venv\Scripts\python -m pip install -q -q -q --upgrade pip
venv\Scripts\python -m pip install -q -q -q -r requirements.txt

TIMEOUT /t 1 > nul
CLS

venv\Scripts\python core.py
PAUSE
