chcp 65001
@echo off
TITLE VLIVE-BACKUP-BOT
mode con: cols=150 lines=50
CLS

echo "____   ___.____    ._______   ______________               ";
echo "\   \ /   |    |   |   \   \ /   \_   _____/               ";
echo " \   Y   /|    |   |   |\   Y   / |    __)_                ";
echo "  \     / |    |___|   | \     /  |        \               ";
echo "   \___/  |_______ |___|  \___/  /_______  /               ";
echo "                  \/                     \/                ";
echo "__________   _____  _________  ____  __.____ _____________ ";
echo "\______   \ /  _  \ \_   ___ \|    |/ _|    |   \______   \";
echo " |    |  _//  /_\  \/    \  \/|      < |    |   /|     ___/";
echo " |    |   /    |    \     \___|    |  \|    |  / |    |    ";
echo " |______  \____|__  /\______  |____|__ |______/  |____|    ";
echo "        \/        \/        \/        \/                   ";
echo "_____________________________                              ";
echo "\______   \_____  \__    ___/                              ";
echo " |    |  _//   |   \|    |                                 ";
echo " |    |   /    |    |    |                                 ";
echo " |______  \_______  |____|                                 ";
echo "        \/        \/                                       ";
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
