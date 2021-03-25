#!/bin/sh

PCOMMAND=NONE
# Check python version

# check python
PV0=`python --version`
PV0=${PV3:0:8}
if [ "$PV0" == "Python 3" ]; then
  PCOMMAND=python
fi

# check python3
PV3=`python3 --version`
PV3=${PV3:0:8}
if [ "$PV3" == "Python 3" ]; then
  PCOMMAND=python3
fi

if [ "$PCOMMAND" == "NONE" ]; then
  clear
  echo ===VLIVE-BACKUP-BOT===
  echo Python 3.x not found
  echo Please install python
  echo
  $PCOMMAND -m webbrowser https://www.python.org/downloads/
  exit
fi

# Resize window
printf '\e[8;9;60t'

clear
echo
echo ====================VLIVE-DOWNLOADER-BOT====================
echo
echo
echo "                           LOADING..."
echo
echo
echo ============================================================

# Move to shell dir
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

if [ -d "venv" ]; then
  rm -rf venv
fi

python -m venv venv

./venv/bin/$PCOMMAND -m pip install -q -q -q --upgrade pip
./venv/bin/$PCOMMAND -m pip install -q -q -q -r requirements.txt

printf '\e[8;50;150t'
clear
./venv/bin/$PCOMMAND core.py
