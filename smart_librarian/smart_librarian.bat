@echo off
cd /d "%~dp0"

call win_scripts\install.bat          || exit /b %errorlevel%
REM If the key is already in your environment, you can pass %OPENAI_API_KEY%; otherwise, keep the command as you currently use it.
call win_scripts\setup_env.bat %OPENAI_API_KEY%  || exit /b %errorlevel%
call win_scripts\build_index.bat      || exit /b %errorlevel%
call win_scripts\chat.bat             || exit /b %errorlevel%
