chcp 65001
@echo off
TITLE VLIVE-BACKUP-BOT
CLS

IF EXIST venv (
ECHO 기존 가상환경을 정리합니다.
ECHO.
rmdir /S /Q venv
)

ECHO 가상환경을 생성합니다.
ECHO.
python -m venv venv

ECHO 의존 프로그램을 설치합니다.
ECHO.
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt

ECHO.
ECHO 의존 프로그램 설치를 완료했습니다.
ECHO.

ECHO 프로그램을 실행합니다.
ECHO.
TIMEOUT /t 1 > nul
cls

venv\Scripts\python core.py
PAUSE
