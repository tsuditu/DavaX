@echo off
setlocal
cd /d "%~dp0.."

REM --- check for OPENAI_API_KEY ---
if not defined OPENAI_API_KEY (
  echo [!] OPENAI_API_KEY not set. Run: win_scripts\setup_env.bat sk-...  or set it in Environment Variables.
  endlocal & exit /b 1
)

call ".venv\Scripts\activate.bat" || (endlocal & exit /b 1)
set "PYTHONPATH=%cd%"

python smart_librarian/main.py %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%