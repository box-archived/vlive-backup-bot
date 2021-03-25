chcp 65001
@echo off
TITLE VLIVE-BACKUP-BOT
mode con: cols=150 lines=50
CLS

echo "┌──────────────────VLIVE-DOWNLOADER-BOT───────────────────┐";
echo "│                                                         │";
echo "│                        LOADING...                       │";
echo "│                                                         │";
echo "└─────────────────────────────────────────────────────────┘";
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
