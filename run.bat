
@echo off
chcp 65001 > nul

python app.py

if errorlevel 1 (
    echo.
    echo Не удалось запустить приложение.
    echo Проверьте, установлен ли Python.
    pause
)
