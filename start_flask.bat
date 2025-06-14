@echo off
REM Устанавливаем переменные окружения для Flask
set FLASK_APP=app
set FLASK_ENV=development

REM Запускаем Flask в режиме отладки
flask --debug run
