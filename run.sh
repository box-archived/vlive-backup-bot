#!/bin/sh

# Resize window
printf '\e[8;50;150t'

clear

# Move to shell dir
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

if [ -d "venv" ]; then
  echo 기존 가상환경을 정리합니다.
  echo
  rm -rf venv
fi

echo 가상환경을 생성합니다.
echo
python -m venv venv

echo 의존 프로그램을 설치합니다.
./venv/bin/python -m pip install --upgrade pip
./venv/bin/python -m pip install -r requirements.txt

echo
echo 의존 프로그램 설치를 완료했습니다.
echo

echo 프로그램을 실행합니다
echo
sleep 1
clear

./venv/bin/python core.py
