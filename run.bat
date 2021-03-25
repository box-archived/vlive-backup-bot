chcp 65001
@echo off
TITLE VLIVE-BACKUP-BOT
CLS

SET T1=기존 가상환경을 정리합니다.
SET T2=가상환경을 생성합니다.
SET T3=의존 프로그램을 설치합니다.
SET T4=의존프로그램 설치를 완료했습니다.
SET T5=프로그램을 실행합니다.

IF EXIST venv (
ECHO %T1%
ECHO.
rmdir /S /Q venv
)

ECHO %T2%
ECHO.
python -m venv venv

ECHO %T3%
ECHO.
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install -r requirements.txt

ECHO.
ECHO %T4%
ECHO.

ECHO %T5%
ECHO.
TIMEOUT /t 1 > nul
cls

venv\Scripts\python core.py
PAUSE
