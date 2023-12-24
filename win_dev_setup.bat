@ECHO OFF
@REM A script to setup the dev env varibles,
@REM including the venv.

cd bowlpicks
@REM Set the Django settings.py settings for development.
set DEVELOPMENT_MODE=True

@REM Set DEBUG to True if you want to see the Django error pages.
@REM DO NOT SET 'DEBUG' TO TRUE IN PRODUCTION
@REM set DEBUG=True

CALL ..\venv\Scripts\activate.bat
@REM py manage.py runserver