#!/bin/sh

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

./venv/bin/python -m pip install -q -q -q --upgrade pip
./venv/bin/python -m pip install -q -q -q -r requirements.txt

printf '\e[8;50;150t'
clear
./venv/bin/python core.py
